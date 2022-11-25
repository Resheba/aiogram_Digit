#______________________Imports__________________
import logging, datetime, sys
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import link, hlink
from asyncio.exceptions import TimeoutError
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DataBase.db_api import *
from DataBase.w2v import model_start
from Keyboard.keyboard import *
from states import Registration, Checker, AuthMenu, Refresh
from rec_sys import selection, lem_selection, w2v_selection, w2v_selection_advance

#_____________Config_______________
from API_Token import API_TOKEN
logging.basicConfig(level = logging.INFO)
bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())

no_answer = 'Не распознал ответ.'
stopwords = ('/start',)
req_text = '👤 Ваше приглашение о встречи отправлено, если человека устроит ваше предложение я сразу вам сообщу!'
events_menu_text = f'''Ближайшие Event\'ы:\n
📣25.10 📍 В среду идём в бар🍺🍾. С меня по бесплатному коктейлю.({hlink('Макс', 'https://t.me/makson')})\n
📣28.10 📍 Есть желающие поиграть в пятничный боулинг? Подробнее в лс.({hlink('Кирилл', 'https://t.me/kirill')})'''

async def on_startup(_):
	await db_start()
	await model_start()

async def show_likes(telegram_id):
	form = 'Последние встречи:\n'
	meetings = await get_likes(telegram_id)
	if meetings:
		for meet in meetings:
			id = meet[1] if meet[1]!=telegram_id else meet[2]
			user = await get_user(id)
			name = user[3]
			nametage = 'https://t.me/'+user[1]
			time = meet[3] if meet[3] else 'Время не выбрано'
			string = hlink(name, nametage)+' | '+time+'\n'
			form+='📍 '+'🔔 '+string
		return form
	return 'Кажется список встреч пуст...'

async def show(user):
	tags = await get_tags(user[0])
	tags = '#'+' #'.join(tags) if tags else ''

	times = await get_times(user[0])
	times = ', '.join(times) if times else ''

	description = user[2] if user[2] else ''
	name = user[3]
	form = f'{name}\n-\n{description}\n🔑 {tags}\n{times}'
	return form

async def req_show(user,  time):
	tags = await get_tags(user[0])
	tags = '#'+' #'.join(tags) if tags else ''

	description = user[2] if user[2] else ''
	name = user[3]
	time = f'\n👤 {name} предлагает встретиться -> {time}' if time else ''
	form = f'{name}\n-\n{description}\n🔑 {tags}{time}'
	return form

#---------------------------------------------------------------------------------------

@dispatcher.message_handler(commands=['start'])
async def main_menu(message: types.Message):
	user = await get_user(message.chat.id)
	if user != 404:
		await message.answer('🛎 Главное меню', reply_markup=await mainMenu_ShowClient(message.chat.id))
	else:
		await message.answer_sticker('CAACAgQAAxkBAAIO6mNRPWqs_bZx80FOQJR47fu29F_7AAI-BgACFdzyAl2PqUPMZbELKgQ')
		await message.answer('Привет! Это демобот команды CoWorkWay!\n\nЯ помогу тебе познакомиться с твоими коллегами, а также найти интересного собеседника!')
		await message.answer('Создадим анкету?', reply_markup=MainMenu_Create_Inline.Keyboard)
		#await Registration.start.set()

#---------------------------------------------------------------------------------------

@dispatcher.callback_query_handler(text='btnCreate')
async def reg_start(message: types.Message, state: FSMContext):
	reply_markup = await echo_key((await state.get_data()).get('last_name'))
	await message.message.edit_text('🚀')
	await message.message.answer('Ваше имя?', reply_markup=reply_markup)

	await Registration.name.set()

@dispatcher.message_handler(state = Registration.name)
async def reg_name(message: types.Message, state: FSMContext):
	await state.update_data(name=message.text.strip())
	reply_markup = await echo_key((await state.get_data()).get('last_description'))
	await message.answer('Расскажи о себе. ("-" для пропуска)', reply_markup=reply_markup)

	await Registration.description.set()

@dispatcher.message_handler(state = Registration.description)
async def reg_description(message: types.Message, state: FSMContext):
	if message.text == '-': await state.update_data(description=None)
	else: await state.update_data(description=message.text.strip())
	reply_markup = await echo_key('-')
	await message.answer('Пришли своё фото.("-" для пропуска)', reply_markup=reply_markup)

	await Registration.photo.set() 

@dispatcher.message_handler(state = Registration.photo, content_types=['photo', 'text'])
async def reg_photo(message: types.Message, state: FSMContext):
	reply_markup = await echo_key('-')
	if message.text == '-': 
		await state.update_data(photo=None)
		await Registration.tags.set()
		await message.answer('Перечисли через запятую свои интересы в виде тегов:')
	elif message.photo: 
		await state.update_data(photo = message.photo[-1].file_id)
		await message.answer('Перечисли через запятую свои интересы в виде тегов:\nПример: работа, семья, спорт')
		await Registration.tags.set()
	else: await message.answer('Не обнаружил фотографию, попробуйте ещё раз. Для пропуска отправьте "-".',reply_markup=reply_markup)

@dispatcher.message_handler(state = Registration.tags)
async def reg_tags(message: types.Message, state: FSMContext):
	await state.update_data(tags=message.text.replace(',',' ').replace('.',' ').replace('#',' ').lower().split())
	reply_markup = await echo_key('-')
	await message.answer('В какое время, дату, часть дня тебе удобны встречи(через запятые)? ("-" для пропуска)', reply_markup=reply_markup)

	await Registration.times.set() 

@dispatcher.message_handler(state = Registration.times)
async def reg_times(message: types.Message, state: FSMContext):
	if message.text == '-': await state.update_data(times=[])
	else: await state.update_data(times=message.text.split(','))
	await state.update_data(telegram_id=message.from_id, telegram_tag=message.from_user.username)#
	curr_state = await state.get_data()
	if 'last_name' in curr_state: 
		del curr_state['last_name']
		del curr_state['last_description']

	if await create_user(**curr_state) == 0: await message.answer('📀 Успешно!')
	else: return await message.answer('Произошла какая-то ошибка...')

	await state.finish()
	await message.answer('🛎 Главное меню', reply_markup=await mainMenu_ShowClient(message.from_id))

#-------------------------------------------------------

@dispatcher.callback_query_handler(scoremarks_callback.filter())
async def score_seter(query: types.CallbackQuery, callback_data: dict):
	try:
		answer_data = callback_data.get('mark')
		await set_score(query.message.chat.id, answer_data)
		await query.message.edit_text('Спасибо за Ваш отзыв!')
		await main_menu(query.message)
	except Exception as ex:
		print('score_seter', ex)

@dispatcher.callback_query_handler(menu_callback.filter(menu='events'))
async def events_menu(query: types.CallbackQuery, callback_data: dict):
	try:
		await query.message.edit_text(text=events_menu_text, reply_markup=EventMarkup.Keyboard, parse_mode="HTML", disable_web_page_preview=True)
	except Exception as ex:
		print('events_menu', ex)

@dispatcher.callback_query_handler(menu_callback.filter(menu='show'))
async def show_menu(query: types.CallbackQuery, callback_data: dict):
	try:
		await query.message.edit_text(text='🔍')
		await update_tagname(query.message.chat.id, query.message.chat.username)
		await check_show(query.message, dispatcher.get_current().current_state())
	except Exception as ex:
		print('show_menu', ex)

@dispatcher.callback_query_handler(menu_callback.filter(menu='my_acc'))
async def my_acc_menu(query: types.CallbackQuery, callback_data: dict):
	try:
		user = await get_user(query.message.chat.id)
		if user!=404:
			my_acc_text = await show(user)
			if user[-1]:
				await query.message.delete()
				await query.message.answer_photo(caption=f'Ваша анкета:\n{my_acc_text}', photo=user[-1])
			else:
				await query.message.edit_text(text=f'Ваша анкета:\n{my_acc_text}')
		await main_menu(query.message)
	except Exception as ex:
		print('my_acc_menu', ex)

@dispatcher.callback_query_handler(menu_callback.filter(menu='new_acc'))
async def new_acc_menu(query: types.CallbackQuery, callback_data: dict):
	await query.message.answer(text='📖 Новая анкета')
	state = dispatcher.get_current().current_state()
	user = await get_user(query.message.chat.id)
	if user != 404:
		await state.update_data({
			'last_name':user[3],
			'last_description':user[2],
			})
		await reg_start(query, state)
	else:
		await reg_start(query, state)
	await delete_user(query.message.chat.id)

@dispatcher.callback_query_handler(menu_callback.filter(menu='score'))
async def score_menu(query: types.CallbackQuery, callback_data: dict):
	try:
		await query.message.edit_text(
			text='Насколько вам понравилась реализация прокета?',
			reply_markup = ScoreMarks.Keyboard
			)
	except Exception as ex:
		print('score_menu', ex)

@dispatcher.callback_query_handler(menu_callback.filter(menu='likes'))
async def last_likes(query: types.CallbackQuery, callback_data: dict):
	try:
		await query.message.edit_text(text=await show_likes(query.message.chat.id), parse_mode="HTML", disable_web_page_preview=True)
		await main_menu(query.message)
	except Exception as ex:
		print('last_likes', ex)

@dispatcher.callback_query_handler(menu_callback.filter(menu='check_requests'))
async def check_requests(query: types.CallbackQuery):
	try:
		req_user = (await get_requests(query.message.chat.id, all=False))
		if req_user:
			req_user_id = req_user[1]
			req_user_time = req_user[3]
			user = await get_user(req_user_id)
			meeting_id = req_user[0]
			return await query.message.edit_text(text=await req_show(user,req_user_time), reply_markup=await req_score(req_user_id, meeting_id))
		else:
			return await query.message.edit_text('🛎 Главное меню', reply_markup=await mainMenu_ShowClient(query.message.chat.id))
	except Exception as ex:
		print('check_requests', ex)

@dispatcher.callback_query_handler(menu_callback.filter(menu='event_exit'))
async def events_exit(query: types.CallbackQuery, callback_data: dict):
	return await query.message.edit_text('🛎 Главное меню', reply_markup=await mainMenu_ShowClient(query.message.chat.id))

#---------------------------------------------------------------------------------------

@dispatcher.callback_query_handler(req_callback.filter(answer='yes'))
async def req_yes_processing(query: types.CallbackQuery, callback_data: dict):
	try:
		meeting_id = callback_data.get('meeting_id')
		await update_tagname(query.message.chat.id, query.message.chat.username)
		if not await update_meeting(meeting_id=meeting_id, react=1):
			await check_requests(query)
	except Exception as ex:
		print('req_yes_processing', ex)

@dispatcher.callback_query_handler(req_callback.filter(answer='no'))
async def req_no_processing(query: types.CallbackQuery, callback_data: dict):
	try:
		meeting_id = callback_data.get('meeting_id')
		if not await update_meeting(meeting_id=meeting_id, react=2):
			await check_requests(query)
	except Exception as ex:
		print('req_no_processing', ex)

@dispatcher.callback_query_handler(req_callback.filter(answer='exit'))
async def req_exit_processing(query: types.CallbackQuery, callback_data: dict):
	try:
		#return await query.message.delete()
		return await query.message.edit_text('🛎 Главное меню', reply_markup=await mainMenu_ShowClient(query.message.chat.id))
	except Exception as ex:
		print('req_exit_processing', ex)

@dispatcher.callback_query_handler(text='btnGo_ckeck')
async def redirect_to_req(query: types.CallbackQuery):
	return await check_requests(query)

#---------------------------------------------------------------------------------------

@dispatcher.message_handler(state = Checker.show)
async def check_show(message: types.Message, state: FSMContext):
	user_for_check = await w2v_selection_advance(message.chat.id)
	if user_for_check:
		form = await show(user_for_check)
		if user_for_check[-1]:
			await message.answer_photo(caption=form, photo=user_for_check[-1], reply_markup=Score.Keyboard)
		else:
			await message.answer(text=form, reply_markup=Score.Keyboard)
		await state.update_data(user_for_check=user_for_check[0])

		await Checker.score.set()
	else:
		await state.finish()
		refresh = 'Анкеты закончились. Пересмотреть некоторые старые варианты?'
		if message.text == refresh:
			await message.answer('Больше нет подходящих анкет💤')
			return await message.answer('🛎 Главное меню', reply_markup=await mainMenu_ShowClient(message.chat.id))
		return await message.answer(refresh, reply_markup=RefreshConfirmInline.Keyboard)

@dispatcher.message_handler(state = Checker.score)
async def check_score(message: types.Message, state: FSMContext):
	to_id = (await state.get_data('user_for_check')).get('user_for_check')
	match message.text:
		case '🛑':
			await state.finish()
			await message.answer('🛎 Главное меню', reply_markup=await mainMenu_ShowClient(message.from_id))
		case '👍':
			times = await get_times(to_id)
			if times:
				await state.update_data(times=times)
				await message.answer('⏰ Выберите время для встречи:', reply_markup= await time_keyboard(times))

				await Checker.times.set()
			else:
				await message.answer(req_text)
				await set_meeting(message.from_id, to_id, 1)
				await set_request(message.from_id, to_id)
				await check_show(message, state)
		case '👎':
			await set_meeting(message.from_id, to_id, 2)

			await check_show(message, state)
		case _:
			await message.answer(no_answer, reply_markup=Score.Keyboard)

@dispatcher.message_handler(state = Checker.times)
async def check_times(message: types.Message, state: FSMContext):
	to_id = (await state.get_data('user_for_check')).get('user_for_check')
	times = (await state.get_data('times')).get('times')
	if message.text in times:
		await message.answer(req_text)
		await set_meeting(message.from_id, to_id, 1, message.text)
		await set_request(message.from_id, to_id, message.text)
		await check_show(message, state)
	elif message.text == skip_times_word:
		await message.answer(req_text)
		await set_meeting(message.from_id, to_id, 1)
		await set_request(message.from_id, to_id)
		await check_show(message, state)
	else:
		await message.answer(no_answer, reply_markup= await time_keyboard(times))

#---------------------------------------------------------------------------------------

@dispatcher.callback_query_handler(confirm_callback.filter())
async def refresh_confirm(query: types.CallbackQuery, callback_data: dict):
	answer_data = callback_data['answer']
	match answer_data:
		case 'yes':
			await refresh_meetings(query.message.chat.id)
			await query.message.edit_text('🔍')
			await check_show(query.message, dispatcher.get_current().current_state())
		case 'exit':
			await query.message.edit_text('🛎 Главное меню', reply_markup=await mainMenu_ShowClient(query.message.chat.id))

#---------------------------------------------------------------------------------------

@dispatcher.callback_query_handler(text='dashboard')
async def dashboard_menu(query: types.CallbackQuery):
	await query.message.answer('Экскурсия по вашей компании!\nКакиой отдел выберите?', reply_markup=DashBoardMenu.Keyboard)
	await query.message.delete()

@dispatcher.callback_query_handler(menu_callback.filter(menu='dashboard_exit'))
async def dashboard_exit(query: types.CallbackQuery, callback_data: dict):
	await query.message.delete()
	return await main_menu(query.message)

@dispatcher.callback_query_handler(menu_callback.filter(menu='dashboard_backend'))
async def dashboard_backend(query: types.CallbackQuery, callback_data: dict):
	await query.message.delete()
	await query.message.answer('Наши программисты:\n1...', reply_markup=DashBoardBlock.Keyboard)

@dispatcher.callback_query_handler(menu_callback.filter(menu='dashboard_adv'))
async def dashboard_adv(query: types.CallbackQuery, callback_data: dict):
	await query.message.delete()
	await query.message.answer('Наш маркетолог:\n...', reply_markup=DashBoardBlock.Keyboard)

@dispatcher.callback_query_handler(menu_callback.filter(menu='dashboard_manager'))
async def dashboard_manager(query: types.CallbackQuery, callback_data: dict):
	await query.message.delete()
	await query.message.answer('Наш менеджер:\n...', reply_markup=DashBoardBlock.Keyboard)

@dispatcher.callback_query_handler(menu_callback.filter(menu='dashboard_block_exit'))
async def dashboard_block_exit(query: types.CallbackQuery, callback_data: dict):
	await dashboard_menu(query)

#---------------------------------------------------------------------------------------

async def set_request(from_id, to_id, time=None):
	try:
		await bot.send_message(to_id,'📩 Кто-то хочет с Вами встретиться!')#, reply_markup=InlineMessageLiked.Keyboard)
	except Exception as ex:
		print('set_request', ex)

#---------------------------------------------------------------------------------------

@dispatcher.message_handler(content_types=['photo','text','sticker'])
async def default(message: types.Message):
	if not message.from_user.is_bot:
		await message.reply('🔌⚙️ Попробуйте: /start')

#---------------------------------------------------------------------------------------

if __name__ == '__main__':
	executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
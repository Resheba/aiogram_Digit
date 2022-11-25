from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from DataBase.db_api import check_score, get_requests

skip_times_word = 'Пропустить'

async def time_keyboard(times):
	Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)

	for time in times:
		Keyboard.insert(KeyboardButton(time))
	Keyboard.insert(KeyboardButton(skip_times_word))

	return Keyboard

class MainMenu_Create_Inline:
	button_create = InlineKeyboardButton(text = 'Создать🚀', callback_data='btnCreate')
	button_dashboard = InlineKeyboardButton(text='DashBoard', callback_data='dashboard')

	Keyboard = InlineKeyboardMarkup(one_time_keyboard=True).add(button_create,button_dashboard)

class InlineMessageLiked:
	button_go = InlineKeyboardButton(text='Смотреть!', callback_data='btnGo_ckeck')

	Keyboard = InlineKeyboardMarkup(one_time_keyboard=True).add(button_go)

class MainMenu_Create:
	button_create = KeyboardButton('Создать')

	Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(button_create)

menu_callback = CallbackData('block','menu')

async def echo_key(*keys):
	Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
	if keys[0]:
		for key in keys:
			Keyboard.insert(KeyboardButton(text=key))
		return Keyboard
	# if default:
	# 	Keyboard.insert(KeyboardButton(text=default))
	# 	return Keyboard
	return None

req_callback = CallbackData('req', 'answer','meeting_id')

async def req_score(telegram_id, meeting_id):
	button_like = InlineKeyboardButton(text = '📞 Ответить', callback_data=f'req:yes:{meeting_id}')
	button_skip = InlineKeyboardButton(text = '⏩ Пропустить', callback_data=f'req:no:{meeting_id}')
	button_exit = InlineKeyboardButton(text = 'Закрыть', callback_data=f'req:exit:{meeting_id}')

	Keyboard = InlineKeyboardMarkup(one_time_keyboard=True).add(button_like, button_exit, button_skip)
	return Keyboard

class EventMarkup:
	button_exit = InlineKeyboardButton(text = '🔙 Меню', callback_data='block:event_exit')

	Keyboard = InlineKeyboardMarkup(one_time_keyboard=True).add(button_exit)

async def mainMenu_ShowClient(telegram_id):
	button_events = InlineKeyboardButton(text='Events', callback_data='block:events')
	button_show = InlineKeyboardButton(text = 'Смотреть анкеты', callback_data='block:show')
	button_acc = InlineKeyboardButton(text = 'Моя анкета', callback_data='block:my_acc')
	button_rereg = InlineKeyboardButton(text = 'Новая анкета', callback_data='block:new_acc')
	button_likes = InlineKeyboardButton(text= 'Последние встречи', callback_data='block:likes')

	Keyboard = InlineKeyboardMarkup(one_time_keyboard=True).add(button_show, button_acc, button_rereg, button_events, button_likes)

	requests = await get_requests(telegram_id)
	if requests:
		Keyboard.insert(InlineKeyboardButton(text = f'Мои заявки({len(requests)})', callback_data='block:check_requests'))
	
	if not await check_score(telegram_id):
		Keyboard.add(InlineKeyboardButton(text = 'Оценить проект', callback_data='block:score'))
	return Keyboard

scoremarks_callback = CallbackData('score','mark')

class ScoreMarks:
	_1 = InlineKeyboardButton(text = '1', callback_data='score:1')
	_2 = InlineKeyboardButton(text = '2', callback_data='score:2')
	_3 = InlineKeyboardButton(text = '3', callback_data='score:3')
	_4 = InlineKeyboardButton(text = '4', callback_data='score:4')
	_5 = InlineKeyboardButton(text = '5', callback_data='score:5')

	Keyboard = InlineKeyboardMarkup(one_time_keyboard=True, row_width=5).add(_1,_2,_3,_4,_5)

class DashBoardMenu:
	button_exit = InlineKeyboardButton(text = '🔙 Выход', callback_data='block:dashboard_exit')
	button_manager = InlineKeyboardButton(text='Менеджер', callback_data='block:dashboard_manager')
	button_backend = InlineKeyboardButton(text='Программисты', callback_data='block:dashboard_backend')
	button_adv = InlineKeyboardButton(text='Маркетолог', callback_data='block:dashboard_adv')

	Keyboard = InlineKeyboardMarkup(one_time_keyboard=True, row_width=1).add(button_manager, button_adv, button_backend, button_exit)

class DashBoardBlock:
	button_exit = InlineKeyboardButton(text = '🔙 Назад', callback_data='block:dashboard_block_exit')

	Keyboard = InlineKeyboardMarkup().add(button_exit)

class MainMenu_Show:
	button_rereg = KeyboardButton('Новый аккаунт')
	button_show = KeyboardButton('Смотреть анкеты')
	button_acc = KeyboardButton('Моя анкета')
	button_refresh = KeyboardButton('Обновить анкеты')

	Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(button_rereg, button_acc, button_refresh, button_show)

class Score:
	button_like = KeyboardButton('👍')
	button_dis = KeyboardButton('👎')
	button_exit = KeyboardButton('🛑')

	Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(button_like, button_dis, button_exit)

class Pre_Show:
	button_show_all = KeyboardButton('all')
	button_show_diff = KeyboardButton('diff')
	button_show_api = KeyboardButton('api')
	button_show_w2v = KeyboardButton('w2v')
	button_like_w2v_advance = KeyboardButton('w2v_advance')

	Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(button_show_all, button_show_diff, button_show_api, button_show_w2v, button_like_w2v_advance)

class RefreshConfirm:
	button_yes = KeyboardButton('Да')
	button_exit = KeyboardButton('Выйти')

	Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(button_yes, button_exit)

confirm_callback = CallbackData('confirm','answer')

class RefreshConfirmInline:
	button_yes = InlineKeyboardButton(text = 'Да', callback_data='confirm:yes')
	button_exit = InlineKeyboardButton(text = 'Выйти', callback_data='confirm:exit')

	Keyboard = InlineKeyboardMarkup(one_time_keyboard=True).add(button_yes, button_exit)

method_callback = CallbackData('type','method')


class InlinePreShow:
	button_show_all = InlineKeyboardButton(text='all', callback_data='type:all')
	button_show_diff = InlineKeyboardButton(text='diff', callback_data='type:diff')
	button_show_api = InlineKeyboardButton(text='api', callback_data='type:api')
	button_show_w2v = InlineKeyboardButton(text='w2v', callback_data='type:w2v')
	button_like_w2v_advance = InlineKeyboardButton(text='w2v_advance', callback_data='type:w2v_advance')

	Keyboard = InlineKeyboardMarkup(one_time_keyboard=True).add(button_show_all, button_show_diff, button_show_api, button_show_w2v, button_like_w2v_advance)
from DataBase.db_api import get_user, get_tags, get_times, db_start, get_unscore_user, get_unscore_users, set_meeting
from DataBase.tags_diff import tags_lems_diff
from DataBase.w2v import similarity, model_start
from itertools import product
import requests, asyncio, aiohttp

K = 30

async def selection(telegram_id):
	result = await get_unscore_user(telegram_id)
	if result:
		result = await get_user(result)
		return result
	else:
		return result

async def lem_selection(telegram_id):
	from_ltags = await get_tags(telegram_id, 0, 1)
	async for id in get_unscore_users(telegram_id):
		to_ltags = await get_tags(id, 0, 1)
		k = await tags_lems_diff(from_ltags,to_ltags)
		if k > K:
			return await get_user(id)
		else:
			await set_meeting(telegram_id, id, 3)

#Есть путь с промежуточной f() или <gen>, которые стоят между генератором и view и заполняют state.data.

# async def rusvec_api(telegram_id):
# 	from_ltags = await get_tags(telegram_id, 0, 1)
# 	async for id in get_unscore_users(telegram_id):
# 		to_ltags = await get_tags(id, 0, 1)
# 		k = await sim_ratio(from_ltags, to_ltags)
# 		if k > K:
# 			return await get_user(id)

# async def sim_ratio(tag_list1, tag_list2):
# 	async with aiohttp.ClientSession() as session:
# 		k, count = 0, 0
# 		for comb in product(tag_list1,tag_list2):
# 			url = f'https://rusvectores.org/tayga_upos_skipgram_300_2_2019/{comb[0]}__{comb[1]}/api/similarity/'

# 			async with session.get(url) as req:
# 				if await req.text() != 'Unknown':
# 					response = int(float((await req.text()).split()[0])*100)
# 					k += response
# 					count += 1
					
# 		return k//count if count else 0

async def w2v_selection(telegram_id):
	from_ltags = await get_tags(telegram_id, 0, 1)
	async for id in get_unscore_users(telegram_id):
		to_ltags = await get_tags(id, 0, 1)
		k = await similarity(from_ltags, to_ltags)
		if k > K:
			return await get_user(id)
		else:
			await set_meeting(telegram_id, id, 3)

async def w2v_selection_advance(telegram_id):
	from_ltags = await get_tags(telegram_id, 0, 1)
	async for id in get_unscore_users(telegram_id):
		to_ltags = await get_tags(id, 0, 1)
		k = await similarity(from_ltags, to_ltags)
		if k == 0: return await lem_selection(telegram_id)
		if k > K: 
			return await get_user(id)
		else:
			await set_meeting(telegram_id, id, 3)

# asyncio.run(db_start())
# asyncio.run(model_start())
# asyncio.run(w2v_selection(1))
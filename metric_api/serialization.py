import sys, asyncio
sys.path.append('../')

from fastapi.encoders import jsonable_encoder
from DataBase.db_api import db_start, metrics_users_count, metrics_fact_meetings_count, metrics_all_meetings_count

async def dict_layout():
	users_count = (await metrics_users_count())[0]
	fact_meetings_count = (await metrics_fact_meetings_count())[0]
	all_meetings_count = (await metrics_all_meetings_count())[0]

	dict = {
	'users_count':users_count,
	'fact_meetings_count':fact_meetings_count,
	'all_meetings_count':all_meetings_count,
	}
	dict = jsonable_encoder(dict)
	return dict
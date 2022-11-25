import sqlite3 as sq
import asyncio, os, datetime
from .tags_lem import tags_lem_morph


async def db_start():
	global db, cur#, temp_id
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))+'\\DataBase\\'
	db = sq.connect(BASE_DIR+'db.db')
	cur = db.cursor()
	# temp_id = 1488

async def create_user(telegram_id, telegram_tag, name, description=None, age=None, spezial=None, photo=None, tags=[], times=[]):
	try:
		# global temp_id
		# telegram_id = temp_id
		# temp_id += 1
		cur.execute("INSERT INTO user VALUES(?,?,?,?,?,?,?)", (telegram_id, telegram_tag, description, name, age, spezial, photo))
		db.commit()

		tags_lems = await tags_lem_morph(tags)
		tags = dict(zip(tags,tags_lems))

		for tag, tag_lem in tags.items():
			cur.execute("INSERT INTO tags VALUES(?,?,?)", (telegram_id, tag, tag_lem))
			db.commit()

		for time in times:
			strip_time = time.strip()
			cur.execute("INSERT INTO times VALUES(?,?)", (telegram_id,strip_time))
			db.commit()
		return 0
	except Exception as ex:
		print("create_user",ex)
		return ex

async def delete_user(telegram_id):
	try:
		cur.execute("DELETE FROM user WHERE telegram_id='{telegram_id}'".format(telegram_id=telegram_id))
		db.commit()

		cur.execute("DELETE FROM meeting WHERE from_tg_id='{telegram_id}' OR to_tg_id = '{telegram_id}'".format(telegram_id=telegram_id))
		db.commit()

		cur.execute("DELETE FROM tags WHERE telegram_id='{telegram_id}'".format(telegram_id=telegram_id))
		db.commit()

		cur.execute("DELETE FROM times WHERE telegram_id='{telegram_id}'".format(telegram_id=telegram_id))
		db.commit()

		return 0
	except Exception as ex:
		print('delete_user', ex)
		return ex

async def refresh_meetings(telegram_id):
	'''В режиме DEBUG; Без режима DEBUG обавить в конец формулы  AND status != 1'''
	try:
		cur.execute("DELETE FROM meeting WHERE from_tg_id='{telegram_id}' AND status != 1".format(telegram_id=telegram_id))
		db.commit()

		return 0
	except Exception as ex:
		print('delete_meetings', ex)
		return ex

async def get_user(telegram_id):
	try:
		user = cur.execute("SELECT * FROM user WHERE telegram_id == '{telegram_id}'".format(telegram_id=telegram_id)).fetchone()
		if not user:
			return 404
		return user
	except Exception as ex:
		print('get_user',ex)
		return ex

async def get_tags(telegram_id, tag=True,tag_lem=False):
	try:
		com = ',' if tag and tag_lem else ''
		tag = 'tag' if tag else ''
		tag_lem = 'tag_lem' if tag_lem else ''
		tags = cur.execute("SELECT {tag}{com}{tag_lem} FROM tags WHERE telegram_id == '{telegram_id}'".format(com=com,telegram_id=telegram_id,tag=tag,tag_lem=tag_lem)).fetchall()
		tags = dict(tags) if com else tags

		if not com: tags = [str(tag[0]) for tag in tags]

		return tags
	except Exception as ex:
		print('get_tags',ex)
		return ex

async def get_times(telegram_id):
	try:
		times = cur.execute("SELECT time FROM times WHERE telegram_id = '{telegram_id}'".format(telegram_id=telegram_id)).fetchall()
		times = [str(time[0]) for time in times]
		return times
	except Exception as ex:
		print('get_times',ex)
		return ex

async def get_unscore_user(telegram_id):
	try:
		unscore_user = cur.execute("""SELECT telegram_id
		FROM user LEFT JOIN (SELECT * FROM meeting WHERE from_tg_id='{telegram_id}' OR to_tg_id = '{telegram_id}') 
		ON (from_tg_id=telegram_id OR to_tg_id=telegram_id)
		WHERE from_tg_id IS NULL AND telegram_id != '{telegram_id}'""".format(telegram_id=telegram_id)).fetchone()

		unscore_user = unscore_user[0] if unscore_user else unscore_user

		return unscore_user
	except Exception as ex:
		print('get_unscore_user',ex)
		return ex

async def get_unscore_users(telegram_id):
	try:
		unscore_users = cur.execute("""SELECT telegram_id
		FROM user LEFT JOIN (SELECT * FROM meeting WHERE from_tg_id='{telegram_id}' OR to_tg_id = '{telegram_id}') 
		ON (from_tg_id=telegram_id OR to_tg_id=telegram_id)
		WHERE from_tg_id IS NULL AND telegram_id != '{telegram_id}'""".format(telegram_id=telegram_id)).fetchall()

		if unscore_users:
			for uid in unscore_users: yield uid[0]
			#unscore_users = (yield uid[0] for uid in unscore_users)
		#else: return None

		#return unscore_users
	except Exception as ex:
		print('get_unscore_users',ex)
		#return ex

async def set_meeting(from_id, to_id, status, time = None, react = 0, date=datetime.datetime.now().date()):
	'''Status-codes:
	1 - Like; 2 - Dislike; 3 - Algoritm
	   React-codes:
	0 - Unreacted; 1 - ReactLike; 2 - ReactDislike'''
	try:
		cur.execute("INSERT INTO meeting VALUES(?,?,?,?,?,?,?)", (None, from_id, to_id, time, status, react, date))
		db.commit()

		return 0
	except Exception as ex:
		print('set_meeting',ex)
		return ex

async def check_score(telegram_id):
	try:
		score_user = cur.execute("SELECT telegram_id FROM product_score WHERE telegram_id = '{telegram_id}'".format(telegram_id=telegram_id)).fetchone()
		if score_user:
			return 1
		return 0
	except Exception as ex:
		print('check_score',ex)

async def set_score(telegram_id, score):
	try:
		cur.execute("INSERT INTO product_score VALUES(?,?)", (telegram_id, score))
		db.commit()

		return 0
	except Exception as ex:
		print('set_meeting',ex)
		return ex

async def get_likes(telegram_id, limit=10):
	try:
		likes_users = cur.execute("""SELECT * FROM meeting 
			WHERE (from_tg_id = '{telegram_id}' OR to_tg_id = '{telegram_id}') AND status = 1 AND react = 1
			ORDER BY date DESC 
			LIMIT '{limit}';""".format(telegram_id=telegram_id, limit=limit)).fetchall()
		likes_users = [like for like in likes_users]

		return likes_users
	except Exception as ex:
		print('get_likes',ex)
		return ex

async def get_requests(telegram_id, all=True):
	try:
		requests = cur.execute("""SELECT * FROM meeting 
			WHERE (to_tg_id = '{telegram_id}') AND status = 1 AND react = 0
			ORDER BY date;""".format(telegram_id=telegram_id))
		if all:
			return requests.fetchall()

		return requests.fetchone()
	except Exception as ex:
		print('get_requests',ex)
		return ex

async def update_meeting(meeting_id, time=None, status=None, react=None, date=datetime.datetime.now().date()):
	try:
		"""Меняется только одно значение."""
		#time = f'time = {time}' if time else ''
		#status = f'status = {status}' if status else ''
		cur.execute("""UPDATE meeting SET react='{react}',date='{date}' WHERE id='{meeting_id}';""".format(react=react, date=date, meeting_id=meeting_id))
		db.commit()

		return 0
	except Exception as ex:
		print('update_meeting',ex)
		return ex

async def update_tagname(telegram_id, telegram_tag):
	try:
		cur.execute("""UPDATE user SET telegram_tag='{telegram_tag}' WHERE telegram_id='{telegram_id}';""".format(telegram_tag=telegram_tag, telegram_id=telegram_id))
		db.commit()

		return 0
	except Exception as ex:
		print('update_meeting',ex)
		return ex

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

async def metrics_users_count():
	try:
		users_count = cur.execute("SELECT COUNT(telegram_id) FROM user").fetchone()
		return users_count
	except Exception as ex:
		print('metrics_users_count')
		return ex

async def metrics_fact_meetings_count():
	try:
		meetings_count = cur.execute("SELECT COUNT(id) FROM meeting WHERE react=1").fetchone()
		return meetings_count
	except Exception as ex:
		print('metrics_fact_meetings_count')
		return ex

async def metrics_all_meetings_count():
	try:
		meetings_count = cur.execute("SELECT COUNT(id) FROM meeting WHERE status=1").fetchone()
		return meetings_count
	except Exception as ex:
		print('metrics_all_meetings_count')
		return ex
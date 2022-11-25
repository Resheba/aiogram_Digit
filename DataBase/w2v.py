from gensim.models import KeyedVectors
import os, asyncio



async def model_start():
	try:
		global model, keys
		BASE_DIR = os.path.dirname(os.path.dirname(__file__))+'\\DataBase\\models\\'
		model_type = 'model_186.bin'
		model = KeyedVectors.load_word2vec_format(BASE_DIR+model_type, binary=True)
		keys = set(model.key_to_index.keys())
		print(f'[INFO] {model_type} has been loaded successfully.')
	except Exception as ex:
		print('model_start', ex)

async def vocab_search(word):
	global keys
	for key in keys:
		if word == key.split('_')[0]:
			return key
	return None

async def similarity(ltg1, ltg2):
	try:
		voc_tg1 = set()
		voc_tg2 = set()

		for tag in ltg1:
			voc_tag = await vocab_search(tag)
			match voc_tag:
				case None: continue
				case _: voc_tg1.add(voc_tag)

		for tag in ltg2:
			voc_tag = await vocab_search(tag)
			match voc_tag:
				case None: continue
				case _: voc_tg2.add(voc_tag)
		result = model.n_similarity(voc_tg1, voc_tg2)
		result *= 100
		return int(result)
	except:
		return 0
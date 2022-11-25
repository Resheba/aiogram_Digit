from pymystem3 import Mystem
import pymorphy2
from string import punctuation
punctuation+='\n'

async def tags_lem_morph(tags):
	morph = pymorphy2.MorphAnalyzer()
	tags = list(' '.join(tags))
	tags = ''.join([i for i in tags if i not in punctuation]).split()
	tags = [morph.parse(word)[0].normal_form.replace('ё','e') for word in tags]
	return tags



async def tags_lem_stem(tags):
	tags = Mystem().lemmatize(' '.join(tags))
	tags = [s for s in tags if s not in punctuation+' ']
	return tags

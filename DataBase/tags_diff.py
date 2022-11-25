from fuzzywuzzy import fuzz

async def tags_lems_diff(lem_tags1, lem_tags2):
	diff = fuzz.token_sort_ratio(lem_tags1, lem_tags2)
	return diff
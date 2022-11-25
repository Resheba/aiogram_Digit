from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
	start = State()
	name = State()
	description = State()
	tags = State()
	times = State()
	photo = State()

class Checker(StatesGroup):
	pre_choose = State()
	show = State()
	score = State()
	times = State()

class AuthMenu(StatesGroup):
	menu = State()

class Refresh(StatesGroup):
	confirm = State()
from aiogram.fsm.state import StatesGroup, State

class Add(StatesGroup):
    add_descr = State()
    add_name = State()

class Choose(StatesGroup):
    choose_category = State()
    choose_item = State()

class Waiting(StatesGroup):
    ignore = State()

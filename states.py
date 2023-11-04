from aiogram.fsm.state import StatesGroup, State


class Add(StatesGroup):
    waiting_to_add_descr = State()
    waiting_to_add_name = State()


class Choose(StatesGroup):
    waiting_to_choose_category = State()
    waiting_to_choose_action = State()
    waiting_to_choose_item = State()


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

menu = [
    [InlineKeyboardButton(text="Выбрать категорию", callback_data="choose_category"),
    InlineKeyboardButton(text="Посмотреть все товары", callback_data="show_all")],
    [InlineKeyboardButton(text="Дата следующей гаражки", callback_data="next_date")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])


def build_kb(d: dict):
    builder = InlineKeyboardBuilder()
    for key in d.keys():
        print(d.get(key))
        builder.add(InlineKeyboardButton(text=str(d.get(key)), callback_data=str(key)))
        print(d.get(key))
    builder.adjust(2)
    return builder.as_markup()


def build_item_kb(position, rel_pos = None): #previous and next items + add to cart
    left_button = InlineKeyboardButton(text="◀", callback_data=f"{position - 1}")
    middle_button = InlineKeyboardButton(text="Хочу посмотреть на месте!", callback_data=f"{position}") # search for dynamic states
    right_button = InlineKeyboardButton(text="▶", callback_data=f"{position + 1}")
    if rel_pos == "first":
        buttons = [middle_button, right_button]
    elif rel_pos == "last":
        buttons = [left_button, middle_button]
    else:
        buttons = [left_button, middle_button, right_button]
    return InlineKeyboardMarkup(buttons)



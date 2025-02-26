from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from logger import logger

import callbacks

menu_buttons = [
    [InlineKeyboardButton(text="Выбрать категорию", callback_data="choose_category"),
    InlineKeyboardButton(text="Посмотреть все товары", callback_data="show_all")],
    [InlineKeyboardButton(text="Дата следующей гаражки", callback_data="next_date")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu_buttons)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])


def build_categories_kb(d: dict):
    builder = InlineKeyboardBuilder()
    for key in d.keys():
        builder.button(
            text=str(d.get(key)),
            callback_data=callbacks.CategoriesCallbackFactory(key=key))
    builder.adjust(2)
    return builder.as_markup()


def build_item_kb(position: int, is_last=False):
    builder = InlineKeyboardBuilder()
    left_button = InlineKeyboardButton(text="◀", callback_data=callbacks.ItemIterCallbackFactory(key=position-1).pack())
    middle_button = InlineKeyboardButton(text="Хочу посмотреть на месте!", callback_data=callbacks.ItemChosenCallbackFactory(key=position).pack()) # search for dynamic states
    right_button = InlineKeyboardButton(text="▶", callback_data=callbacks.ItemIterCallbackFactory(key=position+1).pack())
    if position == 0:
        builder.add(
            middle_button,
            right_button
        )
        builder.adjust(2)
    elif is_last:
        builder.add(
            left_button,
            middle_button
        )
        builder.adjust(2)
    else:
        builder.add(
            left_button,
            middle_button,
            right_button
        )
        builder.adjust(3)
    return builder.as_markup()



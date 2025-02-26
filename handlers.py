import logging
from logger import logger

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import Keyboards
import text
from utils import build_media_group
from aiogram import flags

from Models import Category, Clothing, Filters
import states
from callbacks import *

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await state.set_state(states.Choose.waiting_to_choose_action.state)
    await msg.answer(text.greet.format(name=msg.from_user.username), reply_markup=Keyboards.menu)
    logger.debug("Bot started")


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=Keyboards.menu)


@router.callback_query(F.data == "choose_category")
async def show_categories(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(states.Choose.waiting_to_choose_category)
    categories = {}
    try:
        query = Category.select()
    except Exception as inst:
        logger.error(f"{type(inst)} at show_categories()")

    for cat in query:
        categories[cat.category_id] = cat.category_name
    await clbck.message.answer(text.category_select, reply_markup=Keyboards.build_categories_kb(categories))
    logger.debug("Category list was sent at show_categories()")


@router.callback_query(CategoriesCallbackFactory.filter())
async def show_items_in_categories(clbck: CallbackQuery,
                                   callback_data: CategoriesCallbackFactory,
                                   state: FSMContext):
    logger.debug("show_items_in_categories")
    await state.set_state(states.Choose.waiting_to_choose_item)
    try:
        Filters.replace({Filters.user_id: clbck.from_user.id, Filters.category_key: callback_data.key}).execute()
        logger.debug(f"Filters data updated with catkey | {clbck.from_user.id, callback_data.key}")
    except Exception as inst:
        logger.error(f"{type(inst)} at updating filters")
    await show_item(0, clbck)


async def show_item(position: int, clbck: CallbackQuery):
    pref: Filters
    try:
        pref = (Filters.select()
                .where(Filters.user_id == clbck.from_user.id)
                .get())
    except Exception as inst:
        logger.error(f"{type(inst)} at retrieving filters: {inst}")
    try:
        logger.debug(f"Preferences: {pref.user_id, pref.category_key}")
        query = (Clothing.select()
                 .where((Clothing.category == pref.category_key) &
                        (Clothing.status == 1))
                 .order_by(Clothing.name)
                 )  # учесть статусы в будущем
        if query.exists():
            item: Clothing = query[position]
            logger.debug(f"Item {item.name} | {item.description} retrieved")
            media = build_media_group(item.GetImagePaths())
            logger.debug(f"Media built: {len(media)}")
            await clbck.message.answer_photo(photo=media[0],
                                             caption=f"{item.name}\n{item.description}\n{str(item.price)}",
                                             reply_markup=Keyboards.build_item_kb(position))
        else:
            await clbck.message.answer(text.not_found, reply_markup=Keyboards.menu)
            logger.debug("No matching rows")

    except Exception as inst:
        logger.error(f"{type(inst)} at show_item(): {inst}")


@router.callback_query()
async def default(clbck: CallbackQuery):
    await clbck.message.answer(clbck.message.text)

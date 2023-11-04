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

from Models import Category, Clothing
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
    await state.update_data({str(clbck.from_user.id): {'category_key': callback_data.key}})
    logging.debug("State data updated with catkey")

    await show_item(1, clbck.from_user.id, clbck)


async def show_item(position: int, user_id: int, clbck: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()['users_picks'][user_id]
    try:
        query = (Clothing.select()
                 .where(int(Clothing.category) == user_data['category_key'] and Clothing.status == 1)
                 .order_by(Clothing.name)
                 )  # учесть статусы в будущем
    except Exception as inst:
        logger.error(f"{type(inst)} at show_item()")
    if query.exists():
        item: Clothing = query[position]
        logger.debug(f"Item {item.name} retrieved")
        media = build_media_group(item.GetImagePaths())
        await clbck.message.answer_media_group(media=media,
                                           caption=item.name + '\n'
                                                   + item.description + '\n'
                                                   + str(item.price),
                                           reply_markup=Keyboards.build_item_kb())
    else:
        await clbck.message.answer(text.not_found, reply_markup=Keyboards.menu)


@router.callback_query()
async def default(clbck: CallbackQuery):
    await clbck.message.answer(clbck.message.text)

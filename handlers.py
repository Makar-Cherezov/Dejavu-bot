from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import Keyboards
import text
from aiogram import flags
from aiogram.fsm.context import FSMContext
from Models import Category, Clothing
from states import Add, Waiting, Choose

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await state.set_state(Waiting.ignore)
    await msg.answer(text.greet.format(name=msg.from_user.username), reply_markup=Keyboards.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=Keyboards.menu)


@router.callback_query(F.data == "choose_category")
async def show_categories(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Choose.choose_category)
    categories = {}
    query = Category.select()
    for cat in query:
        categories[cat.category_id] = cat.category_name
    await clbck.message.answer(text.category_select, reply_markup=Keyboards.build_kb(categories))


@router.message(Choose.choose_category)
async def show_item_in_category(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Choose.choose_item)
    key = clbck.data
    query = (Clothing.select()
             .where(str(Clothing.category) == key and Clothing.status == 1)
             .order_by(Clothing.name))  # учесть статусы в будущем
    position = 0
    item: Clothing = query.offset(position).limit(1).get()
    image_paths = item.GetImagePaths()
    images = types.MediaGroup()
    for path in image_paths:
        images.attach_photo(types.InputFile(path))
    name = item.name
    description = item.description
    price = str(item.price)
    await clbck.message.answer_media_group(media=images,
                                           caption=name + '\n' + description + '\n' + price,
                                           reply_markup=Keyboards.build_item_kb())

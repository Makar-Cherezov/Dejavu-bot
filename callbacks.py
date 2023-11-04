from aiogram.filters.callback_data import CallbackData


class CategoriesCallbackFactory(CallbackData, prefix="catkey"):
    key: int
    df: str


class ItemIterCallbackFactory(CallbackData, prefix="itemkey"):
    key: int



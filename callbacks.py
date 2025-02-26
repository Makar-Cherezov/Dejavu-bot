from aiogram.filters.callback_data import CallbackData


class CategoriesCallbackFactory(CallbackData, prefix="catkey"):
    key: int


class ItemIterCallbackFactory(CallbackData, prefix="itemkey"):
    key: int

class ItemChosenCallbackFactory(CallbackData, prefix="itemchosen"):
    key: int


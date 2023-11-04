from Models import Clothing
from aiogram import types


def build_media_group(file_paths: list):
    images = types.MediaGroup()
    for path in file_paths:
        images.attach_photo(types.InputFile(path))
    return images


class SingleUserFilter:
    user_id: int
    category_key: int

    def __init__(self, userid, categorykey):
        self.user_id = userid
        self.category_key = categorykey


class UsersFiltersList:
    info: list[SingleUserFilter]


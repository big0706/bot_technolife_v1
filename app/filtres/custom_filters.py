from aiogram.types import Message
from aiogram.filters import BaseFilter

import app.database.requests as requests


class isAdmin(BaseFilter):

    def __init__(self) -> None:
        self.stuff_id = []

    async def __call__(self, message: Message) -> bool:
        self.stuff_id = await requests.get_admins_id()
        return message.from_user.id in self.stuff_id


class isManager(BaseFilter):

    def __init__(self) -> None:
        self.stuff_id = []

    async def __call__(self, message: Message) -> bool:
        self.stuff_id = await requests.get_manager_id()
        return message.from_user.id in self.stuff_id


class isStuff(BaseFilter):

    def __init__(self) -> None:
        self.stuff_id = []

    async def __call__(self, message: Message) -> bool:
        self.stuff_id = await requests.get_stuff_id()
        return message.from_user.id in self.stuff_id

from app.database.models import (async_session, Product, User, Category, Role)
from sqlalchemy import select, func, update


async def set_user(telegram_id: int, username: str):
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        if not user:
            session.add(User(telegram_id=telegram_id, username=username))
            await session.commit()


async def set_role(telegram_id: int, role: str):
    async with async_session() as session:
        stmt = update(User).where(User.telegram_id == telegram_id).values(role=role)
        await session.execute(stmt)
        await session.commit()


async def set_employ(telegram_id: int, first_name: str, last_name: str, phone: str):
    async with async_session() as session:
        stmt = update(User).where(User.telegram_id == telegram_id).values(first_name=first_name, last_name=last_name,
                                                                          phone=phone, role=Role.SELLER.value)
        await session.execute(stmt)
        await session.commit()


async def get_categories() -> list[Category]:
    async with async_session() as session:
        return await session.scalars(select(Category).order_by(Category.name))


async def get_category_by_id(category_id) -> Category:
    async with async_session() as session:
        return await session.scalar(select(Category).where(Category.id == category_id).order_by(Category.name))


async def get_products_by_category(category_name: str) -> list[Product]:
    async with async_session() as session:
        return await session.scalars(select(Product).where(Product.category == category_name).order_by(Product.name))


async def get_products_by_search(name: str) -> list[Product]:
    async with async_session() as session:
        return await session.scalars(select(Product).where(func.lower(Product.name).like(f'%{str.lower(name)}%')))


async def get_product_by_id(item_id: int) -> Product:
    async with async_session() as session:
        return await session.scalar(select(Product).where(Product.id == item_id))


async def get_user_by_id(telegram_id: int) -> User:
    async with async_session() as session:
        return await session.scalar(select(User).where(User.telegram_id == telegram_id))


async def get_users() -> list[User]:
    async with async_session() as session:
        return await session.scalars(select(User).where(User.role == Role.GUEST.value).order_by(User.username))


async def get_employs() -> list[User]:
    async with async_session() as session:
        return await session.scalars(select(User).where(User.role.in_([Role.ADMIN.value, Role.MANAGER.value,
                                                                       Role.SELLER.value])))


async def get_admins_id() -> list[int]:
    async with async_session() as session:
        users: list[User] = await session.scalars(select(User).where(User.role == Role.ADMIN.value))
        list_id = []
        for u in users:
            list_id.append(u.telegram_id)
        return list_id


async def get_manager_id() -> list[int]:
    async with async_session() as session:
        users: list[User] = await session.scalars(select(User).where(User.role == Role.MANAGER.value))
        list_id = []
        for u in users:
            list_id.append(u.telegram_id)
        return list_id


async def get_stuff_id() -> list[int]:
    async with async_session() as session:
        users: list[User] = await session.scalars(select(User).where(User.role.in_(
                                                        [Role.ADMIN.value, Role.MANAGER.value, Role.SELLER.value])))
        list_id = []
        for u in users:
            list_id.append(u.telegram_id)
        return list_id


async def is_guest(user_id: int) -> bool:
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.telegram_id == user_id))
        return user is None


async def is_admin(user_id: int) -> bool:
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.telegram_id == user_id))
        return Role.ADMIN.value in user.role


async def is_manager(user_id: int) -> bool:
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.telegram_id == user_id))
        return Role.MANAGER.value == user.role

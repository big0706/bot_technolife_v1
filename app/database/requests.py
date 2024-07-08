from app.models.roles_enum import RoleEnum
from app.models.models import (async_session, Product, Employee, Category, User)
from sqlalchemy import select, func, update, delete


# Setter
async def set_user(telegram_id: int, username: str):
    async with async_session() as session:
        user: Employee = await session.scalar(select(Employee).where(Employee.telegram_id == telegram_id))
        if not user:
            session.add(User(telegram_id=telegram_id, username=username))
            await session.commit()


async def set_role(telegram_id: int, role: str):
    async with async_session() as session:
        stmt = update(Employee).where(Employee.telegram_id == telegram_id).values(role=role)
        await session.execute(stmt)
        await session.commit()


async def set_employee(telegram_id: int, username: str, name: str, surname: str, phone: str):
    async with async_session() as session:
        session.add(Employee(telegram_id=telegram_id, username=username, name=name, surname=surname, phone=phone,
                             role=RoleEnum.SELLER.value))
        await session.commit()


async def update_employee(telegram_id: int, name: str, surname: str, phone: str, role: str):
    async with async_session() as session:
        stmt = update(Employee).where(Employee.telegram_id == telegram_id).values(name=name, surname=surname,
                                                                                  phone=phone, role=role)
        await session.execute(stmt)
        await session.commit()


async def delete_user(telegram_id: int) -> None:
    async with async_session() as session:
        stmt = delete(User).where(User.telegram_id == telegram_id)
        await session.execute(stmt)
        await session.commit()


# Category
async def get_categories() -> list[Category]:
    async with async_session() as session:
        return await session.scalars(select(Category).order_by(Category.name))


async def get_category_by_id(category_id) -> Category:
    async with async_session() as session:
        return await session.scalar(select(Category).where(Category.id == category_id).order_by(Category.name))


# Product
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


# User
async def get_employee_by_id(telegram_id: int) -> Employee:
    async with async_session() as session:
        return await session.scalar(select(Employee).where(Employee.telegram_id == telegram_id))


async def get_users() -> list[User]:
    async with async_session() as session:
        return await session.scalars(select(User).order_by(User.username))


async def get_employees() -> list[Employee]:
    async with async_session() as session:
        return await session.scalars(select(Employee).where(Employee.role.in_(
            [RoleEnum.ADMIN.value,
             RoleEnum.MANAGER.value,
             RoleEnum.SELLER.value])))


async def get_admins_id() -> list[int]:
    async with async_session() as session:
        users: list[Employee] = await session.scalars(select(Employee).where(Employee.role == RoleEnum.ADMIN.value))
        list_id = []
        for u in users:
            list_id.append(u.telegram_id)
        return list_id


async def get_manager_id() -> list[int]:
    async with async_session() as session:
        users: list[Employee] = await session.scalars(select(Employee).where(Employee.role.in_(
            [RoleEnum.ADMIN.value,
             RoleEnum.MANAGER.value])))
        list_id = []
        for u in users:
            list_id.append(u.telegram_id)
        return list_id


async def get_stuff_id() -> list[int]:
    async with async_session() as session:
        users: list[Employee] = await session.scalars(select(Employee).where(Employee.role.in_(
            [RoleEnum.ADMIN.value,
             RoleEnum.MANAGER.value,
             RoleEnum.SELLER.value])))
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
        user: Employee = await session.scalar(select(Employee).where(Employee.telegram_id == user_id))
        if user is None:
            return False
        return RoleEnum.ADMIN.value in user.role


async def is_manager(user_id: int) -> bool:
    async with async_session() as session:
        user: Employee = await session.scalar(select(Employee).where(Employee.telegram_id == user_id))
        return RoleEnum.MANAGER.value == user.role

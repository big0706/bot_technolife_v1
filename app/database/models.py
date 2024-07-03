import os
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv
from enum import Enum

load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))

async_session = async_sessionmaker(engine)


class Role(Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    SELLER = 'seller'
    GUEST = 'guest'


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=True)
    last_name: Mapped[str] = mapped_column(String(120), nullable=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=True)
    role: Mapped[str] = mapped_column(String(15), ForeignKey('roles.name'), insert_default=Role.GUEST.value)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)


class Product(Base):
    __tablename__ = "product_catalog"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column(ForeignKey('categories.name'))
    balance: Mapped[int] = mapped_column()
    purchase_price: Mapped[int] = mapped_column()
    cash_price: Mapped[int] = mapped_column()
    credit_price: Mapped[int] = mapped_column()


class Roles(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(), unique=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

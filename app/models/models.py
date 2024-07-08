from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from app.config_dt.config import Config, load_config

config: Config = load_config()

engine = create_async_engine(url=config.db.database_url)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=True)


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(120), nullable=True)
    surname: Mapped[str] = mapped_column(String(120), nullable=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=True)
    role: Mapped[str] = mapped_column(String(15), ForeignKey('roles.name'))
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

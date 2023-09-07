from decimal import Decimal

from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Category(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(primary_key=True)


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    price: Mapped[Decimal] = mapped_column(DECIMAL(scale=2))
    category: Mapped[str] = mapped_column(ForeignKey('categories.name'))


class Photo(Base):
    __tablename__ = 'photos'

    photo_id: Mapped[str] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))

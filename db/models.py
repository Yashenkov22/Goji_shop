from sqlalchemy import Column, DECIMAL, ForeignKey, String, Integer, MetaData, Table

from .base import Base

metadata = MetaData()


categories = Table(
    'categories',
    metadata,
    Column('name', String, primary_key=True),
) 


items = Table(
    'items',
    metadata,
    Column('id',Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('price', DECIMAL(2, 2)),
    Column('category', String, ForeignKey('categories.name')),
)


photos = Table(
    'photos',
    metadata,
    Column('photo_id', String, primary_key=True),
    Column('item_id', Integer, ForeignKey('items.id')),
)


# sizes = Table(
#     'sizes',
#     metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('size', String, unique=True),
# )

# ItemSize = Table(
#     'item_sizes',
#     metadata,
#     Column('id', primary_key=True, autoincrement=True),
#     Column('item_id', Integer, ForeignKey('item.id')),
#     Column('size_id', Integer, ForeignKey('size.id')),
# )
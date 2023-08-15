from sqlalchemy import Column, DECIMAL, ForeignKey, String, Integer, MetaData, Table


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
    Column('photo_id', Integer, primary_key=True),
    Column('item_id',Integer, ForeignKey('items.id')),
)

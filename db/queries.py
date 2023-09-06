from typing import Any

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select, insert, update, delete
from db.models import categories, items, photos


def add_category(session: Session, data: dict[str,str]):
    with session.begin():
        session.execute(insert(categories).values(name=data['name']))


def add_item(session: Session, data: dict):
    with session.begin():
        session.execute(insert(items).values(category=data['category'],
                                             name=data['name'],
                                             price=data['price']))
        
        
def get_all_categories(session: Session):
    with session.begin():
        return session.execute(select(categories)).all()


def get_items_for_current_category(category: str, session: Session):
    with session.begin():
        return session.execute(select(items).where(items.c.category == category)).all()


def delete_item(session: Session, data: dict[str, Any]):
    with session.begin():
        session.execute(delete(photos).where(photos.c.item_id == data['item_id']))
        session.execute(delete(items).where(items.c.id == data['item_id']))


def select_current_item(session: Session, name: str):
    with session.begin():
        return session.execute(select(items).where(items.c.name == name)).fetchone()


def update_item(session: Session, data: dict[str, Any]):
    with session.begin():
        session.execute(update(items).where(items.c.id == data['id']).values(name=data['name'],
                                                                             price=data['price']))


def insert_photo(session: Session, data: dict[str, str]):
    photo_ids = data['photos']
    with session.begin():
        for photo_id in photo_ids:
            session.execute(insert(photos).values(item_id=data['item_id'], photo_id=photo_id))


def select_photos_for_item(session: Session, item_id: int):
    with session.begin():
        return session.execute(select(photos.c.photo_id).where(photos.c.item_id == item_id)).fetchall()


# async def insert_sizes_before_start(session: sessionmaker):
#     SIZES = ('XS', 'S', 'M', 'L', 'XL', 'XXL')
#     with session() as session:
#         session: Session
#         with session.begin():
#             for size in SIZES:
#                 session.execute(insert(sizes).values(size=size))
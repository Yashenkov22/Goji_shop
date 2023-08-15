from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from db.models import categories, items


def add_category(session: Session, data: dict[str,str]):
    with session.begin():
        session.execute(insert(categories).values(name=data['name']))


def add_item(session: Session, data: dict):
    with session.begin():
        session.execute(insert(items).values(category=data['category'],
                                             name=data['name'],
                                             price=data['price']))
        
        
def get_all_categories(session:Session):
    return session.execute(select(categories)).all()


def get_items_for_current_category(category: str, session: Session):
    return session.execute(select(items).where(items.c.category == category)).all()


def delete_item(session: Session, data: dict[str, str]):
    with session.begin():
        session.execute(delete(items).where(items.c.name == data['name']))


def select_current_item(session: Session, name: str):
    return session.execute(select(items).where(items.c.name == name)).fetchone()


def update_item(session: Session, data: dict[str, Any]):
    with session.begin():
        session.execute(update(items).where(items.c.id == data['id']).values(name=data['name'],
                                                                             price=data['price']))
        
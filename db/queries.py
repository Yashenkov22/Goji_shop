from sqlalchemy.orm import Session
from sqlalchemy import select, insert
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
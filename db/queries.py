from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from db.models import Category, Item, Photo


async def add_category(session: AsyncSession, data: dict[str,str]):
    async with session.begin():
        await session.execute(insert(Category).values(name=data['name']))


async def add_item(session: AsyncSession, data: dict):
    async with session.begin():
        await session.execute(insert(Item).values(category=data['category'],
                                             name=data['name'],
                                             price=data['price']))
        
        
async def get_all_categories(session: AsyncSession):
    async with session.begin():
        result = await session.execute(select(Category.name))
        return result.all()


async def get_items_for_current_category(category: str, session: AsyncSession):
    async with session.begin():
        result = await session.execute(select(Item).where(Item.category == category))
        return result.all()


async def delete_item(session: AsyncSession, item_id: int):
    async with session.begin():
        await session.execute(delete(Photo).where(Photo.item_id == item_id))
        await session.execute(delete(Item).where(Item.id == item_id))


async def select_current_item(session: AsyncSession, name: str):
    async with session.begin():
        result = await session.execute(select(Item).where(Item.name == name))
        return result.fetchone()


async def update_item(session: AsyncSession, data: dict[str, Any]):
    async with session.begin():
        await session.execute(update(Item).where(Item.id == data['id']).values(name=data['name'],
                                                                             price=data['price']))


async def insert_photo(session: AsyncSession, data: dict[str, str]):
    photo_ids = data['photos']
    async with session.begin():
        for photo_id in photo_ids:
            await session.execute(insert(Photo).values(item_id=data['item_id'], photo_id=photo_id))


async def select_photos_for_item(session: AsyncSession, item_id: int):
    async with session.begin():
        result = await session.execute(select(Photo.photo_id).where(Photo.item_id == item_id))
        return result.fetchall()

async def delete_category(session: AsyncSession, data: dict[str, Any]):
    items = await get_items_for_current_category(data['category'], session)

    for item in items:
        await delete_item(session, item[0].id)
    
    async with session.begin():
        await session.execute(delete(Category).where(Category.name == data['category']))
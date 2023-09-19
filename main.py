import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import TOKEN_API, db_url
from db.base import Base
from middlewares.db import DbSessionMiddleware
from handlers.base import main_router
from handlers.shop.base import shop_router
from handlers.admin.base import admin_router
from handlers.art.base import art_router


async def main():
    #Database connection
    engine = create_async_engine(db_url, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(TOKEN_API)
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(admin_router)
    dp.include_router(shop_router)
    dp.include_router(art_router)
    dp.include_router(main_router)
    
    dp.update.middleware(DbSessionMiddleware(session_pool=async_session))
    
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from config import TOKEN_API
from db.models import metadata
# from db.queries import insert_sizes_before_start
from middlewares.db import DbSessionMiddleware
from handlers.shop.base import shop_router
from handlers.admin.base import admin_router


async def main():
    engine = create_engine('sqlite:///goji.sqlite3', echo=True)
    session_maker = sessionmaker(engine, expire_on_commit=False)

    bot = Bot(TOKEN_API)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(admin_router)
    dp.include_router(shop_router)
    
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    
    # metadata.drop_all(engine)
    metadata.create_all(engine)
    
    # try:
    #     await insert_sizes_before_start(session_maker)
    # except Exception as ex:
    #     print(ex)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
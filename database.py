from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import select
from telegram import Update
from telegram.ext import ContextTypes
from methods import BikerMethod, TravelMethod
from models import Base, Biker, Travel
from config import settings

engine = create_async_engine(
    url='sqlite+aiosqlite:///db/trips.db',
    echo=True
)

assesion = async_sessionmaker(engine, expire_on_commit=False)


def connection(method):
    async def wrapper(*args, **kwargs):
        async with assesion() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
    return wrapper


@connection
async def add_one_biker(user_data: dict, session: AsyncSession):
    new_biker = await BikerMethod.add(session=session, **user_data)
    print(f'Добавлен новый пользователь: {new_biker.id}')
    return new_biker


async def in_group_check(update: Update, context: ContextTypes):
    try:
        chat_member = await context.bot.get_chat_member(chat_id=settings.CHAT_ID, user_id=update.message.from_user.id)
        if chat_member != 'left':
            return True
    except:
        return False
    return False


@connection
async def get_all_travels(session):
    return await TravelMethod.get_all(session)


@connection
async def get_all_bikers(session):
    return await BikerMethod.get_all(session)


async def get_user(session):
    query = select(Biker)
    result = await session.execute(query)
    records = result.scalars()
    return records.all()


async def create_all():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_data(update: Update, biker: Biker):
    async with assesion() as session:
        data = update.message.text.splitlines()
        trip_info = Travel(
            title=data[1][1 + data[1].find(':'):],
            date=data[2][1 + data[2].find(':'):],
            route=data[3][1 + data[3].find(':'):],
            distance=data[4][1 + data[4].find(':'):],
            trip_time=data[5][1 + data[5].find(':'):],
            description=data[6][1 + data[6].find(':'):],
            biker_id=biker.id,
            biker=biker
        )
        session.add_all([trip_info, ])
        await session.commit()

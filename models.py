import datetime

from sqlalchemy import ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (DeclarativeBase, Mapped, class_mapper,
                            declared_attr, mapped_column, relationship)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    def to_dict(self) -> dict:
        columns = class_mapper(self.__class__).columns
        return {column.key: getattr(self, column.key) for column in columns}


class Biker(Base):
    first_name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    user_chat_id: Mapped[int]
    travels: Mapped[list['Travel']] = relationship(
        'Travel', back_populates='biker', cascade='all, delete-orphan')


class Travel(Base):
    title: Mapped[str]
    date: Mapped[str]
    route: Mapped[str]
    distance: Mapped[int]
    trip_time: Mapped[int]
    description: Mapped[str]
    biker_id: Mapped[int] = mapped_column(
        ForeignKey('bikers.id', ondelete='CASCADE'))
    biker: Mapped[Biker] = relationship('Biker', lazy='joined')
    __table_args__ = (
        UniqueConstraint('biker_id', 'title'),
    )

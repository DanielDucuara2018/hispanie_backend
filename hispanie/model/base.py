from datetime import date
from typing import Any, Type, TypeVar, overload

from sqlalchemy import ARRAY, Date, MetaData, cast, select
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm.decl_api import DeclarativeMeta

from hispanie import db
from hispanie.errors import Error, NoDataFound
from hispanie.utils import to_list

T = TypeVar("T", bound="Base")

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    __errors__: dict[str, type[Error]] = {}
    metadata = MetaData(naming_convention=naming_convention)

    id: Mapped[str] | None

    @overload
    @classmethod
    async def find(
        cls: Type[T],
        filter_defs: dict[str, Any],
        joins: list[DeclarativeMeta],
        **filters: Any,
    ) -> list[T]: ...

    @overload
    @classmethod
    async def find(
        cls: Type[T],
        **filters: Any,
    ) -> list[T]: ...

    @classmethod
    async def find(
        cls: Type[T],
        filter_defs: dict[str, Any] | None = None,
        joins: list[DeclarativeMeta] | None = None,
        **filters: Any,
    ) -> list[T]:
        async with db.session_scope() as session:
            stmt = select(cls)

            if joins:
                for jn in joins:
                    stmt = stmt.outerjoin(jn)

            for_equality = True
            for key, value in filters.items():
                if key.startswith("!"):
                    key = key[1:]
                    for_equality = False

                if filter_defs and key in filter_defs:
                    column = filter_defs[key]
                else:
                    column = getattr(cls, key)

                if not isinstance(value, list):
                    value = to_list(value)

                is_date = any(isinstance(v, date) for v in value)

                if isinstance(column.type, ARRAY):
                    filter_expr = column.overlap(value)
                else:
                    if is_date:
                        column = cast(column, Date)
                    filter_expr = column.in_(value)

                if for_equality:
                    stmt = stmt.where(filter_expr)
                else:
                    stmt = stmt.where(~filter_expr)

            result = await session.execute(stmt)
            return list(result.scalars().all())

    @classmethod
    async def get(cls: Type[T], **kwargs) -> T:
        async with db.session_scope() as session:
            if "id" in kwargs and len(kwargs) == 1:
                result = await session.get(cls, kwargs["id"])
            else:
                stmt = select(cls)
                for key, value in kwargs.items():
                    stmt = stmt.where(getattr(cls, key) == value)
                result = (await session.execute(stmt)).scalars().first()

            if not result:
                if error := cls.__errors__.get("_error"):
                    raise error(**kwargs)
                raise NoDataFound(key=kwargs, messages="Not data found in DB")
            return result

    async def update(self: T, force_update: bool = False, **kwargs) -> T:
        async with db.session_scope() as session:
            merged = await session.merge(self)
            for key, value in kwargs.items():
                if force_update or value is not None:
                    setattr(merged, key, value)
        return merged

    async def create(self: T) -> T:
        async with db.session_scope() as session:
            session.add(self)
        return self

    async def delete(self: T) -> T:
        async with db.session_scope() as session:
            merged = await session.merge(self)
            await session.delete(merged)
        return self

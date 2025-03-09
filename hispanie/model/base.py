from datetime import date
from typing import Any, Type, TypeVar

from sqlalchemy import ARRAY, Date, cast
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm.decl_api import DeclarativeMeta

from hispanie import db
from hispanie.errors import Error, NoDataFound
from hispanie.utils import to_list

T = TypeVar("T", bound="Base")


class Base(DeclarativeBase):
    __errors__: dict[str, type[Error]] = {}

    id: Mapped[str] | None

    @classmethod
    def find(
        cls: Type[T],
        filter_defs: dict[str, Any] | None = None,
        joins: list[DeclarativeMeta] | None = None,
        **filters,
    ) -> list[T]:
        with db.session_scope() as session:
            query = session.query(cls)

        if joins:
            for jn in joins:
                query = query.outerjoin(jn)

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
                filter = column.overlap(value)
            else:
                if is_date:
                    column = cast(column, Date)
                filter = column.in_(value)

            if for_equality:
                query = query.filter(filter)
            else:
                query = query.filter(~filter)

        return query.all()

    @classmethod
    def get(cls: Type[T], **kwargs) -> T:
        with db.session_scope() as session:
            query = session.query(cls)
        if not (result := query.get(kwargs)):
            if error := cls.__errors__.get("_error"):
                raise error(**kwargs)
            raise NoDataFound(key=kwargs, messages="Not data found in DB")
        return result

    def update(self: T, force_update: bool = False, **kwargs) -> T:
        with db.session_scope():
            for key, value in kwargs.items():
                if force_update or value is not None:
                    setattr(self, key, value)
        return self

    def create(self: T) -> T:
        with db.session_scope() as session:
            session.add(self)
        return self

    def delete(self: T) -> T:
        with db.session_scope() as session:
            session.delete(self)
        return self

from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.sql import ColumnElement

from pydevman.db.mixin import IdMixin, SoftDeleteMixin

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseMapper(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        assert issubclass(model, DeclarativeBase), "必须是 s.o.DeclarativeBase 的子类"
        assert issubclass(model, IdMixin), "必须是 IdMixin 的子类"
        assert issubclass(model, SoftDeleteMixin), "必须是 SoftDeleteMixin 的子类"
        self.model: Type[ModelType] = model

    def get(self, session: Session, id: int) -> ModelType | None:
        """获取单个对象 by id"""
        return session.get(self.model, id)

    def get_by_condition(
        self, session: Session, condition: ColumnElement[bool]
    ) -> ModelType | None:
        """获取单个对象 by 条件(自动过滤软删除)"""
        stmt = select(self.model).where(self._not_soft_del).where(condition).limit(1)
        return session.scalars(stmt).first()

    def list(
        self,
        session: Session,
        condition: Optional[ColumnElement[bool]] = None,
        limit: int | None = None,
    ) -> list[ModelType]:
        """批量获取"""
        stmt = select(self.model).where(self._not_soft_del)
        if condition:
            stmt = stmt.where(condition)
        if limit:
            stmt = stmt.limit(limit)
        return session.scalars(stmt).all()

    def create(self, session: Session, po: ModelType) -> ModelType:
        """插入"""
        session.add(po)
        return po

    def create_list(
        self, session: Session, po_list: list[ModelType]
    ) -> list[ModelType]:
        """批量插入"""
        for po in po_list:
            session.add(po)
        return po_list

    def update(self, session: Session, id: int, values: dict):
        stmt = update(self.model).where(self.model.id == id).values(**values)
        res = session.execute(stmt)
        return res.rowcount or 0

    def update_by_condition(
        self, session: Session, values: dict, condition: ColumnElement[bool]
    ) -> int:
        stmt = update(self.model).values(**values)
        if condition is not None:
            stmt = stmt.where(condition)
        res = session.execute(stmt)
        return res.rowcount or 0

    def delete_soft(self, session: Session, id: int) -> int:
        """软删除 by id"""
        return self.update(session, id, {"is_delete": True})

    def delete(self, session: Session, id: int) -> int:
        """硬删除 by id"""
        stmt = delete(self.model).where(self.model.id == id)
        res = session.execute(stmt)
        return res.rowcount or 0

    @property
    def _not_soft_del(self) -> ColumnElement[bool]:
        return self.model.is_delete.is_(False)

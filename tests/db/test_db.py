from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import DateTime, Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.sql import func

from pydevman.db.core import BaseMapper


class Base(DeclarativeBase): ...


class AuditMixin:
    """表结构基础:包含表基础字段(创建时间、更新时间和软删除标识)"""

    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )
    is_delete: Mapped[bool] = mapped_column(default=False)


@dataclass
class User(Base, AuditMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键"
    )
    name: Mapped[str]
    age: Mapped[int]


@dataclass
class Order(Base, AuditMixin):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键"
    )
    order_id: Mapped[int]


class UserMapper(BaseMapper[User]):
    model = User


class OrderMapper(BaseMapper[Order]):
    model = Order


class Database:
    def __init__(self, url: str):
        self.url = url
        self.engine = create_engine(
            url,
            echo=True,
            # 需要 json 时打开
            # json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False),
        )
        Base.metadata.create_all(self.engine)


class Service:
    def __init__(
        self, engine: Engine, user_mapper: UserMapper, order_mapper: OrderMapper
    ):
        self.engine = engine
        # 看情况也可以用 sessionmaker
        # self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        # with self.Session.begin() as session:
        self.user_mapper = user_mapper
        self.order_mapper = order_mapper

    def get_user_order(self, user_id: int, order_id: int):
        # expire_on_commit=False 主要是 DetachedInstanceError
        #  由于会话关闭后，对象返回，再次读取对象会 Error
        with Session(self.engine, expire_on_commit=False) as session, session.begin():
            user = self.user_mapper.get_by_condition(session, User.id == user_id)
            order = self.order_mapper.get_by_condition(session, Order.id == order_id)
        return user, order

    def insert_user_order(self, user: User, order: Order):
        """事务需要在业务层保证，而不是 Mapper"""
        with Session(self.engine) as session, session.begin():
            self.user_mapper.create(session, user)
            self.order_mapper.create(session, order)

    def update_user_order(self, user: User, order: Order):
        """事务需要在业务层保证，而不是 Mapper"""
        with Session(self.engine) as session, session.begin():
            self.user_mapper.upsert_one(session, user)
            self.order_mapper.upsert_one(session, order)


def test_db():
    db = Database("sqlite:///:memory:")
    user_mapper = BaseMapper(User)
    order_mapper = BaseMapper(Order)
    service = Service(db.engine, user_mapper, order_mapper)

    user = User(name="alice", age=12)
    order = Order(order_id=123)

    service.insert_user_order(user, order)
    res = service.get_user_order(1, 1)
    service.update_user_order()
    print(res)

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from datetime import datetime


# SQLA 1
# class Base(DeclarativeBase):
#     registry_date = Column(DateTime)

# SQLA 2
class Base(DeclarativeBase):
    registry_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    nickname: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return (f"UserObject(id={self.id};"
                f"nickname={self.nickname};"
                f"is_admin={self.is_admin}")


class Nick(Base):
    __tablename__ = "nickname"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nick: Mapped[str]
    owner_id: Mapped[int] = mapped_column(Boolean,nullable=True)

    def __repr__(self):
        return (f"UserObject(id={self.id};"
                f"nickname={self.nick};"
                f"owner={self.owner_id})")

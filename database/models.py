from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
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
    nickname_id: Mapped[int] = mapped_column(Integer,ForeignKey("nickname.id"),nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    room_id: Mapped[int] = mapped_column(Integer,nullable=True)

    #relationships
    nickname: Mapped["Nick"] = relationship(lazy="joined",back_populates="users")


    def __repr__(self):
        return (f"UserObject(id={self.id};"
                f"nickname_id={self.nickname_id};"
                f"is_admin={self.is_admin}")


class Nick(Base):
    __tablename__ = "nickname"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nick: Mapped[str]

    #relationships
    users: Mapped[list["User"]] = relationship(lazy="select",back_populates="nickname")

    def __repr__(self):
        return (f"UserObject(id={self.id};"
                f"nickname={self.nick};")

class Room(Base):
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    owner_id:Mapped[int]
    name: Mapped[str]
    password: Mapped[str]

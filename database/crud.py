from datetime import datetime
from sqlalchemy.orm import Session,lazyload,joinedload
from sqlalchemy import select, text, func, insert, and_
from sqlalchemy import update
import  hashlib
# from sqlalchemy.orm.sync import update


from .models import User, Nick,Room
from .db import engine


# SQLA 1
# def get_all_users() -> list[User]:
#     with Session(bind=engine) as session:
#         users = session.query(User).all()
#         return users

# SQLA 2
# def get_all_users() -> list[User]:
#     with Session(bind=engine) as session:
#         stmt = select(User).limit(5) # statement
#         result = session.execute(stmt).all()
#         r_result = []
#         for user_tuple in result:
#             r_result.append(user_tuple[0])
#         return result.all()

def is_user_registered(user_id: int) -> bool:
    with Session(bind=engine) as session:
        stmt = select(User).where(User.id == user_id)
        print("запрос по регистрации")
        print(stmt)
        print("запрос по регистрации")
        result = session.execute(stmt).scalars().first()
        return result is not None

def get_all_users() -> list[User]:
    with Session(bind=engine) as session:
        stmt = select(User).limit(5)  # statement
        result = session.execute(stmt).unique().scalars().all()
        return result


def add_user(id: int, is_admin: bool, registry_date: datetime):
    with Session(bind=engine) as session:
        new_user = User(id=id, is_admin=is_admin, registry_date=registry_date)

        session.add(new_user)
        session.commit()
        return f"Пользователь c id {id} добавлен"


# def ar():
#    random_nickname = session.query(Nickname).filter(Nickname.owner_id == None).order_by(func.random()).first()

def add_nick(nick: str, owner_id: bool):
    with Session(bind=engine) as session:
        new_nick = Nick(owner_id=owner_id, nick=nick)
        session.add(new_nick)
        session.commit()
        return f"Ник{nick} добавлен"


def check_user(user_id: int):
    with Session(bind=engine) as session:
        user = session.get(User, user_id)
        return user


def get_free_nick():
    with Session(bind=engine) as session:
        stmt = select(Nick).where(Nick.owner_id.is_(None)).order_by(func.random()).limit(1)
        result = session.execute(stmt).scalars().first()
        if result is None:
            # print("нет ников")
            return
        return result


def set_owner_id(own_id: int, nick_id: int):
    with Session(bind=engine) as session:
        stmt = update(Nick).where(Nick.id == nick_id).values(owner_id=own_id)
        session.execute(stmt)
        session.commit()

def set_room_id(user_id: int, room_id: int):
    with Session(bind=engine) as session:
        stmt = update(User).where(User.id == user_id).values(room_id=room_id)
        session.execute(stmt)
        session.commit()

def check_owner_id_room(own_id:int):
    with Session(bind=engine) as session:
        stmt = select(Room.id).where(Room.owner_id == own_id)
        result =  session.execute(stmt).scalar()
        return result is not None

def check_user_id_room(user_id:int):
    with Session(bind=engine) as session:
        stmt = select(User.room_id).where(User.id == user_id)
        result =  session.execute(stmt).scalar()
        return result is not None

def check_room_id(user_id:int):
    with Session(bind=engine) as session:
        stmt = select(User.room_id).where(User.id == user_id)
        result =  session.execute(stmt).scalar()
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        print(result)
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        return result is not None


def check_adm(user_id):
    with Session(bind=engine) as session:
        stmt = select(User.is_admin).where(User.id == user_id)
        return session.execute(stmt).scalar()


def add_nick(new_nick: str):
    with Session(bind=engine) as session:
        new_nick = Nick(nick=new_nick)
        session.add(new_nick)
        session.commit()


def create_room(name: str,
                password: str,
                owner_id: int):
    with Session(bind=engine) as session:
        password = hashlib.sha256(password.encode()).hexdigest()
        print(password)
        curr_room = Room(owner_id=owner_id,
                         name=name,
                         password=password)
        session.add(curr_room)
        session.commit()
        set_room_id(owner_id, curr_room.id)
        print(curr_room.id,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")


def check_valid_room(room_name: str,
                  password:str):
    with Session(bind=engine) as session:
        stmt = select(Room.password==hashlib.sha256(password.encode()).hexdigest()).where(Room.name==room_name)
        result = session.execute(stmt).scalars().first()
        if not result: #проверка на название
            return False
        return True

def check_busy_name_room(room_name:str):
    with Session(bind=engine) as session:
        stmt = select(Room.name).where(Room.name==room_name)
        result = session.execute(stmt).scalars().first()
        if not result: #проверка на название
            return False
        return True


def join_room(user_id:int,room_name):
    with Session(bind=engine) as session:
        stmt = select(Room).where(Room.name==room_name)
        room = session.execute(stmt).scalars().first()
        room_id = room.id
        stmt = select(User).where(User.id==user_id)
        user = session.execute(stmt).scalars().first()
        user.room_id = room_id
        session.commit()
        set_room_id(user_id, room_id)

def add_standart_data_nicks():
    with Session(bind=engine) as session:
        nicknames = ["Саша", "Маша", "Даша"]
        for nickname in nicknames:
            new_nick = Nick(nick=nickname)
            session.add(new_nick)
        session.commit()


def add_standart_data_nicks_sqla2():
    with Session(bind=engine) as session:
        nicknames = ["Саша", "Маша", "Даша"]
        data = [{"nick": nickname} for nickname in nicknames]
        # for nickname in nicknames:
        #     data.append({"nick": nickname})
        # stmt = insert(Nick).values([
        #     {"nick": "Эдуард"},
        #     {"nick": "Маргарита"}
        # ])
        stmt = insert(Nick).values(data)
        print(stmt)
        session.execute(stmt)
        session.commit()


# SQLA1
# def delete_user(user_id:int):
#     with Session(bind=engine) as session:
#         user = session.query(User).filter(User.id==user_id).one()
#         session.delete(user)
#         session.commit()
#         return f"Пользователь c id {user_id} удален"

def delete_user(user_id: int):
    with Session(bind=engine) as session:
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()

def delete_room_from_user(user_id:int):
    with Session(bind=engine) as session:
        #stmt = select(User.room_id).where(User.id==user_id)
        #user = session.execute(stmt).scalars().first()
        #user.room_id = None
        #session.commit()
        stmt = update(User).values(room_id=None).where(User.id==user_id)
        print(stmt)
        session.execute(stmt)
        session.commit()

def get_free_nickname_for_room(room_id:int) -> list[str]:
    with Session(bind=engine) as session:
        stmt = select(Nick.nick).join(User,and_(Nick.id == User.nickname_id, User.room_id == room_id),isouter=True).where(User.id.is_(None))
        print(stmt)
        nicknames = session.execute(stmt).scalars().fetchall()
        return nicknames
        #Авторское решение
        #nicknames_stmt = select(Nick.nick)
        #nicknames = session.execute(nicknames_stmt).scalars().fetchall()
        #print(nicknames)
        #busy_nicknames_stmt = select(Nick.nick).join(User,Nick.id==User.nickname_id).where(User.room_id == room_id)
        #busy_nicknames = session.execute(busy_nicknames_stmt).scalars().fetchall()
        #print(busy_nicknames)
        #nick_set = set(nicknames).difference(busy_nicknames)
        #print(nick_set)


def test_func_sql():
    with Session(bind=engine) as session:
        # return session.execute(text("SELECT random()")).scalar()
        return session.execute(select(func.random())).scalar()

# SELECT random()

import pymongo as pymongo

from classes.User import User
from constant import MONGO_DB_CONNECTION


def init_db():
    client = pymongo.MongoClient(MONGO_DB_CONNECTION)
    db = client.huge
    return db


def is_user_ip_contain(user: User) -> bool:
    """функция проверяет играли ли в игру с компьютера с текущим IP"""

    db = init_db()

    return db.users.find_one({"ip": user.ip})


def add_user_in_db(user: User) -> bool:
    """
    функция добавляет текущий ip компьютера в базу данных.
    Возвращает True, если операция успешна.
    """
    db = init_db()

    try:
        db.users.insert_one(user.get_dict())
        return True
    except Exception as e:
        print(e)
        return False


def update_user_in_db(user):
    """
        функция обновляет username текущего ip
        Возвращает True, если операция успешна.
        """
    db = init_db()
    try:
        db.users.update_one({"ip": user.ip}, {"username": user.username})
        return True
    except Exception as e:
        print(e)
        return False

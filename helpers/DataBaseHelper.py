import pymongo as pymongo

from classes.User import User
from constant import MONGO_DB_CONNECTION


def init_db():
    client = pymongo.MongoClient(MONGO_DB_CONNECTION)
    return client.huge


db = init_db()


def is_mac_contain(mac: str) -> bool:
    """функция проверяет играли ли в игру с компьютера с текущим MAC-адресом"""

    return db.users.find_one({"mac": mac})


def get_best_score(mac: str):
    return db.users.find_one({"mac": mac})['best_score']


def is_username_contain(user: User) -> bool:
    """функция проверяет играли ли в игру с таким именем"""

    return db.users.find_one({"username": user.username})


def get_username(uuid: str):
    """функция возвращает username, который привязан к текущему MAC-адресу"""

    return db.users.find_one({"mac": uuid})['username']


def add_user_in_db(user: User) -> bool:
    """
    функция добавляет текущий MAC-адресс компьютера в базу данных.
    Возвращает True, если операция успешна.
    """

    try:
        db.users.insert_one(user.get_dict())
        return True
    except Exception as e:
        print(e)
        return False


def update_user_in_db(user):
    """
    функция обновляет username текущего MAC-адреса
    Возвращает True, если операция успешна.
    """
    try:
        db.users.update_one({"mac": user.mac},
                            {"$set": {"username": user.username, "best_score": user.best_score}})
        return True
    except Exception as e:
        print(e)
        return False


def get_best_score_top():
    """функция возвращает топ участников игры"""
    return db.users.find({}, {'_id': 0, 'username': 1, 'best_score': 1, 'mac': 1})

class User:
    def __init__(self, username: str, ip: str):
        self.username = username
        self.ip = ip

    def get_dict(self):
        return {"ip": self.ip, "username": self.username}

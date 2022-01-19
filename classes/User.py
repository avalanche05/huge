class User:
    def __init__(self, username: str, mac: str, best_score: int = 0):
        self.username = username
        self.mac = mac
        self.best_score = best_score

    def get_dict(self):
        return {"mac": self.mac, "username": self.username, "best_score": self.best_score}

    def set_best_score(self, best_score):
        if best_score > self.best_score:
            self.best_score = best_score

    def set_username(self, username):
        self.username = username

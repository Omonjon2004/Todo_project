import bcrypt

class Hash:
    @staticmethod
    def make_password(password):
        salt = bcrypt.gensalt()
        encoded_password = password.encode("utf-8")
        return bcrypt.hashpw(encoded_password, salt).decode("utf-8")

    @staticmethod
    def match_password(password, hashed_password):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

class UsersService : 

    @staticmethod
    def get_user_by_email(email: str):
        print(email)
        return "user" 

    @staticmethod
    def get_password_by_email(email: str):
        print(email)
        return "password"

    @staticmethod
    def create_user(email: str, password: str):
        print(email, password)
        return True

    @staticmethod
    def delete_user(email: str):
        print(email)
        return True 

    @staticmethod
    def update_user(email: str, password: str):
        print(email, password)
        return True

    @staticmethod
    def is_admin(email: str):
        print(email)
        return True

    
class UsersService : 

    @staticmethod
    def getUserByEmail(email):
        print(email)
        return "user" 

    @staticmethod
    def getPasswordByEmail(email):
        print(email)
        return "password"

    @staticmethod
    def createUser(email, password):
        print(email,password)
        return True

    @staticmethod
    def deleteUser(email):
        print(email)
        return True 

    @staticmethod
    def updateUser(email, password):
        print(email, password)
        return True

    @staticmethod
    def userIsAdmin(email):
        print(email)
        return True

    
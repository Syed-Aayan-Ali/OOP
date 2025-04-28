from models.customer import Customer
from models.admin import Admin
from services.file_saver import FileService

class AuthService:
    @staticmethod
    def login(username, password):
        users = FileService.load_users()
        
        print(users)

        for user in users:
            if user.username == username and user.password == password:
                return user
        return None

    @staticmethod
    def signup(user_data, role="customer"):
        users = FileService.load_users()

        for u in users:
            if u.username == user_data["username"]:
                raise Exception("Username already exists!")

        if role == "admin":
            new_user = Admin(**user_data)
        else:
            new_user = Customer(**user_data)

        users.append(new_user)
        FileService.save_users(users)
        return new_user

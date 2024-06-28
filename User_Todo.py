from db import *
from hash import *


session_user = None
class UI:
    def main(self):
        try:
            menu = """
                   1) Register
                   2) Login
                   0) Exits
                      >>>"""

            match input(menu):
                case "1":
                    Users().register()
                case "2":
                    Users().login()
                case "0":
                    return
        except psycopg2.Error as e:
            print(e)
            self.main()


class Users:
    def __init__(self):
        self.db = Database()

    def register(self):
        fullname = input("Full name >> ")
        username = input("Username >> ")
        email = input("Email >> ")
        password = input("Password >> ")
        phone_number = input("Phone number >> ")


        password=Hash.make_password(password)

        user_created = self.db.insert_user(fullname=fullname, username=username, password=password,
                                           email=email, phone_number=phone_number)
        if user_created:
            print("User registered successfully")
        else:
            print("Username or phone number is incorrect, please try again")

        UI().main()

    def login(self):
        global session_user
        username = input("Username >> ")
        password = input("Password >> ")

        user = self.db.get_user_by_username(username)

        if user and Hash.match_password(password, user[3]):
            session_user = user
            print(f"Logged in successfully as '{username}'")
            Todo().main()
        else:
            print("Invalid username or password. Please try again.")
            UI().main()


class Todo:
    def __init__(self):
        self.db = Database()
    def main(self):
        menu = """
        1) My todos
        2) Create a todo
        3) Update a todo
        4) Delete a todo
        5) Log out
        0) Exits
        >>> """

        match input(menu):
            case '1':
                self.view_todos()
            case '2':
                self.create_todo()
            case '3':
                self.update_todo()
            case '4':
                self.delete_todo()
            case '5':
                self.logout()
            case '0':
                UI().main()


    def view_todos(self):
        global session_user
        if session_user:
               owner_id = session_user[0]
               user=self.db.get_todos(owner_id=owner_id)
               if user:
                   print(f"Todo list view{user}")
                   menu="""
                    0)Exits
                   """
                   match input(menu):
                       case '0':
                           Todo().main()
               else:
                   menu = """
                     0)Exits
                         """
                   match input(menu):
                       case '0':
                           Todo().main()
                   print("Todo list view failed")
        else:
            print("No todo found")


    def create_todo(self):
        global session_user
        self.db = Database()

        title=input("Title >> ")
        status=input("Status >>")
        deadline=input("Deadline >> ")

        if session_user:
            owner_id = session_user[0]
            user = self.db.insert_todo(title=title, status=status, owner_id=owner_id, deadline=deadline)
            if user:
                print(f"Todo created successfully")
                Todo().main()
            else:
                print("Todo creation failed")
                Todo().create_todo()
        else:
            print("No todo found")
    def update_todo(self):
        print(" What do you want to update? ")
        menu="""
           1)Status >> Update
           2)Deadline >> Update
           0)Exits
        """
        match input(menu):
            case '1':
                self.title_update()
            case '2':
                self.deadline_update()
            case '0':
                Todo().main()
    def title_update(self):
        self.db = Database()
        new_status=input(" New_status >> ")
        title=input("Which Title do you want to update? >> ")
        user=self.db.title_update_todo(new_status=new_status,title=title)
        if user:
            print(f"Title updated successfully")
            Todo().main()
        else:
            print("Title update failed")
            Todo().update_todo()
    def deadline_update(self):
        self.db = Database()
        new_deadline=input("New deadline >> ")
        title=input("Which Title do you want to update? >> ")
        user=self.db.deadline_update_todo(new_deadline=new_deadline, title=title)
        if user:
            print(f"Status updated successfully")
            Todo().main()
        else:
            print("Status update failed")
            Todo().update_todo()
    def delete_todo(self):
        global session_user
        self.db = Database()
        title = input("Title >> ")
        status = input("Status >> ")

        if session_user:
            owner_id = session_user[0]
            user = self.db.delete_todo(owner_id=owner_id, title=title, status=status)
            if user:
                print(f"Todo updated successfully")
                Todo().main()
            else:
                print("Todo update failed")
        else:
            print("No todo found")
    def logout(self):
        global session_user
        if session_user:
            id=session_user[0]
            user=self.db.delete_user(id=id)
            if user:
                print(f"Todo list view{user}")
                session_user=None
                UI().main()
                print("Logged out successfully")
            else:
                print("Login failed")




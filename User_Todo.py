import psycopg2

from db import Database
from hash import Hash

session_user = None

class UI:
    def main(self):
        try:
            menu = """
                   1) Register
                   2) Login
                   0) Exit
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

        password = Hash.make_password(password)

        user_created = self.db.insert_user(fullname=fullname, username=username, password=password,
                                           email=email, phone_number=phone_number)
        if user_created:
            print("User registered successfully")
        else:
            print("User registration failed. Please try again.")

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
        0) Exit
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
            todos = self.db.get_todos(owner_id=owner_id)
            if todos:
                print(f"Todo list: {todos}")
            else:
                print("No todos found")
        else:
            print("No todos found")

        self.main()

    def create_todo(self):
        global session_user
        title = input("Title >> ")
        status = input("Status >> ")
        deadline = input("Deadline >> ")

        if session_user:
            owner_id = session_user[0]
            todo_created = self.db.insert_todo(title=title, status=status, owner_id=owner_id, deadline=deadline)
            if todo_created:
                print("Todo created successfully")
            else:
                print("Todo creation failed")
        else:
            print("No user session found")

        self.main()

    def update_todo(self):
        print("What do you want to update?")
        menu = """
           1) Status
           2) Deadline
           0) Exit
        >>> """
        match input(menu):
            case '1':
                self.status_update()
            case '2':
                self.deadline_update()
            case '0':
                self.main()

    def status_update(self):
        global session_user
        if session_user:
            owner_id = session_user[0]
            todos = self.db.get_todos(owner_id=owner_id)
            if todos:
                print(todos)
                todo_id = input("Enter Todo ID to update status >> ")
                new_status = input("New Status >> ")
                status_updated = self.db.update_todo_status(new_status=new_status, id=todo_id, owner_id=owner_id)
                if status_updated:
                    print("Todo status updated successfully")
                else:
                    print("Todo status update failed")
            else:
                print("No todos found")
        else:
            print("No user session found")
        self.main()

    def deadline_update(self):
        global session_user
        if session_user:
            owner_id = session_user[0]
            todos = self.db.get_todos(owner_id=owner_id)
            if todos:
                print(todos)
                todo_id = input("Enter Todo ID to update deadline >> ")
                new_deadline = input("New Deadline >> ")
                deadline_updated = self.db.update_todo_deadline(new_deadline=new_deadline, id=todo_id, owner_id=owner_id)
                if deadline_updated:
                    print("Todo deadline updated successfully")
                else:
                    print("Todo deadline update failed")
            else:
                print("No todos found")
        else:
            print("No user session found")
        self.main()


    def delete_todo(self):
        global session_user
        if session_user:
            owner_id = session_user[0]
            todos = self.db.get_todos(owner_id=owner_id)
            if todos:
                print(todos)
                todo_id = input("Enter Todo ID to delete >> ")
                todo_deleted = self.db.delete_todo(todo_id)
                if todo_deleted:
                    print("Todo deleted successfully")
                else:
                    print("Todo deletion failed")
            else:
                print("No user session found")


        self.main()

    def logout(self):
        global session_user
        if session_user:
            user_id=session_user[0]
            res=self.db.log_out(user_id=user_id)
            if res:
                print("Logged out successfully")
                UI().main()
            else:
                print("Logout failed")
                self.main()
        else:
            print("No user session found")



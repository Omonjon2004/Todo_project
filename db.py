import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        try:
            self.db = psycopg2.connect(
                host='localhost',
                database='postgres',
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
            )
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def create_user_table(self):
        try:
            cursor = self.db.cursor()
            create_user_sql = """
              create table users (
                    id serial primary key,
                    fullname varchar(255) not null, 
                    username varchar(128) not null unique,
                    password varchar(128) not null,
                    email varchar(56) unique,
                    phone varchar(56) check (LENGTH(phone) >= 13)
                );             
            """
            cursor.execute(create_user_sql)
            self.db.commit()
            print("Table 'users' created successfully.")
        except psycopg2.Error as mes:
            print(f"Error creating 'users' table: {mes}")

    def create_todos_table(self):
        try:
            cursor = self.db.cursor()
            create_todos_sql = """
               create table todos (
                        id serial primary key,
                        title varchar(128) not null, 
                        status varchar(128) not null,
                        owner_id int references users(id) on delete cascade,
                        deadline timestamp default now() + interval '1 day');
                      """
            cursor.execute(create_todos_sql)
            self.db.commit()
            print("Table 'todos' created successfully.")
        except psycopg2.Error as mes:
            print(f"Error creating 'todos' table: {mes}")

    def insert_user(self, fullname, username, password, email, phone_number):
        try:
            insert_user_sql = """
                insert into users (fullname, username, password, email, phone) 
                values (%s, %s, %s, %s, %s);
            """
            cursor = self.db.cursor()
            cursor.execute(insert_user_sql, (fullname, username, password, email, phone_number))
            self.db.commit()
            return True
        except psycopg2.Error as mes:
            print(f"Error inserting user: {mes}")
            return False

    def get_todos(self, owner_id):
        try:
            get_todos_sql = """
            select * from todos where owner_id=%s;
            """
            cursor = self.db.cursor()
            cursor.execute(get_todos_sql, (owner_id,))
            todos = cursor.fetchall()
            return todos
        except psycopg2.Error as e:
            print(f"Error fetching todos: {e}")
            return None

    def delete_user(self, id):
        try:
            delete_user_sql = """
            delete from users where id=%s;                      
            """
            cursor = self.db.cursor()
            cursor.execute(delete_user_sql, (id,))
            self.db.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error deleting user: {e}")
            return False

    def get_user_by_username(self, username):
        try:
            search_username_sql = """
                select * from users where username = %s;
            """
            cursor = self.db.cursor()
            cursor.execute(search_username_sql, (username,))
            result = cursor.fetchone()
            return result
        except psycopg2.Error as mes:
            print(f"Error fetching user '{username}': {mes}")
            return None

    def insert_todo(self, title, status, owner_id, deadline):
        try:
            insert_todo_sql = """
            insert into todos (title, status, owner_id, deadline) 
            values (%s, %s, %s, %s);
            """
            cursor = self.db.cursor()
            cursor.execute(insert_todo_sql, (title, status, owner_id, deadline))
            self.db.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error creating todo: {e}")
            return False

    def delete_todo(self, todo_id):
        try:
            delete_todo_sql = """
            delete from todos where id=%s;
            """
            cursor = self.db.cursor()
            cursor.execute(delete_todo_sql, (todo_id,))
            self.db.commit()

            if cursor.rowcount > 0:
                print(f"Todo with id '{todo_id}' deleted successfully.")
                return True
            else:
                print(f"No todo found with id '{todo_id}'.")
                return False
        except psycopg2.Error as e:
            print(f"Error deleting todo with id '{todo_id}': {e}")
            return False

    def update_todo_status(self, new_status, id, owner_id):
        try:
           update_status_sql = """
                      update todos set status=%s where id=%s and owner_id=%s;
                            """
           cursor = self.db.cursor()
           cursor.execute(update_status_sql, (new_status, id, owner_id))
           self.db.commit()
           if cursor.rowcount > 0:
               print(f"Todo with id '{id}' deleted successfully.")
               return True
           else:
               print(f"No todo found with id '{id}'.")
               return False
        except psycopg2.Error as e:
            print(f"Error deleting todo with id '{id}': {e}")
        return False




    def update_todo_deadline(self, new_deadline, id, owner_id):
        try:
           update_status_sql = """
                      update todos set deadline=%s where id=%s and owner_id=%s;
                            """
           cursor = self.db.cursor()
           cursor.execute(update_status_sql, (new_deadline, id, owner_id))
           self.db.commit()
           if cursor.rowcount > 0:
               print(f"Todo with id '{id}' update successfully.")
               return True
           else:
               print(f"No todo found with id '{id}'.")
               return False
        except psycopg2.Error as e:
            print(f"Error updating todo with id '{id}': {e}")
        return False


    def log_out(self,user_id):
        try:
            user_delete_sql = """
                          delete from users where id=%s;
                          """
            cursor = self.db.cursor()
            cursor.execute(user_delete_sql, (user_id,))
            self.db.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error logging out: {e}")
            return False




if __name__ == "__main__":
    db = Database()
    db.create_user_table()
    db.create_todos_table()

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
              create table  users (
                    id serial primary key,
                    fullname varchar(255) not null, 
                    username varchar(128) not null unique ,
                    password varchar(128) not null ,
                    email varchar(56) unique ,
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
            create_todos_sql="""
               create table  todos (
                        id serial primary key,
                        title varchar(128)  not null, 
                        status varchar(128) not null,
                        owner_id int references users(id) on delete  cascade ,
                        deadline timestamp default now()+interval '1 day');
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
            return False
    def get_todos(self, owner_id):
        try:
            get_todos="""
            select * from todos where owner_id=%s;
            """
            cursor = self.db.cursor()
            cursor.execute(get_todos, (owner_id,))
            todos = cursor.fetchall()
            return todos
        except psycopg2.Error as e:
            return None
    def delete_user(self, id):
        try:
            delete_user_sql="""
            delete from users where id=%s;                      
            """
            cursor = self.db.cursor()
            cursor.execute(delete_user_sql, (id,))
            self.db.commit()
            return True
        except psycopg2.Error as e:
            return False
    def get_user_by_username(self, username):
        try:
            search_username_sql = """
                select * from users where username = %s ;
            """
            cursor = self.db.cursor()
            cursor.execute(search_username_sql, (username,))
            result = cursor.fetchone()
            return result
        except psycopg2.Error as mes:
            print(f"Error fetching user '{username}': {mes}")
            return None

    def insert_todo(self, title, status, owner_id,deadline):
        try:
            insert_todo="""
            insert into todos (title, status, owner_id,deadline) 
            values (%s, %s, %s,%s);
            """
            cursor = self.db.cursor()
            cursor.execute(insert_todo, (title, status, owner_id,deadline))
            self.db.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error creating todo: {e}")
            return False

    def delete_todo(self,id):
       try:
           delete_todo = """
                   delete from todos where id=%s;
                  """
           cursor = self.db.cursor()
           cursor.execute(delete_todo, (id,))
           self.db.commit()
           return True
       except psycopg2.Error as e:
           print(f"Error deleting todo: {e}")
           return False



    def title_update_todo(self, new_status,title,owner_id):
        try:
            title_sql="""
            update todos set status=%s where title=%s and owner_id=%s;
             """
            cursor = self.db.cursor()
            cursor.execute(title_sql, (new_status,title,owner_id))
            self.db.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error updating todo: {e}")
            return False
    def deadline_update_todo(self, new_deadline,title):
        try:
            status_sql="""
            update todos set status=%s where title=%s;
            """
            cursor = self.db.cursor()
            cursor.execute(status_sql, (new_deadline,title))
            self.db.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error updating todo: {e}")






if __name__ == "__main__":
    # Database().create_user_table()
    Database().create_todos_table()



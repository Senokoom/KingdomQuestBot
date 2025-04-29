
import mysql.connector
from mysql.connector import Error

# class user:
#     def __init__(self, user_id):
#         self.id = user_id
#         self.changer = 0
#         self.changer_log = []
#         self.botstarted = False

# class state:
#     def __init__(self, ):
        


class MySQLDataBase:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.connect()

    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                port = self.port,
                database = self.database,
                user = self.user,
                password = self.password
            )
            if self.connection.is_connected():
                print("Успешно подключился к БД")
        except Error as e:
            print(f"Ошибка подключения к БД: {e}")
    


    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Разорвали соединение с БД")
    


    def find_user_by_tgid(self, tgid):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE tgid = %s"
            cursor.execute(query, (tgid, ))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Ошибка при поиске: {e}")
            return None



    def create_user(self,  tgid, initial_count=0):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(id) FROM users")
            max_id = cursor.fetchone()[0] or 0
            new_id = max_id + 1
            
            query = "INSERT INTO users (id, tgid, count) VALUES (%s, %s, %s)"
            cursor.execute(query, (new_id, tgid, initial_count))
            cursor.close()
            return new_id
        except Error as e:
            print(f"Произошла ошибка при создании: {e}")
            return None


    def get_or_create_user(self, tgid):
        user = self.find_user_by_tgid(tgid)
        if not user:
            new_id = self.create_user(tgid)
            if new_id:
                print("Создал нового")
                return{'id': new_id, 'tgid': tgid, 'count': 0}
            return None
        print("старый")
        return user
    

    def update_user_count(self, tgid, new_count):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE users SET count = %s WHERE tgid = %s"
            cursor.execute(query, (new_count, tgid))
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()

            return affected_rows > 0
        except Error as e:
            print(f"Произошла ошбика при обновлении count: {e}")
            return False
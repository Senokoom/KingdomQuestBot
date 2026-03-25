import mysql
from mysql.connector import Error


class MySQLDataBase:
    def __init__(self, config):

        self.host = config["host"]
        self.port = config["port"]
        self.database = config["database"]
        self.user = config["user"]
        self.password = config["password"]

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
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
            self.connection.commit()
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

    def update_user_event(self, tgid, new_event):
        try: 
            cursor = self.connection.cursor()
            query = "UPDATE users SET event = %s WHERE tgid = %s"
            cursor.execute(query, (new_event, tgid))
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()

            return affected_rows > 0
        except Error as e:
            print(f"Произошла ошибка при обновлении event: {e}")
            return False

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

    def update_user(self, tgid, data):
        try:
            cursor = self.connection.cursor()

            query = """
            UPDATE users
            SET count=%s,
                gold=%s,
                soldier=%s,
                peasant=%s,
                loyality_soldier=%s,
                loyality_peasant=%s
            WHERE tgid=%s
            """

            cursor.execute(query, (
                data["count"],
                data["gold"],
                data["soldier"],
                data["peasant"],
                data["loyality_soldier"],
                data["loyality_peasant"],
                tgid
            ))

            self.connection.commit()

        except Exception as e:
            print("DB ERROR:", e)

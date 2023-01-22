import sqlite3
import time
import math

from flask_sqlalchemy import SQLAlchemy

class Database:
    def __init__(self):
        self.db_file = '/home/flask_app/big_arb.db'

        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def creat(self, request):
        with self.connection:
            result = self.cursor.execute(
                request)

    def add_trade(self, db_data):
        with self.connection:
            self.cursor.executemany(
                "INSERT INTO arbitrage (profit, exchange1, exchange2, bank1, bank2, crypto_path, role, start_min, start_max, rates_path, value, exchange_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                db_data)


    def clear_table(self):
        with self.connection:
            self.cursor.execute("DELETE FROM arbitrage")

    # def add_trade_new(self, db_data):
    #     with self.connection:
    #         self.cursor.executemany(
    #             "INSERT INTO arbitrage_new (profit, exchange1, exchange2, bank1, bank2, crypto_path, role, start_min, start_max, finish_min, finish_max, exchange_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #             db_data)
    #
    # def clear_table_new(self):
    #     with self.connection:
    #         self.cursor.execute("DELETE FROM arbitrage_new")

    def select_data(self, **kwargs):
        with self.connection:

            params = (
                kwargs.get('profit_from', -100),
                kwargs.get('profit_to', 15),
                kwargs.get('start_min', 500)
                # kwargs.get("exchange1", all_exchange),
                # kwargs.get("exchange2", "%"),
                # kwargs.get("bank1", "%"),
                # kwargs.get("bank2", "%"),
                # kwargs.get('crypto_from', '%'),
                # kwargs.get('crypto_to', '%'),
                # kwargs.get("role", '%'),

            )
            result = self.cursor.execute(
                f"""SELECT exchange1, exchange2, role, bank1, bank2, crypto_path, rates_path, start_min, start_max, profit, exchange_path 
                FROM arbitrage WHERE profit BETWEEN ? AND ? AND exchange1 {kwargs.get("exchange1", 'LIKE "%"')} 
                AND exchange2 {kwargs.get("exchange2", 'LIKE "%"')} AND bank1 {kwargs.get("bank1", 'LIKE "%"')} 
                AND bank2 {kwargs.get("bank2", 'LIKE "%"')} AND ({kwargs.get("crypto_from", "crypto_path LIKE '%'")}) AND ({kwargs.get("crypto_to", "crypto_path LIKE '%'")})
                AND role {kwargs.get("role", 'LIKE "%"')} AND start_min >= ?
                GROUP BY exchange1, exchange2, bank1, bank2, start_max, role ORDER BY profit DESC""",
                params).fetchall()

            return result


    def select_row(self, params):
        with self.connection:
            result = self.cursor.execute(
                f"""SELECT DISTINCT {params} FROM arbitrage ORDER BY {params}""").fetchall()
            return result

    def db_request(self, request):
        with self.connection:
            result = self.cursor.execute(
                f"""{request}""").fetchall()

            return result

    def addUser(self, name, email, hash):
        with self.connection:
            res = self.cursor.execute(f"SELECT COUNT(email) AS count FROM users WHERE email LIKE ?", (email, )).fetchone()
            print(res)
            if res[0] > 0:
                print('Пользователь с таким email уже существует')
                return False

            tm = math.floor(time.time())
            self.cursor.execute("INSERT INTO users(name, email, password, time) VALUES(?, ?, ?, ?)", (name, email, hash, tm))
            return True

    def getUser(self, user_id):
        try:
            res = self.cursor.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1").fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данныX из бд " + str(e))
        return False


    def getUserByEmail(self, email):
        try:
            res = self.cursor.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1").fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данныX из бд " + str(e))
        return False

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.cursor.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
        except sqlite3.Error as e:
            print("Оибка обновления аватара в БД: " + str(e))
            return False
        return True

import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли пользователь в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = (?)", (user_id,))
        return not bool(result.fetchone() is None)

    def get_balance(self, user_id):
        """Достаем баланс в базе по его user_id"""
        result = self.cursor.execute("select balance from users where user_id = (?)", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id: int):
        self.cursor.execute(
            "INSERT INTO users (user_id) VALUES(?);",
            (int(user_id),))
        return self.conn.commit()

    def add_info(self, name, city, phone, bithday, user_id):
        self.cursor.execute("UPDATE users SET name = ?, city = ?, ph_number = ?, bithday = ? WHERE user_id = ?",(name,city,phone,bithday,user_id))
        return self.conn.commit()

    def get_bithday(self, user_id):
        """Достаем баланс в базе по его user_id"""
        result = self.cursor.execute("select bithday from users where user_id = (?)", (user_id,))
        return result.fetchone()[0]

    def upd_status(self, status, count ,user_id):
        self.cursor.execute("UPDATE users SET status = ?, count = ? WHERE user_id = ?",
                            (status, count, user_id))
        return self.conn.commit()

    def get_status(self, user_id):
        """Достаем баланс в базе по его user_id"""
        result = self.cursor.execute("select status from users where user_id = (?)", (user_id,))
        return result.fetchone()[0]

    def get_count(self, user_id):
        """Достаем баланс в базе по его user_id"""
        result = self.cursor.execute("select count from users where user_id = (?)", (user_id,))
        return result.fetchone()[0]


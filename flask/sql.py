import mysql.connector
import datetime


class Database:
    def __init__(self, host: str, user: str, passwd: str, db_name: str):
        try:
            self.db = mysql.connector.connect(
                host=host,
                user=user,
                password=passwd,
                database=db_name
            )
            if self.db:
                print("数据库连接成功")
        except UserWarning:
            print("数据库连接失败")

    def createDatabase(self):
        cursor = self.db.cursor()
        sql = """
            CREATE DATABASE IF NOT EXISTS rental_mng;
            USE rental_mng;
        """
        cursor.execute(sql)
        cursor.close()

    def createTable(self):
        cursor = self.db.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                id              INT             NOT NULL    PRIMARY KEY,
                username        VARCHAR(50)     NOT NULL    UNIQUE,
                pwd_hash        VARCHAR(128)    NOT NULL,
                user_type       ENUM('user', 'operator') NOT NULL DEFAULT 'user'
            );
            
            CREATE TABLE IF NOT EXISTS user_info (
                username        VARCHAR(50)     NOT NULL    UNIQUE,
                id_number       VARCHAR(20)     NOT NULL,
                phone           VARCHAR(20)     NOT NULL,
                email           VARCHAR(100)    NOT NULL,
                contact_info    VARCHAR(50),
            
                foreign key (username) references users(username)
            );
            
            CREATE TABLE IF NOT EXISTS rental_info (
                rental_id       INT             NOT NULL    PRIMARY KEY AUTO_INCREMENT,
                publisher       VARCHAR(50)     NOT NULL,
                address         VARCHAR(255)    NOT NULL,
                area            DECIMAL(10, 2)  NOT NULL,
                floor           INT             NOT NULL,
                rent            DECIMAL(10, 2)  NOT NULL,
                house_type      VARCHAR(128)    NOT NULL,
                region          VARCHAR(128),
                orientation     VARCHAR(50),
                decoration      VARCHAR(128),
                surroundings    TEXT,
            
                foreign key (publisher) references users(username)
            ) AUTO_INCREMENT = 1000000;
            
            CREATE TABLE IF NOT EXISTS log(
                event_id        INT             NOT NULL    PRIMARY KEY AUTO_INCREMENT,
                time_stamp      TIMESTAMP       NOT NULL,
                username        VARCHAR(50)     NOT NULL,
                src_ip          VARCHAR(50)     NOT NULL,
                event           VARCHAR(20)     NOT NULL,
                note            VARCHAR(128),
                
                foreign key (username) references users(username)
            ) AUTO_INCREMENT = 1000000;
            
            INSERT INTO users
            VALUES ( '100000', 'guest', 'FFFFFFFF', 'user');
        """
        cursor.execute(sql)
        self.db.commit()
        print(cursor.fetchall())
        cursor.close()

    def get_maxUserId(self, isOperator=False):
        cursor = self.db.cursor()
        sql = """
            SELECT max(u.id) maxId
            FROM users AS u
            WHERE u.user_type='{0}'
        """.format('operator' if isOperator else 'user')
        print(sql, "executed.")
        cursor.execute(sql)
        result = cursor.fetchall()
        maxId = result[0][0]
        cursor.close()
        if type(maxId) is int:
            return maxId
        else:
            print("invalid user id.")
            return -1

    def insertUser(self, username, pwd_hash, isOperator=False):
        user_id = self.get_maxUserId(isOperator) + 1
        cursor = self.db.cursor()
        sql = """
            INSERT INTO users
            VALUES ({0}, '{1}', '{2}', '{3}')
        """.format(user_id, username, pwd_hash, 'operator' if isOperator else 'user')
        print(sql)
        cursor.execute(sql)
        self.db.commit()
        print("executed.")
        cursor.close()

    def insertUserInfo(self, username: str, id_number: str, phone: str, email: str, contact_info: str):
        cursor = self.db.cursor()
        sql = f"""
            INSERT INTO user_info(username, id_number, phone, email, contact_info)
            VALUES ('{username}', '{id_number}', '{phone}', '{email}', '{contact_info}');
        """
        cursor.execute(sql)
        self.db.commit()
        print(sql, "executed.")
        cursor.close()

    def insertRental(self, username: str, address: str, area: int, floor: int, rent: int, house_type: str,
                     orientation: str = '', decoration: str = '', region: str = '', surroundings: str = ''):
        cursor = self.db.cursor()
        sql = f"""
            INSERT INTO rental_info(
                publisher, address, area, floor, rent, house_type,
                region, orientation, decoration, surroundings
            )
            VALUES (
                '{username}', '{address}', {area}, {floor}, {rent}, '{house_type}',
                '{region}', '{orientation}', '{decoration}', '{surroundings}'
            )
        """
        try:
            cursor.execute(sql)
            self.db.commit()
            print(sql, "executed.")
        except UserWarning:
            print("insert rental info failed.")
        cursor.close()

    def insertLog(self, event: str, username: str, ip: str, note: str = ''):
        cursor = self.db.cursor()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = f"""
            INSERT INTO log(time_stamp, username, src_ip, event, note)
            VALUES ('{timestamp}', '{username}', '{ip}', '{event}', '{note}')
        """
        try:
            cursor.execute(sql)
            self.db.commit()
            # print(sql, "executed.")
        except UserWarning:
            print("insert log failed.")
        cursor.close()

    def updateRental(self, rentalID):
        cursor = self.db.cursor()
        pass
        # unfinished method
        sql = f"""
            UPDATE rental_info
            SET       
            WHERE renta_id = {rentalID}
        """
        try:
            cursor.execute(sql)
            self.db.commit()
        except UserWarning:
            print("update failed, sql:", sql)
        cursor.close()

    def getUsers(self, isOperator=False):
        cursor = self.db.cursor()
        sql = """
            SELECT username
            FROM users AS u
            WHERE u.user_type='{0}';
        """.format('operator' if isOperator else 'user')
        cursor.execute(sql)
        result: list = cursor.fetchall()
        cursor.close()
        userList = [item for row in result for item in row]
        # print("user list:", userList)
        return userList

    def getAllUsers(self):
        cursor = self.db.cursor()
        sql = """
            SELECT username
            FROM users
        """
        cursor.execute(sql)
        result: list = cursor.fetchall()
        cursor.close()
        userList = [item for row in result for item in row]
        # print("all user list:", userList)
        return userList

    # !!!this method is used getting user's phone and email but not all info
    def getUserInfo(self, username: str):
        cursor = self.db.cursor()
        sql = f"""
            SELECT phone, email
            FROM user_info
            WHERE username='{username}'
        """
        cursor.execute(sql)
        result: list = cursor.fetchall()
        cursor.close()
        info = [item for row in result for item in row]
        return info

    def getUserInfoByUsername(self, username):
        cursor = self.db.cursor()
        sql = f"""
            SELECT *
            FROM user_info
            WHERE username='{username}'
        """
        cursor.execute(sql)
        result: list = cursor.fetchall()
        cursor.close()
        info = [item for row in result for item in row]
        return info

    def getAllUserInfo(self):
        cursor = self.db.cursor()
        sql = f"""
            SELECT *
            FROM user_info, users
            WHERE user_info.username = users.username
            ORDER BY users.id
        """
        cursor.execute(sql)
        result: list = cursor.fetchall()
        cursor.close()
        return result

    def getLog(self):
        cursor = self.db.cursor()
        sql = """
            SELECT *
            FROM log
            ORDER BY event_id desc 
        """
        cursor.execute(sql)
        result: list = cursor.fetchall()
        cursor.close()
        return result

    def loginVerify(self, username: str, pwd_hash: str):
        cursor = self.db.cursor()
        sql = f"""
            SELECT pwd_hash
            FROM users AS u 
            WHERE u.username='{username}'
        """
        try:
            cursor.execute(sql)
            passwd = cursor.fetchall()
            cursor.close()
            return True if passwd[0][0] == pwd_hash else False
        except UserWarning:
            print("sql error")
            cursor.close()
            return False

    def getAllRentalInfo(self, publisher=''):
        cursor = self.db.cursor()
        if publisher == '':
            sql = """
                SELECT *
                FROM rental_info
            """
        elif publisher in self.getAllUsers():
            sql = f"""
                SELECT *
                FROM rental_info
                WHERE publisher = '{publisher}'
            """
        else:
            print(f"{publisher} dose not exist")
            return
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getRentalsById(self, rentalID):
        cursor = self.db.cursor()
        sql = f"""
            SELECT *
            FROM rental_info
            WHERE rental_id={rentalID}
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def delUser(self, userID):
        cursor = self.db.cursor()
        sql1 = f"""
            DELETE FROM rental_info
            WHERE publisher IN (SELECT username FROM users WHERE id = {userID});
        """
        cursor.execute(sql1)
        print(cursor.fetchall())
        self.db.commit()

        sql2 = f"""
            DELETE FROM user_info
            WHERE username IN (SELECT username FROM users WHERE id = {userID});
        """
        cursor.execute(sql2)
        print(cursor.fetchall())
        self.db.commit()
        sql3 = f"""
            DELETE FROM users
            WHERE id = {userID};
        """
        cursor.execute(sql3)
        print(cursor.fetchall())
        self.db.commit()
        cursor.close()

    def delRentalByID(self, rentalID):
        cursor = self.db.cursor()
        sql = f"""
            DELETE 
            FROM rental_info
            WHERE rental_id={rentalID}
        """
        cursor.execute(sql)
        print(cursor.fetchall())
        self.db.commit()
        cursor.close()

    def isOperator(self, username: str):
        cursor = self.db.cursor()
        sql = f"""
            SELECT user_type
            FROM users
            WHERE username='{username}'
        """
        cursor.execute(sql)
        result = cursor.fetchall()[0][0]
        cursor.close()
        return True if result == 'operator' else False

    def __del__(self):
        self.db.close()
        print("数据库连接已关闭")

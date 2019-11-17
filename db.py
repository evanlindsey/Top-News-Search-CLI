import binascii
import hashlib
import os
import sqlite3


class DB:
    '''DB class
    Provides methods for connecting to and querying the SQLite database.
    '''

    db_path = 'db.sqlite'

    @classmethod
    def sql_connect(cls):
        '''Connect to the SQLite database using credentials from class properties.

        Returns:
            Connection: The return value. Object to perform SQL actions on.
        '''
        return sqlite3.connect(cls.db_path)

    @classmethod
    def sql_command(cls, query, data):
        '''Execute the given query against the SQLite connection.

        Args:
            query: Target query to execute.
            data: Variables to inject in the query.
        '''
        cnx = cls.sql_connect()
        cursor = cnx.cursor()
        cursor.execute(query, data)
        cnx.commit()
        cursor.close()
        cnx.close()

    @classmethod
    def sql_select(cls, query, data):
        '''Execute the given select statement against the SQLite connection.

        Args:
            query: Target select statement to execute.
            data: Variables to inject in the select statement.

        Returns:
            list: The return value. Row results from the select statement.
        '''
        cnx = cls.sql_connect()
        cursor = cnx.cursor()
        cursor.execute(query, data)
        res = [x for x in cursor.fetchall()]
        cursor.close()
        cnx.close()
        return res

    @classmethod
    def get_salt(cls):
        '''Generate a random salt for use in the password hash.

        Returns:
            string: The return value. Hex value of the generated salt.
        '''
        salt = os.urandom(16)
        return str(binascii.hexlify(salt))

    @classmethod
    def hash_password(cls, password, salt):
        '''Create a password hash from the given password and salt.

        Args:
            password: Plain text password.
            salt: Salt in hex form.

        Returns:
            string: The return value. Resulting password hash.
        '''
        key = hashlib.pbkdf2_hmac(
            'sha256', password.encode(), salt.encode(), 100000)
        return str(binascii.hexlify(key))

    @classmethod
    def check_password(cls, password, hashed, salt):
        '''Check if the provided password matches the original password hash.

        Args:
            password: Plain text password.
            hashed: Hash of the original password.
            salt: Salt in hex form.

        Returns:
            boolean: The return value. Result of the password comparison.
        '''
        return cls.hash_password(password, salt) == hashed

    @classmethod
    def get_user(cls, username):
        '''Retrieve the row from the users table that matches the user name.

        Args:
            username: Target user name.

        Returns:
            list: The return value. Row result from the select statement.
        '''
        query = ('SELECT id, password, salt FROM users WHERE username = ?')
        data = (username,)
        return cls.sql_select(query, data)

    @classmethod
    def add_user(cls, username, password):
        '''Add a row to the users table using the given user name and password.

        Args:
            username: Desired user name.
            password: Hashed password.

        Returns:
            boolean: The return value. True if successful. False if error (such as user name taken).
        '''
        res = cls.get_user(username)
        if len(res) == 0:
            query = (
                'INSERT INTO users (username, password, salt) VALUES (?, ?, ?)')
            salt = cls.get_salt()
            password = cls.hash_password(password, salt)
            data = (username, password, salt)
            cls.sql_command(query, data)
            return True
        return False

    @classmethod
    def auth_user(cls, username, password):
        '''Retrieve the given user name from the users table and compare the passwords.

        Args:
            username: Target user name.
            password: Plain text password.

        Returns:
            int: The return value. User ID is successful. -1 if error (such as user not existing or password not matching).
        '''
        res = cls.get_user(username)
        if len(res) == 1:
            user_id = res[0][0]
            hashed = res[0][1]
            salt = res[0][2]
            if cls.check_password(password, hashed, salt):
                return user_id
        return -1

    @classmethod
    def get_articles(cls, user_id):
        '''Retrieve saved articles from the articles table for the given user ID.

        Args:
            user_id: Target user ID.

        Returns:
            dictionary: The return value. All resulting articles. Keys are article IDs. Values are pickled article objects.
        '''
        query = ('SELECT id, article FROM user_articles WHERE user_id = ?')
        data = (user_id,)
        res = cls.sql_select(query, data)
        res = [(x[0], x[1]) for x in res]
        return dict(enumerate(res))

    @classmethod
    def add_article(cls, user_id, article):
        '''Add a row to the articles table for the given user id using the given pickled article object.

        Args:
            user_id: Target user ID.
            article: Pickled article object.
        '''
        query = ('INSERT INTO user_articles (user_id, article) VALUES (?, ?)')
        data = (user_id, article)
        cls.sql_command(query, data)

    @classmethod
    def delete_article(cls, article_id):
        '''Delete a row from the articles table matching the given article id.

        Args:
            article_id: Target article ID.
        '''
        query = ('DELETE FROM user_articles WHERE id = ?')
        data = (article_id,)
        cls.sql_command(query, data)

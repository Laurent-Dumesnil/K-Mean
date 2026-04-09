import sqlite3

class DatabaseConnection():
    def __init__(self, db_name):
        self.__connection = None
        self.__cursor = None
        self.__db_name = db_name
        self.create_table()

    @property
    def connection(self):
        return self.__connection

    @property
    def cursor(self):
        return self.__cursor

    def __enter__(self):
        self.__connection = sqlite3.connect(self.__db_name)
        self.__cursor = self.__connection.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.__connection:
            if exc_type is None:
                self.__connection.commit()
            else:
                self.__connection.rollback()
            self.__cursor.close()
            self.__connection.close()
            self.__connection = None
            self.__cursor = None

    def create_table(self):
        try:
            with self as db:
                db.cursor.execute('PRAGMA foreign_keys = 1')
                db.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS words
                (
                    word TEXT PRIMARY KEY NOT NULL,
                    idx INTEGER UNIQUE NOT NULL
                )
                ''')

                db.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS coocurence
                (
                    word_1 INTEGER NOT NULL,
                    word_2 INTEGER NOT NULL,
                    window_size INTEGER NOT NULL,
                    coocurence_value INTEGER NOT NULL,
                    PRIMARY KEY (word_1, word_2, window_size),
                    FOREIGN KEY (word_1) REFERENCES words(word),
                    FOREIGN KEY (word_2) REFERENCES words(word)
                )
                ''')
        except Exception as e:
            print(e)

class DatabaseService():
    def __init__(self):
        self.__db = DatabaseConnection("ai_db")

    def add_words(self, datas:dict):
        if isinstance(datas, dict):
            try:
                with self.__db as db:
                    db.cursor.executemany('INSERT INTO words (word, idx) VALUES(?, ?)',  datas.items())
            except Exception as e:
                print(e)

    def get_words(self):
        try:
            with self.__db as db:
                db.cursor.execute('SELECT * FROM words')
                results = db.cursor.fetchall()
                return results
        except Exception as e:
            print(e)
    
    def get_coocurence(self, window_size):
        try:
            with self.__db as db:
                db.cursor.execute('SELECT word_1, word_2, coocurence_value FROM coocurence WHERE window_size = ?', (window_size,))
                results = db.cursor.fetchall()
                return results
        except Exception as e:
            print(e)
    
    def add_coocurence(self, datas:list):
        if isinstance(datas, list):
            try:
                with self.__db as db:
                    db.cursor.executemany('INSERT OR REPLACE INTO coocurence (word_1, word_2, window_size, coocurence_value) VALUES(?, ?, ?, ?)', [(word_1, word_2, window, value) for word_1, word_2, window, value in datas])
            except Exception as e:
                print(e)

    def delete_from(self):
        try:
            with self.__db as db:
                db.cursor.execute("DELETE FROM coocurence")
                db.cursor.execute("DELETE FROM words")
        except Exception as e:
            print(e)
import sqlite3

class DatabaseConnection():
    def __init__(self):
        self.__connection = None
        self.__cursor = None
        self.__db_name = "ai_db"

    @property
    def connection(self):
        return self.__connection

    @property
    def cursor(self):
        return self.__cursor

    def __enter__(self):
        self.__connection = sqlite3.connect(self.__db_name)
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute('PRAGMA foreign_keys = 1')
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

class DatabaseService():
    def add_words(self, datas:dict):
        if isinstance(datas, dict):
            try:
                with DatabaseConnection() as db:
                    db.cursor.executemany('INSERT INTO words (word, idx) VALUES(?, ?)',  datas.items())
            except Exception as e:
                print(e)

    def get_words(self):
        try:
            with DatabaseConnection() as db:
                db.cursor.execute('SELECT * FROM words')
                results = db.cursor.fetchall()
                return results
        except Exception as e:
            print(e)
    
    def get_coocurence(self, window_size):
        try:
            with DatabaseConnection() as db:
                db.cursor.execute('SELECT word_1, word_2, coocurence_value FROM coocurence WHERE window_size = ?', (window_size,))
                results = db.cursor.fetchall()
                return results
        except Exception as e:
            print(e)
    
    def add_coocurence(self, datas:list):
        if isinstance(datas, list):
            try:
                with DatabaseConnection() as db:
                    db.cursor.executemany('INSERT OR REPLACE INTO coocurence (word_1, word_2, window_size, coocurence_value) VALUES(?, ?, ?, ?)', [(word_1, word_2, window, value) for word_1, word_2, window, value in datas])
            except Exception as e:
                print(e)

    def delete_from(self):
        try:
            with DatabaseConnection() as db:
                db.cursor.execute("DELETE FROM coocurence")
                db.cursor.execute("DELETE FROM words")
        except Exception as e:
            print(e)

    def create_table(self):
        try:
            with DatabaseConnection() as db:
                db.cursor.execute("DROP TABLE IF EXISTS cooccurence")
                db.cursor.execute("DROP TABLE IF EXISTS words")
                db.cursor.execute('''
                    
                    CREATE TABLE words
                (
                    word TEXT PRIMARY KEY NOT NULL,
                    idx INTEGER UNIQUE NOT NULL
                )
                ''')

                db.cursor.execute('''
                    
                    CREATE TABLE coocurence
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
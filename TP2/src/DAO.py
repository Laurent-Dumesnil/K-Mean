import sqlite3
from abc import ABC

class DatabaseConnection(ABC):
    def get_connection(self):
        connection = sqlite3.connect("ai2.db")
        return connection
    
    def create_table(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = 1')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words
        (
            word INTEGER PRIMARY KEY NOT NULL,
            idx INTEGER UNIQUE NOT NULL
        )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coocurence
        (
            word_1 INTEGER NOT NULL,
            word_2 INTEGER NOT NULL,
            window_size INTEGER NOT NULL,
            coocurence_value INTEGER NOT NULL,
            PRIMARY KEY (word_1, word_2, window_size)
            FOREIGN KEY (word_1) REFERENCES words(word)
            FOREIGN KEY (word_2) REFERENCES words(word)
        )
        ''')
        connection.commit()
        connection.close()

class DataManager(DatabaseConnection):
    def __init__(self):
        self.create_table()

    def add_words(self, datas:dict):
        if isinstance(datas, dict):
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.executemany('INSERT INTO words (word, idx) VALUES(?, ?)',  datas.items())
            connection.commit()
            connection.close()

    def get_words(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM words')
        results = cursor.fetchall()
        connection.close()
        return results
    
    def get_coocurence(self, window_size):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT word_1, word_2, coocurence_value FROM coocurence WHERE window_size = ?', (window_size,))
        results = cursor.fetchall()
        connection.close()
        return results
    
    def add_coocurence(self, datas:list):
        if isinstance(datas, list):
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.executemany('INSERT INTO coocurence_value (word_1, word_2, window_size, coocurence_value) VALUES(?, ?, ?, ?)', [(word_1, word_2, window, value) for word_1, word_2, window, value in datas])
            connection.commit()
            connection.close()

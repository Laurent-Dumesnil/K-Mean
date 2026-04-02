import sqlite3
from abc import ABC

class DatabaseConnection(ABC):
    def get_connection(self):
        connexion = sqlite3.connect("ai2.db")
        return connexion
    
    def create_table(self):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute('PRAGMA foreign_keys = 1')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words
        (
            word TEXT PRIMARY KEY NOT NULL,
            idx INTEGER UNIQUE NOT NULL
        )
        ''')
        connexion.commit()
        connexion.close()

class DataManager(DatabaseConnection):
    def __init__(self):
        self.create_table()

    def add_words(self, datas:dict):
        if isinstance(datas, dict):
            connexion = self.get_connection()
            cursor = connexion.cursor()
            cursor.executemany('INSERT INTO words (word, idx) VALUES(?, ?)',  [(mot, idx) for mot,idx in datas.items()])
            connexion.commit()
            connexion.close()

    def get_words(self):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute('SELECT * FROM words')
        result = cursor.fetchall()
        connexion.close()
        return result
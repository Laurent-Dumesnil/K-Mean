import sqlite3

class DatabaseConnection():
    @staticmethod
    def get_connection():
        connexion = sqlite3.connect("ai2.db")
        return connexion
    
    @staticmethod
    def create_table():
        connexion = DatabaseConnection.get_connection()
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

class DataManager():
    @staticmethod
    def add_words(datas:dict):
        if isinstance(datas, dict):
            connexion = DatabaseConnection.get_connection()
            cursor = connexion.cursor()
            cursor.executemany('INSERT INTO words (word, idx) VALUES(?, ?)', datas.items())
            connexion.commit()
            connexion.close()

    @staticmethod
    def get_words():
        connexion = DatabaseConnection.get_connection()
        cursor = connexion.cursor()
        cursor.execute('SELECT * FROM words')
        result = cursor.fetchall()
        connexion.close()
        return result
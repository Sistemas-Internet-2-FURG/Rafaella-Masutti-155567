import sqlite3
from src.config.config import nomeBanco

conexao = sqlite3.connect(f"{nomeBanco}.db")
cursor = conexao.cursor()

cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    usuario TEXT UNIQUE NOT NULL,
                                    nome TEXT NOT NULL, 
                                    senha TEXT NOT NULL
                                    )
                ''')

cursor.execute('''
                CREATE TABLE IF NOT EXISTS animais(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    dono INTEGER NOT NULL,
                                    foto TEXT,
                                    nome TEXT NOT NULL, 
                                    especie TEXT NOT NULL,
                                    FOREIGN KEY (dono) REFERENCES usuarios(id) ON DELETE CASCADE
                                    )
                ''')

conexao.commit()
conexao.close()
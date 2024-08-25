import sqlite3

conexao = sqlite3.connect("animaisEstimacao.db")
cursor = conexao.cursor()

cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    usuario TEXT UNIQUE,
                                    nome TEXT, 
                                    senha TEXT
                                    )
                ''')

cursor.execute('''
                CREATE TABLE IF NOT EXISTS animais(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    dono TEXT,
                                    foto TEXT,
                                    nome TEXT, 
                                    especie TEXT,
                                    FOREIGN KEY (dono) REFERENCES usuarios(usuario) ON DELETE SET NULL
                                    )
                ''')

conexao.commit()
conexao.close()
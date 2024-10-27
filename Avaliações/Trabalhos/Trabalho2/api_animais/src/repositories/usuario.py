import sqlite3, os
from src.config.config import nomeBanco

dbpath = os.path.join(os.path.dirname(__file__), f"../../{nomeBanco}.db")

def criarUsuario(usuario):
    try:
        conexao = sqlite3.connect(dbpath)
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, nome, senha) VALUES (?, ?, ?)", (usuario["usuario"], usuario["nome"], usuario["senha"]))
        ultimoId = cursor.lastrowid
        conexao.commit()
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: usuarios.usuario" in str(e):
            return None, 409
    except sqlite3.DatabaseError as e:
        return None, f"Erro de banco de dados: {e}"
    finally:
        if conexao:
            conexao.close()
    return ultimoId, None

def buscarSenhaEId(usuario):
    try:
        conexao = sqlite3.connect(dbpath)
        cursor = conexao.cursor()
        cursor.execute("SELECT id, senha FROM usuarios WHERE usuario = ?", (usuario, ))
        senhaEId = cursor.fetchone()
    except sqlite3.DatabaseError as e:
        return None, None, f"Erro de banco de dados: {e}"
    finally:
        if conexao:
            conexao.close()
    if senhaEId == None:
        return None, None, None
    return senhaEId[1], senhaEId[0], None

def buscarUsuario(id):
    try:
        conexao = sqlite3.connect(dbpath)
        conexao.row_factory=sqlite3.Row
        cursor = conexao.cursor()
        cursor.execute("SELECT usuario, nome FROM usuarios WHERE id = ?", (id,))
        usuario = cursor.fetchone()
    except sqlite3.DatabaseError as e:
        return None, f"Erro de banco de dados: {e}"
    finally:
        if conexao:
            conexao.close()
    if usuario == None:
        return None, None
    return dict(usuario), None
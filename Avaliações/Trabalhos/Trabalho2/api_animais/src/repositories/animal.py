import sqlite3, os
from src.config.config import nomeBanco

dbpath = os.path.join(os.path.dirname(__file__), f"../../{nomeBanco}.db")

def criarAnimal(animal, dono):
    try:
        conexao = sqlite3.connect(dbpath)
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO animais (dono, foto, nome, especie) VALUES (?, ?, ?, ?)", (dono, animal["foto"], animal["nome"], animal["especie"]))
        ultimoId = cursor.lastrowid
        conexao.commit()
    except sqlite3.DatabaseError as e:
        return None, f"Erro de banco de dados: {e}"
    finally:
        if conexao:
            conexao.close()
    return ultimoId, None

def buscarAnimais(dono):
    try:
        conexao = sqlite3.connect(dbpath)
        conexao.row_factory=sqlite3.Row
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM animais WHERE dono=?", (dono,))
        animal = cursor.fetchall()
    except sqlite3.DatabaseError as e:
        return None, f"Erro de banco de dados: {e}"
    finally:
        if conexao:
            conexao.close()
    if animal:
        animais = []
        for linha in animal:
            animais.append(dict(linha))
        return animais, None
    return None, None

def buscarAnimal(id):
    try:
        conexao = sqlite3.connect(dbpath)
        conexao.row_factory=sqlite3.Row
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM animais WHERE id=?", (id,))
        animal = cursor.fetchone()
    except sqlite3.DatabaseError as e:
        return None, f"Erro de banco de dados: {e}"
    finally:
        if conexao:
            conexao.close()
    if animal != None:
        return dict(animal), None
    return None, None

def buscarDono(id):
    try:
        conexao = sqlite3.connect(dbpath)
        conexao.row_factory=sqlite3.Row
        cursor = conexao.cursor()
        cursor.execute("SELECT dono FROM animais WHERE id=?", (id,))
        dono = cursor.fetchone()
    except sqlite3.DatabaseError as e:
        return None, f"Erro de banco de dados: {e}"
    finally:
        if conexao:
            conexao.close()
    if dono != None:
        return dono[0], None
    return None, None

def editarAnimal(dados, id):
    try:
        conexao = sqlite3.connect(dbpath)
        cursor = conexao.cursor()
        cursor.execute("UPDATE animais SET foto=?, nome=?, especie=? WHERE id=?", (dados["foto"], dados["nome"], dados["especie"], id))
        conexao.commit()
    except sqlite3.DatabaseError as e:
        return None, f"Erro de banco de dados: {e}"
    finally:
        if conexao:
            conexao.close()
    return None, None

def apagarAnimal(id):
    try:
        conexao = sqlite3.connect(dbpath)
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM animais WHERE id=?", (id,))
        linhasDeletadas = cursor.rowcount
        conexao.commit()
    except sqlite3.DatabaseError as e:
        return None, f"Erro de banco de dados: {e}"
    finally:
        if conexao:
            conexao.close()
    if linhasDeletadas > 0:
        return 1, None
    return None, None
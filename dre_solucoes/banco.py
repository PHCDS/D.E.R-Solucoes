import sqlite3

ARQUIVO = "dre.db"


def conectar():
    con = sqlite3.connect(ARQUIVO)
    con.execute("PRAGMA foreign_keys = ON")
    return con

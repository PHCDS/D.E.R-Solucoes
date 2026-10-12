# DER06 - Selecionar no imóvel os equipamentos que existem na residência
from banco import conectar
from der05_equipamentos import listar_equipamentos, mostrar_equipamentos
from der07_uso import pedir_quantidade, pedir_horas


# T05 - tabela que liga imóvel e equipamento
def criar_tabela_imovel_equipamento():
    con = conectar()
    con.execute("""
        CREATE TABLE IF NOT EXISTS imovel_equipamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imovel_id INTEGER NOT NULL,
            equipamento_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            horas_dia REAL NOT NULL,
            FOREIGN KEY (imovel_id) REFERENCES imovel(id) ON DELETE CASCADE,
            FOREIGN KEY (equipamento_id) REFERENCES equipamento(id)
        )
    """)
    con.commit()
    con.close()


def salvar_item(imovel_id, equipamento_id, quantidade, horas):
    con = conectar()
    con.execute("""INSERT INTO imovel_equipamento (imovel_id, equipamento_id, quantidade, horas_dia)
                   VALUES (?, ?, ?, ?)""", (imovel_id, equipamento_id, quantidade, horas))
    con.commit()
    con.close()


# T02 - busca por nome ou categoria
def buscar_equipamentos(termo):
    con = conectar()
    lista = con.execute(
        "SELECT id, nome, categoria, potencia_w FROM equipamento "
        "WHERE nome LIKE ? OR categoria LIKE ? ORDER BY nome",
        (f"%{termo}%", f"%{termo}%")).fetchall()
    con.close()
    return lista


# T03 - só aceita o que está na base
def buscar_equipamento(equipamento_id):
    con = conectar()
    eq = con.execute("SELECT id, nome, categoria, potencia_w FROM equipamento WHERE id = ?",
                     (equipamento_id,)).fetchone()
    con.close()
    return eq


# T01 + T04 - tela de seleção, dá pra adicionar vários em seguida
def tela_adicionar_equipamentos(imovel_id):
    while True:
        print("\n--- ADICIONAR EQUIPAMENTO ---")
        termo = input("Buscar por nome ou categoria (Enter mostra todos): ").strip()
        if termo == "":
            mostrar_equipamentos(listar_equipamentos())
        else:
            mostrar_equipamentos(buscar_equipamentos(termo))

        texto = input("Número do equipamento: ").strip()
        equipamento = None
        if texto.isdigit():
            equipamento = buscar_equipamento(int(texto))

        if equipamento is None:
            print("Esse equipamento não está na base.")
        else:
            qtd = pedir_quantidade()
            horas = pedir_horas()
            salvar_item(imovel_id, equipamento[0], qtd, horas)
            print(f"{equipamento[1]} adicionado.")

        if input("Adicionar outro? (s/n): ").strip().lower() != "s":
            break

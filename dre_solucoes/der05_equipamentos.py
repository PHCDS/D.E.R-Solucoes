# DER05 - Ter uma base de equipamentos elétricos para o usuário escolher
from banco import conectar


# T01 - tabela de equipamento
def criar_tabela_equipamento():
    con = conectar()
    con.execute("""
        CREATE TABLE IF NOT EXISTS equipamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            potencia_w REAL NOT NULL CHECK (potencia_w > 0)
        )
    """)
    con.commit()
    con.close()


# T02 - equipamentos mais comuns (potência média em W)
BASE_INICIAL = [
    ("Geladeira", "Cozinha", 250),
    ("Micro-ondas", "Cozinha", 1200),
    ("Air fryer", "Cozinha", 1500),
    ("Liquidificador", "Cozinha", 300),
    ("Cafeteira elétrica", "Cozinha", 600),
    ("Chuveiro elétrico", "Banheiro", 5500),
    ("Secador de cabelo", "Banheiro", 1500),
    ("Ar-condicionado 9000 BTUs", "Climatização", 900),
    ("Ventilador", "Climatização", 100),
    ("Lâmpada LED", "Iluminação", 9),
    ("Lâmpada fluorescente", "Iluminação", 15),
    ("TV LED", "Eletrônicos", 120),
    ("Computador", "Eletrônicos", 300),
    ("Notebook", "Eletrônicos", 65),
    ("Carregador de celular", "Eletrônicos", 10),
    ("Roteador Wi-Fi", "Eletrônicos", 12),
    ("Máquina de lavar", "Lavanderia", 500),
    ("Ferro de passar", "Lavanderia", 1000),
]


def popular_base():
    con = conectar()
    qtd = con.execute("SELECT COUNT(*) FROM equipamento").fetchone()[0]
    if qtd == 0:
        con.executemany("INSERT INTO equipamento (nome, categoria, potencia_w) VALUES (?, ?, ?)",
                        BASE_INICIAL)
        con.commit()
    con.close()


# T03 - listagem com filtro por categoria
def listar_categorias():
    con = conectar()
    linhas = con.execute("SELECT DISTINCT categoria FROM equipamento ORDER BY categoria").fetchall()
    con.close()
    return [linha[0] for linha in linhas]


def listar_equipamentos(categoria=None):
    con = conectar()
    if categoria is None:
        lista = con.execute(
            "SELECT id, nome, categoria, potencia_w FROM equipamento ORDER BY categoria, nome").fetchall()
    else:
        lista = con.execute(
            "SELECT id, nome, categoria, potencia_w FROM equipamento WHERE categoria = ? ORDER BY nome",
            (categoria,)).fetchall()
    con.close()
    return lista


def mostrar_equipamentos(lista):
    if not lista:
        print("Nenhum equipamento encontrado.")
    for eq in lista:
        print(f"[{eq[0]}] {eq[1]} ({eq[2]}) - {eq[3]:.0f} W")


def tela_base_equipamentos():
    categorias = listar_categorias()
    print("\n--- BASE DE EQUIPAMENTOS ---")
    print("0 - Todas")
    for i, cat in enumerate(categorias, start=1):
        print(f"{i} - {cat}")
    op = input("Filtrar por: ").strip()
    if op.isdigit() and 1 <= int(op) <= len(categorias):
        mostrar_equipamentos(listar_equipamentos(categorias[int(op) - 1]))
    else:
        mostrar_equipamentos(listar_equipamentos())

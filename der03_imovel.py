# DER03 - Cadastrar o imóvel para o dimensionamento energético
from banco import conectar

TIPOS = ["Casa", "Apartamento", "Outro"]


# T01 - tabela de imóvel ligada ao usuário
def criar_tabela_imovel():
    con = conectar()
    con.execute("""
        CREATE TABLE IF NOT EXISTS imovel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            tipo TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuario(id)
        )
    """)
    con.commit()
    con.close()


# T03 - campos obrigatórios
def validar_imovel(nome, endereco, tipo):
    if nome == "" or endereco == "":
        return "Nome e endereço são obrigatórios."
    if tipo not in TIPOS:
        return "Tipo inválido."
    return None


def escolher_tipo():
    for i, tipo in enumerate(TIPOS, start=1):
        print(f"{i} - {tipo}")
    op = input("Tipo: ").strip()
    if op.isdigit() and 1 <= int(op) <= len(TIPOS):
        return TIPOS[int(op) - 1]
    return ""


# T04 - salvar e mostrar na lista
def salvar_imovel(usuario_id, nome, endereco, tipo):
    con = conectar()
    con.execute("INSERT INTO imovel (usuario_id, nome, endereco, tipo) VALUES (?, ?, ?, ?)",
                (usuario_id, nome, endereco, tipo))
    con.commit()
    con.close()


def listar_imoveis(usuario_id):
    con = conectar()
    imoveis = con.execute(
        "SELECT id, nome, endereco, tipo FROM imovel WHERE usuario_id = ? ORDER BY id",
        (usuario_id,)).fetchall()
    con.close()
    return imoveis


def mostrar_imoveis(usuario_id):
    imoveis = listar_imoveis(usuario_id)
    print("\n--- MEUS IMÓVEIS ---")
    if not imoveis:
        print("Nenhum imóvel cadastrado ainda.")
    for im in imoveis:
        print(f"[{im[0]}] {im[1]} - {im[3]} - {im[2]}")


def buscar_imovel(imovel_id, usuario_id):
    # só encontra se o imóvel for do usuário logado
    con = conectar()
    imovel = con.execute(
        "SELECT id, nome, endereco, tipo FROM imovel WHERE id = ? AND usuario_id = ?",
        (imovel_id, usuario_id)).fetchone()
    con.close()
    return imovel


# T02 - formulário
def tela_cadastrar_imovel(usuario_id):
    print("\n--- NOVO IMÓVEL ---")
    nome = input("Nome (ex: Casa da praia): ").strip()
    endereco = input("Endereço: ").strip()
    tipo = escolher_tipo()

    erro = validar_imovel(nome, endereco, tipo)
    if erro:
        print(erro)
        return
    salvar_imovel(usuario_id, nome, endereco, tipo)
    print("Imóvel cadastrado!")
    # a lista aparece de novo, já com ele, quando volta pro menu de imóveis

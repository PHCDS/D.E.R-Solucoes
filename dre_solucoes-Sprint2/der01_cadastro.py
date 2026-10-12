# DER01 - Criar um cadastro com e-mail para salvar imóveis e análises
import hashlib
from banco import conectar


# T01 - tabela de usuário no banco
def criar_tabela_usuario():
    con = conectar()
    con.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()


def gerar_hash(senha):
    # a senha não fica pura no banco
    return hashlib.sha256(senha.encode()).hexdigest()


# T03 - validações
def email_valido(email):
    if email.count("@") != 1 or " " in email:
        return False
    usuario, dominio = email.split("@")
    if usuario == "" or "." not in dominio:
        return False
    if dominio.startswith(".") or dominio.endswith("."):
        return False
    return True


def email_existe(email):
    con = conectar()
    linha = con.execute("SELECT id FROM usuario WHERE email = ?", (email,)).fetchone()
    con.close()
    return linha is not None


def validar_cadastro(nome, email, senha):
    if nome == "":
        return "O nome é obrigatório."
    if not email_valido(email):
        return "E-mail inválido."
    if len(senha) < 6:
        return "A senha precisa ter pelo menos 6 caracteres."
    if email_existe(email):
        return "Já existe um cadastro com esse e-mail."
    return None


def salvar_usuario(nome, email, senha):
    con = conectar()
    con.execute("INSERT INTO usuario (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, gerar_hash(senha)))
    con.commit()
    con.close()


# T02 - tela de cadastro
def tela_cadastro():
    print("\n--- CADASTRO ---")
    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip().lower()
    senha = input("Senha: ")

    erro = validar_cadastro(nome, email, senha)
    if erro:
        print(erro)
        return
    salvar_usuario(nome, email, senha)
    print("Cadastro feito! Agora é só entrar.")

# T04 - testes no arquivo testes.py

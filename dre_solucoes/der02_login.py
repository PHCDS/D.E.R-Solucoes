# DER02 - Ter acesso aos imóveis cadastrados
from banco import conectar
from der01_cadastro import gerar_hash


# T02 - compara e-mail e senha com o que está no banco
def autenticar(email, senha):
    con = conectar()
    usuario = con.execute(
        "SELECT id, nome FROM usuario WHERE email = ? AND senha = ?",
        (email, gerar_hash(senha))).fetchone()
    con.close()
    return usuario  # (id, nome) ou None


# T01 - tela de login
def tela_login():
    print("\n--- LOGIN ---")
    email = input("E-mail: ").strip().lower()
    senha = input("Senha: ")

    usuario = autenticar(email, senha)
    if usuario is None:
        # T04 - mensagem de erro
        print("E-mail ou senha incorretos.")
        return None
    print(f"Bem-vindo, {usuario[1]}!")
    return usuario

# T03 - quando o login dá certo, o main.py leva direto pra lista de imóveis

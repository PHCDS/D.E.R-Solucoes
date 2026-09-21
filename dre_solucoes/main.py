# D.R.E Soluções - projeto completo (DER01 a DER10)
from der01_cadastro import criar_tabela_usuario, tela_cadastro
from der02_login import tela_login
from der03_imovel import criar_tabela_imovel, tela_cadastrar_imovel, mostrar_imoveis, buscar_imovel
from der04_editar_imovel import tela_editar_imovel, tela_excluir_imovel
from der05_equipamentos import criar_tabela_equipamento, popular_base, tela_base_equipamentos
from der06_selecao import criar_tabela_imovel_equipamento, tela_adicionar_equipamentos
from der08_consumo import mostrar_consumos
from der09_total import mostrar_total
from der10_editar_equipamento import tela_editar_item, tela_remover_item


def preparar_banco():
    criar_tabela_usuario()
    criar_tabela_imovel()
    criar_tabela_equipamento()
    criar_tabela_imovel_equipamento()
    popular_base()


def menu_imovel(imovel):
    while True:
        print(f"\n===== {imovel[1]} ({imovel[3]}) =====")
        mostrar_consumos(imovel[0])
        mostrar_total(imovel[0])
        print("\n1 - Adicionar equipamentos")
        print("2 - Editar equipamento")
        print("3 - Remover equipamento")
        print("4 - Ver base de equipamentos")
        print("0 - Voltar")
        op = input("Opção: ").strip()

        if op == "1":
            tela_adicionar_equipamentos(imovel[0])
        elif op == "2":
            tela_editar_item(imovel[0])
        elif op == "3":
            tela_remover_item(imovel[0])
        elif op == "4":
            tela_base_equipamentos()
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def menu_imoveis(usuario):
    usuario_id = usuario[0]
    while True:
        mostrar_imoveis(usuario_id)
        print("\n1 - Cadastrar imóvel")
        print("2 - Abrir imóvel")
        print("3 - Editar imóvel")
        print("4 - Excluir imóvel")
        print("0 - Sair da conta")
        op = input("Opção: ").strip()

        if op == "1":
            tela_cadastrar_imovel(usuario_id)
        elif op == "2":
            texto = input("Número do imóvel: ").strip()
            imovel = buscar_imovel(int(texto), usuario_id) if texto.isdigit() else None
            if imovel is None:
                print("Imóvel não encontrado.")
            else:
                menu_imovel(imovel)
        elif op == "3":
            tela_editar_imovel(usuario_id)
        elif op == "4":
            tela_excluir_imovel(usuario_id)
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def main():
    preparar_banco()
    while True:
        print("\n===== D.R.E SOLUÇÕES =====")
        print("1 - Criar conta")
        print("2 - Entrar")
        print("0 - Sair")
        op = input("Opção: ").strip()

        if op == "1":
            tela_cadastro()
        elif op == "2":
            usuario = tela_login()
            # DER02 T03 - login certo vai direto pra lista de imóveis
            if usuario:
                menu_imoveis(usuario)
        elif op == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

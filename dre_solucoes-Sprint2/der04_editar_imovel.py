# DER04 - Excluir e editar imóveis cadastrados
from banco import conectar
from der03_imovel import buscar_imovel, validar_imovel, escolher_tipo


# T03 - confirmação antes de qualquer alteração
def confirmar(mensagem):
    resposta = input(mensagem + " (s/n): ").strip().lower()
    return resposta == "s"


def editar_imovel(imovel_id, nome, endereco, tipo):
    con = conectar()
    con.execute("UPDATE imovel SET nome = ?, endereco = ?, tipo = ? WHERE id = ?",
                (nome, endereco, tipo, imovel_id))
    con.commit()
    con.close()


def excluir_imovel(imovel_id):
    # os equipamentos do imóvel saem junto (ON DELETE CASCADE)
    con = conectar()
    con.execute("DELETE FROM imovel WHERE id = ?", (imovel_id,))
    con.commit()
    con.close()


def pedir_imovel(usuario_id):
    texto = input("Número do imóvel: ").strip()
    imovel = None
    if texto.isdigit():
        imovel = buscar_imovel(int(texto), usuario_id)
    if imovel is None:
        print("Imóvel não encontrado.")
    return imovel


# T02 - edição com os dados já preenchidos
def tela_editar_imovel(usuario_id):
    imovel = pedir_imovel(usuario_id)
    if imovel is None:
        return

    print("Aperte Enter para manter o valor atual.")
    nome = input(f"Nome [{imovel[1]}]: ").strip() or imovel[1]
    endereco = input(f"Endereço [{imovel[2]}]: ").strip() or imovel[2]
    print(f"Tipo atual: {imovel[3]}")
    tipo = escolher_tipo() or imovel[3]

    erro = validar_imovel(nome, endereco, tipo)
    if erro:
        print(erro)
        return
    if confirmar("Salvar as alterações?"):
        editar_imovel(imovel[0], nome, endereco, tipo)
        print("Imóvel atualizado.")
    else:
        print("Nada foi alterado.")


def tela_excluir_imovel(usuario_id):
    imovel = pedir_imovel(usuario_id)
    if imovel is None:
        return
    if confirmar(f"Excluir '{imovel[1]}' e todos os equipamentos dele?"):
        excluir_imovel(imovel[0])
        print("Imóvel excluído.")
    else:
        print("Exclusão cancelada.")

# T01 - as opções de editar e excluir ficam no menu de imóveis (main.py)
# T04 - testes no arquivo testes.py

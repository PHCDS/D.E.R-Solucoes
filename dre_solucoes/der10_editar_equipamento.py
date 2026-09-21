# DER10 - Editar ou remover um equipamento já lançado no imóvel
from banco import conectar
from der04_editar_imovel import confirmar
from der07_uso import pedir_quantidade, pedir_horas


def buscar_item(item_id, imovel_id):
    con = conectar()
    item = con.execute("""
        SELECT ie.id, e.nome, ie.quantidade, ie.horas_dia
        FROM imovel_equipamento ie
        JOIN equipamento e ON e.id = ie.equipamento_id
        WHERE ie.id = ? AND ie.imovel_id = ?
    """, (item_id, imovel_id)).fetchone()
    con.close()
    return item


def pedir_item(imovel_id):
    texto = input("Número do equipamento na lista: ").strip()
    item = None
    if texto.isdigit():
        item = buscar_item(int(texto), imovel_id)
    if item is None:
        print("Equipamento não encontrado nesse imóvel.")
    return item


def editar_item(item_id, quantidade, horas):
    con = conectar()
    con.execute("UPDATE imovel_equipamento SET quantidade = ?, horas_dia = ? WHERE id = ?",
                (quantidade, horas, item_id))
    con.commit()
    con.close()


def remover_item(item_id):
    con = conectar()
    con.execute("DELETE FROM imovel_equipamento WHERE id = ?", (item_id,))
    con.commit()
    con.close()


# T02 - alterar quantidade e horas
def tela_editar_item(imovel_id):
    item = pedir_item(imovel_id)
    if item is None:
        return
    print(f"{item[1]}: hoje está com {item[2]} un. e {item[3]:g} h/dia")
    qtd = pedir_quantidade()
    horas = pedir_horas()
    editar_item(item[0], qtd, horas)
    print("Equipamento atualizado.")


# T03 - confirmação antes de remover
def tela_remover_item(imovel_id):
    item = pedir_item(imovel_id)
    if item is None:
        return
    if confirmar(f"Remover {item[1]} do imóvel?"):
        remover_item(item[0])
        print("Equipamento removido.")
    else:
        print("Remoção cancelada.")

# T01 - as opções de editar e remover ficam no menu do imóvel (main.py)
# T04 - o consumo e o total são calculados direto do banco toda vez que a tela
#       do imóvel aparece, então logo depois da alteração o valor novo já sai

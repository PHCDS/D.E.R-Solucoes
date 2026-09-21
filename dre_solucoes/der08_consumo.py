# DER08 - Ver o consumo médio mensal estimado de cada equipamento
from banco import conectar

DIAS_MES = 30


# T01 + T02 - fórmula e arredondamento
def calcular_consumo(potencia_w, quantidade, horas_dia):
    kwh = potencia_w * quantidade * horas_dia * DIAS_MES / 1000
    return round(kwh, 2)


def listar_itens(imovel_id):
    con = conectar()
    itens = con.execute("""
        SELECT ie.id, e.nome, e.potencia_w, ie.quantidade, ie.horas_dia
        FROM imovel_equipamento ie
        JOIN equipamento e ON e.id = ie.equipamento_id
        WHERE ie.imovel_id = ?
        ORDER BY ie.id
    """, (imovel_id,)).fetchall()
    con.close()
    return itens


# T03 - mostra o kWh/mês de cada equipamento
def mostrar_consumos(imovel_id):
    itens = listar_itens(imovel_id)
    print("\n--- CONSUMO POR EQUIPAMENTO ---")
    if not itens:
        print("Nenhum equipamento lançado.")
    for item in itens:
        consumo = calcular_consumo(item[2], item[3], item[4])
        print(f"[{item[0]}] {item[1]} | {item[3]} un. x {item[4]:g} h/dia | {consumo:.2f} kWh/mês")

# T04 - testes no arquivo testes.py

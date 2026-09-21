# DER09 - Ver o consumo total médio mensal do imóvel
from der08_consumo import listar_itens, calcular_consumo


# T01 - soma de todos os equipamentos
def calcular_total(imovel_id):
    total = 0
    for item in listar_itens(imovel_id):
        total += calcular_consumo(item[2], item[3], item[4])
    # T03 - sem equipamento o for não roda e o total fica 0
    return round(total, 2)


# T02 - mostra o total
def mostrar_total(imovel_id):
    print(f"CONSUMO TOTAL: {calcular_total(imovel_id):.2f} kWh/mês")

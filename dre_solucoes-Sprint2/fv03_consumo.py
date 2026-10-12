# FV03 - Usar o consumo que o sistema já calculou para o imóvel
from der09_total import calcular_total


# T01 + T02 + T03
def definir_consumo_referencia(imovel_id):
    consumo = calcular_total(imovel_id)
    print(f"\nConsumo calculado para esse imóvel: {consumo:.2f} kWh/mês")

    if consumo == 0:
        print("O imóvel ainda não tem equipamento lançado.")

    texto = input("Enter usa esse valor, ou digite outro consumo em kWh/mês: ").strip()
    if texto == "":
        if consumo == 0:
            print("Sem consumo não dá para dimensionar. Cadastre os equipamentos primeiro.")
            return None
        return consumo

    try:
        outro = float(texto.replace(",", "."))
    except ValueError:
        print("Valor inválido.")
        return None
    if outro <= 0:
        print("O consumo tem que ser maior que zero.")
        return None
    return outro

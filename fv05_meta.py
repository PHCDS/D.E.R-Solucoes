# FV05 - Escolher quanto do consumo o sistema solar vai atender


# T02 - validação
def validar_percentual(texto):
    try:
        pct = float(texto.replace(",", "."))
    except ValueError:
        return None
    if not (1 <= pct <= 100):
        return None
    return pct


# T01 + T03
def pedir_percentual():
    print("\n--- META DE GERAÇÃO ---")
    while True:
        pct = validar_percentual(input("Quanto do consumo o sistema deve atender (1 a 100%): ").strip())
        if pct is not None:
            return pct
        print("O percentual tem que ficar entre 1 e 100.")


def calcular_energia_alvo(consumo_referencia, percentual):
    # E_FV = consumo x fração
    return round(consumo_referencia * percentual / 100, 2)

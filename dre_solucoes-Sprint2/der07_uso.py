# DER07 - Informar a quantidade e o tempo médio de uso diário de cada equipamento


# T02 - quantidade inteira acima de zero
def validar_quantidade(texto):
    if not texto.isdigit():
        return None
    qtd = int(texto)
    if qtd <= 0:
        return None
    return qtd


# T03 - horas entre 0 e 24
def validar_horas(texto):
    texto = texto.replace(",", ".")  # aceita 1,5 também
    try:
        horas = float(texto)
    except ValueError:
        return None
    if not (0 <= horas <= 24):
        return None
    return horas


# T01 + T04 - campos com mensagem de erro, repete até o valor ser válido
def pedir_quantidade():
    while True:
        qtd = validar_quantidade(input("Quantidade: ").strip())
        if qtd is not None:
            return qtd
        print("A quantidade tem que ser um número inteiro maior que zero.")


def pedir_horas():
    while True:
        horas = validar_horas(input("Horas de uso por dia: ").strip())
        if horas is not None:
            return horas
        print("As horas de uso têm que ficar entre 0 e 24.")

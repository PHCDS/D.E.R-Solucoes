# FV04 - Informar localização do imóvel e horas de sol pleno (HSP)
from banco import conectar

HSP_MIN = 3
HSP_MAX = 7


# T01 - cidade, estado e HSP na tabela de imóvel
def adicionar_colunas_local():
    con = conectar()
    colunas = [c[1] for c in con.execute("PRAGMA table_info(imovel)").fetchall()]
    for coluna, tipo in [("cidade", "TEXT"), ("estado", "TEXT"), ("hsp", "REAL")]:
        if coluna not in colunas:
            con.execute(f"ALTER TABLE imovel ADD COLUMN {coluna} {tipo}")
    con.commit()
    con.close()


def salvar_local(imovel_id, cidade, estado, hsp):
    con = conectar()
    con.execute("UPDATE imovel SET cidade = ?, estado = ?, hsp = ? WHERE id = ?",
                (cidade, estado, hsp, imovel_id))
    con.commit()
    con.close()


def buscar_local(imovel_id):
    con = conectar()
    linha = con.execute("SELECT cidade, estado, hsp FROM imovel WHERE id = ?",
                        (imovel_id,)).fetchone()
    con.close()
    return linha


# T04 - validação
def validar_hsp(texto):
    try:
        hsp = float(texto.replace(",", "."))
    except ValueError:
        return None
    if not (HSP_MIN <= hsp <= HSP_MAX):
        return None
    return hsp


# T02 + T03 - tabela de referência ou digitado na mão
def tela_local(imovel_id, tabela_hsp):
    print("\n--- LOCALIZAÇÃO DO IMÓVEL ---")
    atual = buscar_local(imovel_id)
    if atual and atual[2]:
        print(f"Já cadastrado: {atual[0]}/{atual[1]}, HSP {atual[2]:g}")
        if input("Quer trocar? (s/n): ").strip().lower() != "s":
            return atual[2], "cadastro anterior"

    cidade = input("Cidade: ").strip()
    estado = input("Estado (UF): ").strip().upper()

    regioes = list(tabela_hsp.keys())
    print("\nHSP (horas de sol pleno por dia):")
    for i, r in enumerate(regioes, start=1):
        print(f"{i} - {r} (aproximado: {tabela_hsp[r]:g})")
    print("0 - Digitar o valor do CRESESB para a cidade")

    op = input("Opção: ").strip()
    if op.isdigit() and 1 <= int(op) <= len(regioes):
        regiao = regioes[int(op) - 1]
        hsp = tabela_hsp[regiao]
        origem = f"tabela de referência ({regiao}, valor aproximado)"
    else:
        hsp = None
        while hsp is None:
            hsp = validar_hsp(input(f"HSP (entre {HSP_MIN} e {HSP_MAX}): ").strip())
            if hsp is None:
                print(f"O HSP tem que ser um número entre {HSP_MIN} e {HSP_MAX}.")
        origem = "informado pelo usuário"

    salvar_local(imovel_id, cidade, estado, hsp)
    print(f"Local salvo. HSP adotado: {hsp:g} ({origem})")
    return hsp, origem

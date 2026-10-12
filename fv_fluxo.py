# Fluxo do dimensionamento fotovoltaico (FV03 a FV10 na ordem)
from fv02_dados import carregar_tudo, ErroDataset
from fv03_consumo import definir_consumo_referencia
from fv04_local import tela_local
from fv05_meta import pedir_percentual, calcular_energia_alvo
from fv06_dimensionamento import escolher_modulo, dimensionar, mostrar_dimensionamento
from fv07_inversor import selecionar_inversor, mostrar_inversor
from fv08_baterias import (perguntar_armazenamento, escolher_bateria,
                           dimensionar_banco, mostrar_banco)
from fv09_orcamento import montar_orcamento, mostrar_orcamento
from fv10_proposta import mostrar_proposta


def dimensionar_fotovoltaico(imovel):
    imovel_id, imovel_nome = imovel[0], imovel[1]

    # FV02 - sem dataset o dimensionamento nem começa
    try:
        base = carregar_tudo()
    except ErroDataset as erro:
        print(f"\nNão dá para dimensionar: {erro}")
        return

    # FV03
    consumo = definir_consumo_referencia(imovel_id)
    if consumo is None:
        return

    # FV04
    hsp, hsp_origem = tela_local(imovel_id, base["hsp"])

    # FV05
    percentual = pedir_percentual()
    energia_alvo = calcular_energia_alvo(consumo, percentual)
    print(f"Energia a gerar: {energia_alvo:.2f} kWh/mês")

    # FV08 - perguntado antes porque muda o filtro do inversor
    autonomia = perguntar_armazenamento()
    precisa_bateria = autonomia is not None

    # FV06
    modulo = escolher_modulo(base["modulos"])
    d = dimensionar(energia_alvo, hsp, modulo)
    mostrar_dimensionamento(d)

    # FV07
    inversor, descartados = selecionar_inversor(
        base["inversores"], d["potencia_instalada_w"], modulo, precisa_bateria)
    mostrar_inversor(inversor, descartados, d["potencia_instalada_w"], modulo, precisa_bateria)
    if inversor is None:
        return

    # FV08
    banco = None
    if precisa_bateria:
        bateria = escolher_bateria(base["baterias"])
        banco = dimensionar_banco(consumo, autonomia, bateria)
    mostrar_banco(banco)

    # FV09
    orcamento = montar_orcamento(d, inversor, banco)
    mostrar_orcamento(orcamento)

    # FV10
    local = None
    from fv04_local import buscar_local
    local = buscar_local(imovel_id)
    mostrar_proposta({
        "imovel_nome": imovel_nome,
        "cidade": local[0] if local else None,
        "estado": local[1] if local else None,
        "hsp": hsp,
        "hsp_origem": hsp_origem,
        "consumo_referencia": consumo,
        "percentual": percentual,
        "energia_alvo": energia_alvo,
        "dimensionamento": d,
        "inversor": inversor,
        "banco": banco,
        "orcamento": orcamento,
    })

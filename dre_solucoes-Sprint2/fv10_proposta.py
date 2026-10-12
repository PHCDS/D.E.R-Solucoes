# FV10 - Ver uma proposta preliminar com tudo o que foi dimensionado
from fv06_dimensionamento import RENDIMENTO_GLOBAL


def linha():
    print("=" * 60)


# T01 + T02 + T03 - resumo com tudo o que o enunciado pede
def mostrar_proposta(dados):
    d = dados["dimensionamento"]
    inv = dados["inversor"]
    banco = dados["banco"]
    orc = dados["orcamento"]
    m = d["modulo"]

    linha()
    print("PROPOSTA PRELIMINAR - SISTEMA FOTOVOLTAICO")
    linha()

    print(f"\nImóvel: {dados['imovel_nome']}")
    if dados.get("cidade"):
        print(f"Local: {dados['cidade']}/{dados['estado']}")
    print(f"HSP adotado: {dados['hsp']:g} h/dia ({dados['hsp_origem']})")

    print("\n[ CONSUMO ]")
    print(f"Consumo de referência: {dados['consumo_referencia']:.2f} kWh/mês")
    print(f"Atendimento solar: {dados['percentual']:.0f}%")
    print(f"Energia a gerar (E_FV): {dados['energia_alvo']:.2f} kWh/mês")

    print("\n[ GERAÇÃO ]")
    print(f"Rendimento global adotado: {RENDIMENTO_GLOBAL:.2f}")
    print(f"Potência necessária: {d['potencia_necessaria_w'] / 1000:.2f} kWp")
    print(f"Módulo: {m['fabricante']} {m['modelo']} - {m['potencia_wp']:.0f} Wp, "
          f"{m['eficiencia']:.1f}%")
    print(f"Quantidade: {d['quantidade']} módulos")
    print(f"Potência instalada: {d['potencia_instalada_w'] / 1000:.2f} kWp")
    print(f"Geração estimada: {d['geracao_estimada_kwh']:.2f} kWh/mês")

    print("\n[ INVERSOR ]")
    if inv is None:
        print("Nenhum inversor compatível no dataset.")
    else:
        print(f"{inv['fabricante']} {inv['modelo']}")
        print(f"Potência nominal: {inv['potencia_nominal'] / 1000:.1f} kW | "
              f"{inv['qtd_mppt']} MPPT | eficiência {inv['eficiencia']:.1f}%")

    print("\n[ ARMAZENAMENTO ]")
    if banco is None:
        print("Sistema sem banco de baterias.")
    else:
        b = banco["bateria"]
        print(f"{banco['quantidade']}x {b['fabricante']} {b['modelo']} ({b['tecnologia']})")
        print(f"Autonomia: {banco['autonomia_horas']:g} h | "
              f"Capacidade instalada: {banco['capacidade_instalada_kwh']:.2f} kWh")

    print("\n[ INVESTIMENTO ]")
    print(f"Equipamentos: R$ {orc['total_equipamentos']:.2f}")
    print(f"Custos adicionais: R$ {orc['total_extras']:.2f}")
    print(f"Custo total estimado: R$ {orc['custo_total']:.2f}")

    print("\nValores de referência coletados em 05/10/2026. "
          "Ver datasets/FONTES.md.")
    linha()

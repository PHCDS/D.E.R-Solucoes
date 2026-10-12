# FV09 - Receber uma estimativa de custo da solução

# T02 - custos extras adotados como premissa de projeto (documentados no README)
# Percentual sobre o valor dos equipamentos.
EXTRAS = {
    "Estrutura de fixação": 0.08,
    "Cabos, conectores e proteções": 0.07,
    "Instalação e mão de obra": 0.20,
    "Projeto e homologação": 0.05,
}


# T01 - soma dos equipamentos selecionados
def montar_orcamento(dimensionamento, inversor, banco):
    itens = []

    m = dimensionamento["modulo"]
    subtotal_modulos = round(dimensionamento["quantidade"] * m["preco"], 2)
    itens.append({
        "item": f"Módulo {m['fabricante']} {m['modelo']}",
        "qtd": dimensionamento["quantidade"],
        "unitario": m["preco"],
        "subtotal": subtotal_modulos,
    })

    if inversor:
        itens.append({
            "item": f"Inversor {inversor['fabricante']} {inversor['modelo']}",
            "qtd": 1,
            "unitario": inversor["preco"],
            "subtotal": inversor["preco"],
        })

    # sem armazenamento o custo de bateria fica zero
    if banco:
        b = banco["bateria"]
        subtotal_bat = round(banco["quantidade"] * b["preco"], 2)
        itens.append({
            "item": f"Bateria {b['fabricante']} {b['modelo']}",
            "qtd": banco["quantidade"],
            "unitario": b["preco"],
            "subtotal": subtotal_bat,
        })

    total_equipamentos = round(sum(i["subtotal"] for i in itens), 2)

    extras = []
    for nome, pct in EXTRAS.items():
        extras.append({"item": nome, "pct": pct, "valor": round(total_equipamentos * pct, 2)})
    total_extras = round(sum(e["valor"] for e in extras), 2)

    return {
        "itens": itens,
        "total_equipamentos": total_equipamentos,
        "extras": extras,
        "total_extras": total_extras,
        "custo_total": round(total_equipamentos + total_extras, 2),
    }


# T03 - equipamentos separados do custo total
def mostrar_orcamento(orc):
    print("\n--- ORÇAMENTO ESTIMADO ---")
    for i in orc["itens"]:
        print(f"{i['qtd']}x {i['item']}")
        print(f"     R$ {i['unitario']:.2f} un.  =  R$ {i['subtotal']:.2f}")
    print(f"\nEquipamentos: R$ {orc['total_equipamentos']:.2f}")
    print("\nCustos adicionais estimados:")
    for e in orc["extras"]:
        print(f"  {e['item']} ({e['pct'] * 100:.0f}%): R$ {e['valor']:.2f}")
    print(f"  Subtotal: R$ {orc['total_extras']:.2f}")
    print(f"\nCUSTO TOTAL ESTIMADO: R$ {orc['custo_total']:.2f}")

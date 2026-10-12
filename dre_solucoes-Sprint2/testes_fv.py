# Testes do fotovoltaico (FV02 a FV10)
import os
import banco

banco.ARQUIVO = "teste_fv.db"
if os.path.exists(banco.ARQUIVO):
    os.remove(banco.ARQUIVO)

from main import preparar_banco
from der01_cadastro import salvar_usuario
from der02_login import autenticar
from der03_imovel import salvar_imovel, listar_imoveis
from der06_selecao import salvar_item, buscar_equipamentos
from fv02_dados import carregar_tudo, ErroDataset, numero
from fv04_local import validar_hsp, salvar_local, buscar_local
from fv05_meta import validar_percentual, calcular_energia_alvo
from fv06_dimensionamento import calcular_potencia_necessaria, dimensionar, buscar_modulo, RENDIMENTO_GLOBAL
from fv07_inversor import selecionar_inversor, compativel, modulos_por_string
from fv08_baterias import dimensionar_banco
from fv09_orcamento import montar_orcamento
from der09_total import calcular_total

preparar_banco()
base = carregar_tudo()

# FV02 - os três datasets carregam e têm o mínimo pedido
assert len(base["modulos"]) >= 10, f"só {len(base['modulos'])} módulos"
assert len(base["inversores"]) >= 8, f"só {len(base['inversores'])} inversores"
assert len(base["baterias"]) >= 6, f"só {len(base['baterias'])} baterias"
for m in base["modulos"]:
    assert m["potencia_wp"] > 0 and m["preco"] > 0
for i in base["inversores"]:
    assert i["potencia_nominal"] > 0 and i["mppt_min"] < i["mppt_max"]
for b in base["baterias"]:
    assert 0 < b["dod"] <= 100 and b["kwh"] > 0
assert any(i["aceita_bateria"] for i in base["inversores"]), "nenhum inversor híbrido"
# campo quebrado é recusado
try:
    numero({"id": "1", "potencia_wp": "abc"}, "potencia_wp", "modulos.csv")
    raise AssertionError("devia ter recusado texto no campo numérico")
except ErroDataset:
    pass
print("FV02 ok")

# FV04 - validação do HSP
assert validar_hsp("4.9") == 4.9
assert validar_hsp("5,2") == 5.2
assert validar_hsp("2.9") is None
assert validar_hsp("7.1") is None
assert validar_hsp("abc") is None
print("FV04 ok")

# FV05 - percentual e energia alvo
assert validar_percentual("80") == 80
assert validar_percentual("0") is None
assert validar_percentual("101") is None
assert calcular_energia_alvo(300, 80) == 240.0
assert calcular_energia_alvo(450, 100) == 450.0
print("FV05 ok")

# FV06 - conta feita na mão
# E_FV 240 kWh, HSP 4.9, rendimento 0.78 -> 240/(4.9*30*0.78) = 2.0929 kWp
esperado = 240 / (4.9 * 30 * 0.78) * 1000
assert abs(calcular_potencia_necessaria(240, 4.9) - round(esperado, 2)) < 0.01
modulo = buscar_modulo(base["modulos"], 1)   # OSDA 560 Wp
d = dimensionar(240, 4.9, modulo)
# 2092.9 / 560 = 3.73 -> arredonda pra 4 módulos
assert d["quantidade"] == 4, d["quantidade"]
assert d["potencia_instalada_w"] == 4 * 560
# arredondamento sempre para cima
assert dimensionar(1, 4.9, modulo)["quantidade"] == 1
print("FV06 ok")

# FV07 - compatibilidade, não escolhe pelo preço
inv, descartados = selecionar_inversor(base["inversores"], d["potencia_instalada_w"], modulo)
assert inv is not None
assert d["potencia_instalada_w"] <= inv["potencia_max_fv"]
assert modulo["voc"] <= inv["tensao_max"]
assert modulos_por_string(inv, modulo) >= 1
# inversor incompatível por potência é descartado mesmo sendo o mais barato
pequeno = min(base["inversores"], key=lambda i: i["potencia_nominal"])
grande = dimensionar(2000, 4.9, modulo)   # arranjo enorme
ok, motivos = compativel(pequeno, grande["potencia_instalada_w"], modulo)
assert not ok and motivos
# arranjo gigante não acha inversor nenhum
nenhum, _ = selecionar_inversor(base["inversores"], 200000, modulo)
assert nenhum is None
# com bateria, só entra híbrido
hibrido, _ = selecionar_inversor(base["inversores"], d["potencia_instalada_w"], modulo, True)
assert hibrido is not None and hibrido["aceita_bateria"]
print("FV07 ok")

# FV08 - banco de baterias
bateria = base["baterias"][2]   # Moura lítio 4.8 kWh, DoD 80%, ef 95%
bk = dimensionar_banco(300, 12, bateria)
assert bk["energia_diaria_kwh"] == 10.0          # 300/30
assert bk["energia_autonomia_kwh"] == 5.0        # 10 * 12/24
assert bk["quantidade"] >= 1
assert bk["capacidade_instalada_kwh"] == round(bk["quantidade"] * bateria["kwh"], 2)
# autonomia maior pede mais bateria
assert dimensionar_banco(300, 48, bateria)["quantidade"] > bk["quantidade"]
# campos que o fabricante não publica vêm marcados
freedom = base["baterias"][0]
assert freedom["kwh_calculado"] is True
assert freedom["eficiencia_adotada"] is True
assert freedom["kwh"] == round(12 * 105 / 1000, 2)
print("FV08 ok")

# FV09 - orçamento
orc_sem = montar_orcamento(d, inv, None)
soma_itens = sum(i["subtotal"] for i in orc_sem["itens"])
assert abs(orc_sem["total_equipamentos"] - soma_itens) < 0.01
assert orc_sem["total_equipamentos"] == round(4 * modulo["preco"] + inv["preco"], 2)
assert orc_sem["custo_total"] > orc_sem["total_equipamentos"]
# sem bateria nenhum item de bateria entra
assert not any("Bateria" in i["item"] for i in orc_sem["itens"])
# com bateria o total sobe
orc_com = montar_orcamento(d, hibrido, bk)
assert orc_com["total_equipamentos"] > orc_sem["total_equipamentos"]
print("FV09 ok")

# FV03 - o consumo vem do cálculo da sprint 1
salvar_usuario("Teste", "teste@email.com", "123456")
uid = autenticar("teste@email.com", "123456")[0]
salvar_imovel(uid, "Casa teste", "Rua X, 1", "Casa")
imovel_id = listar_imoveis(uid)[0][0]
geladeira = buscar_equipamentos("Geladeira")[0][0]
salvar_item(imovel_id, geladeira, 1, 24)
assert calcular_total(imovel_id) == 180.0
# FV04 - o local fica gravado no imóvel
salvar_local(imovel_id, "São Paulo", "SP", 4.9)
assert buscar_local(imovel_id) == ("São Paulo", "SP", 4.9)
print("FV03 ok")

os.remove(banco.ARQUIVO)
print("\nTodos os testes do fotovoltaico passaram.")

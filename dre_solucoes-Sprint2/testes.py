# Testes das tasks de teste (DER01 T04, DER04 T04, DER08 T04) e das regras principais
import os
import banco

# usa um banco separado pra não bagunçar o dre.db
banco.ARQUIVO = "teste.db"
if os.path.exists(banco.ARQUIVO):
    os.remove(banco.ARQUIVO)

from main import preparar_banco
from der01_cadastro import validar_cadastro, salvar_usuario
from der02_login import autenticar
from der03_imovel import salvar_imovel, listar_imoveis
from der04_editar_imovel import editar_imovel, excluir_imovel
from der06_selecao import salvar_item, buscar_equipamentos
from der07_uso import validar_quantidade, validar_horas
from der08_consumo import calcular_consumo, listar_itens
from der09_total import calcular_total
from der10_editar_equipamento import editar_item, remover_item

preparar_banco()

# DER01 T04 - cadastro com dados certos e errados
assert validar_cadastro("Pedro", "pedro@email.com", "123456") is None
assert validar_cadastro("", "pedro@email.com", "123456") is not None
assert validar_cadastro("Pedro", "pedroemail.com", "123456") is not None
assert validar_cadastro("Pedro", "pedro@email.com", "123") is not None
salvar_usuario("Pedro", "pedro@email.com", "123456")
assert validar_cadastro("Outro", "pedro@email.com", "123456") is not None  # e-mail repetido
print("DER01 ok")

# DER02 - login certo e errado
usuario = autenticar("pedro@email.com", "123456")
assert usuario is not None
assert autenticar("pedro@email.com", "senhaerrada") is None
print("DER02 ok")

# DER03 - salvar e aparecer na lista
uid = usuario[0]
salvar_imovel(uid, "Casa", "Rua A, 10", "Casa")
salvar_imovel(uid, "Apto", "Rua C, 30", "Apartamento")
assert len(listar_imoveis(uid)) == 2
imovel_id = listar_imoveis(uid)[0][0]
print("DER03 ok")

# DER07 - validações de quantidade e horas
assert validar_quantidade("2") == 2
assert validar_quantidade("0") is None
assert validar_quantidade("1.5") is None
assert validar_quantidade("abc") is None
assert validar_horas("24") == 24
assert validar_horas("1,5") == 1.5
assert validar_horas("25") is None
assert validar_horas("-1") is None
print("DER07 ok")

# DER08 T04 - contas feitas na mão
assert calcular_consumo(100, 2, 5) == 30.0      # 100 x 2 x 5 x 30 / 1000
assert calcular_consumo(5500, 1, 0.5) == 82.5   # chuveiro meia hora por dia
assert calcular_consumo(9, 10, 6) == 16.2       # 10 lâmpadas LED
print("DER08 ok")

# DER09 - imóvel vazio e com mais de um equipamento
assert calcular_total(imovel_id) == 0
geladeira = buscar_equipamentos("Geladeira")[0][0]
chuveiro = buscar_equipamentos("Chuveiro")[0][0]
salvar_item(imovel_id, geladeira, 1, 24)   # 180 kWh
salvar_item(imovel_id, chuveiro, 1, 0.5)   # 82,5 kWh
assert calcular_total(imovel_id) == 262.5
print("DER09 ok")

# DER10 - o total muda logo depois de editar e remover
item_chuveiro = listar_itens(imovel_id)[1][0]
editar_item(item_chuveiro, 1, 1)           # chuveiro vira 165 kWh
assert calcular_total(imovel_id) == 345.0
remover_item(item_chuveiro)
assert calcular_total(imovel_id) == 180.0
print("DER10 ok")

# DER04 T04 - editar e excluir, conferindo a lista
editar_imovel(imovel_id, "Casa nova", "Rua B, 20", "Casa")
assert listar_imoveis(uid)[0][1] == "Casa nova"
excluir_imovel(imovel_id)
assert len(listar_imoveis(uid)) == 1
assert listar_itens(imovel_id) == []       # equipamentos saíram junto
print("DER04 ok")

os.remove(banco.ARQUIVO)
print("\nTodos os testes passaram.")

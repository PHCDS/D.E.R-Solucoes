# D.R.E Soluções

Sistema de dimensionamento energético residencial, feito em duas sprints para a
FIAP.

A sprint 1 estima o consumo mensal de energia de uma residência a partir dos
equipamentos que ela tem. A sprint 2 usa esse consumo para dimensionar um
sistema fotovoltaico e montar um orçamento.

## Como rodar

```bash
python main.py
```

O banco `dre.db` é criado sozinho na primeira execução, já com a base de
equipamentos elétricos. Os datasets fotovoltaicos ficam em `datasets/`.

Testes:

```bash
python testes.py       # sprint 1
python testes_fv.py    # sprint 2
```

## Como achar cada User Story no código

Sprint 1, consumo:

| US | Arquivo |
|---|---|
| DER01 | der01_cadastro.py |
| DER02 | der02_login.py |
| DER03 | der03_imovel.py |
| DER04 | der04_editar_imovel.py |
| DER05 | der05_equipamentos.py |
| DER06 | der06_selecao.py |
| DER07 | der07_uso.py |
| DER08 | der08_consumo.py |
| DER09 | der09_total.py |
| DER10 | der10_editar_equipamento.py |

Sprint 2, fotovoltaico:

| US | Arquivo |
|---|---|
| FV01 | datasets/ (modulos.csv, inversores.csv, baterias.csv) |
| FV02 | fv02_dados.py |
| FV03 | fv03_consumo.py |
| FV04 | fv04_local.py |
| FV05 | fv05_meta.py |
| FV06 | fv06_dimensionamento.py |
| FV07 | fv07_inversor.py |
| FV08 | fv08_baterias.py |
| FV09 | fv09_orcamento.py |
| FV10 | fv10_proposta.py |

O `fv_fluxo.py` chama essas etapas na ordem, e o `main.py` junta tudo nos menus.

## Fórmulas

Consumo de um equipamento, em kWh/mês:

```
consumo = potência (W) x quantidade x horas por dia x 30 / 1000
```

Energia que o sistema solar precisa gerar:

```
E_FV = consumo de referência x percentual de atendimento
```

Potência de pico necessária:

```
P_FV = E_FV / (HSP x 30 x rendimento global)
```

Quantidade de módulos, arredondada sempre para cima:

```
N = ceil(P_FV / potência do módulo)
P_instalada = N x potência do módulo
```

Geração estimada do que foi instalado:

```
geração = P_instalada / 1000 x HSP x 30 x rendimento global
```

Banco de baterias:

```
E_d = consumo mensal / 30
E_autonomia = E_d x horas de autonomia / 24
C_bat = E_autonomia / (DoD x rendimento da bateria)
N_bat = ceil(E_autonomia / (capacidade útil da bateria x rendimento))
```

## Premissas de projeto

O enunciado não fixa esses valores, então o grupo escolheu e deixou
documentado aqui. Todos ficam em constante no topo do arquivo, fáceis de
trocar.

**Rendimento global de 0,78** (`fv06_dimensionamento.py`). Cobre perda por
temperatura, sujeira no painel, queda nos cabos, diferença entre módulos e
perda do inversor. O mercado costuma trabalhar entre 0,75 e 0,80; ficamos no
meio dessa faixa.

**Mês de 30 dias** nos dois cálculos de consumo, para o número ficar
comparável entre meses.

**Sobredimensionamento do arranjo até 1,3x a potência nominal do inversor**
(`fv07_inversor.py`). É prática comum no setor, porque o arranjo quase nunca
entrega a potência de pico. Acima disso o sistema descarta o inversor.

**Custos adicionais sobre o valor dos equipamentos** (`fv09_orcamento.py`):
estrutura 8%, cabos e proteções 7%, instalação 20%, projeto e homologação 5%.
São estimativas do grupo para dar ordem de grandeza. O orçamento mostra o
valor dos equipamentos separado, que é o número que sai direto do dataset.

**Eficiência de bateria quando o fabricante não publica**: 85% para
chumbo-ácido e 95% para lítio. O sistema avisa na tela quando usa esses
valores.

**Capacidade em kWh quando o fabricante não publica**: calculada como
tensão x Ah / 1000. Também vem avisada na tela.

## Datasets

Os três CSV trazem produtos reais vendidos no Brasil, com preço, fornecedor,
data da coleta e link da fonte. As limitações da coleta estão em
`datasets/FONTES.md`, e vale ler antes de defender os números.

A tabela de HSP por região é aproximada e serve de ponto de partida. Para um
projeto de verdade, o valor da cidade sai do CRESESB SunData.

## Evidência de execução

O arquivo `EVIDENCIA_CENARIOS.txt` tem a saída dos dois cenários pedidos no
enunciado, com e sem bateria, rodados sobre o mesmo imóvel.

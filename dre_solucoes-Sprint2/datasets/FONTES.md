# Fontes e limitações dos datasets

Coleta feita em 05/10/2026. Preço de equipamento solar muda rápido, então
se a entrega for depois dessa data vale reconferir os valores.

## Módulos (10 produtos)

Preço e ficha técnica vieram da página de cada produto na Buyers Energy e na
Pichau. As fichas da Buyers Energy repetem a mesma dimensão (2278 x 1134) em
quase todos os modelos, o que indica ficha padronizada da loja e não do
fabricante. Antes de usar Voc e Isc para cálculo de string, confira no
datasheet do fabricante.

O ODA550-36-MH (Pichau) e o TSM-NE19R (Buyers) apareceram marcados como
esgotados. O preço é real, mas o produto pode não estar disponível.

Lojas que bloquearam o acesso durante a coleta: Neosolar, Minha Casa Solar
(para módulos), Aldo, Mercado Livre, Magazine Luiza e Leroy Merlin. Por isso
não há módulo de 400 a 500 W na base: existem no mercado, mas não deu para
abrir a página e ler o preço.

## Inversores (9 produtos)

Seis têm ficha técnica de datasheet oficial do fabricante (Growatt via Aldo,
Solis, Deye). Três têm ficha só da loja: Huawei SUN2000-5KTL-L1,
Livoltek Hyper 5000 e, em parte, o Deye SUN-5K.

Onde a loja e o datasheet divergiram, ficou valendo o datasheet. Os casos:

- Growatt MIN 3000TL-X: a loja marca que aceita bateria. O datasheet é claro
  que a série MIN TL-X é on-grid pura. Ficou "nao" na base.
- Solis S6-GR1P3K-M: loja dizia 500 V e 98%; datasheet diz 550 V e 97,1%.
- Solis S5-GR1P10K: loja dizia 15 kW de entrada FV; datasheet diz 17 kW.
- Deye SUN-10K: loja dizia 3 MPPT; datasheet diz 2.

Os dois inversores Deye são bifásicos 127/220 V (split-phase), não
monofásicos. Está gravado 220 V na base para o cálculo, mas numa instalação
real isso muda o projeto elétrico.

O Sungrow SG6.0RS-S foi descartado: o preço foi encontrado, mas nenhuma fonte
publicava tensão máxima de entrada nem faixa de MPPT, que o sistema precisa
para verificar compatibilidade.

## Baterias (6 produtos)

Duas estacionárias de chumbo-ácido e quatro de lítio LiFePO4.

Dois campos ficaram em branco de propósito:

- capacidade_kwh das Freedom: o fabricante não declara. O sistema calcula
  (tensão x Ah / 1000) e avisa na tela que é valor calculado.
- eficiencia_pct das Freedom e da Deye SE-F5: não é publicada. O sistema
  adota 85% para chumbo-ácido e 95% para lítio, avisa na tela, e esses
  valores estão documentados no README como premissa de projeto.

Produtos descartados: Intelbras BCE 12-105 (datasheet oficial, mas sem preço
em loja brasileira) e Moura 12MS234 (preço encontrado, mas sem DoD nem
eficiência em nenhuma fonte, e as lojas divergiam na capacidade).

Preço de bateria varia muito entre loja. A mesma Moura estacionária apareceu
por R$ 2.933 numa loja e R$ 2.019 em outra. Os valores da base são de uma
loja só, na data da coleta.

## HSP

A tabela por região traz valores aproximados, para o sistema ter um ponto de
partida. Não é dado oficial. Para a cidade do imóvel, o valor correto sai do
CRESESB SunData (http://www.cresesb.cepel.br/index.php?section=sundata), que
é a referência usada no setor. O sistema deixa digitar o HSP na mão por isso.

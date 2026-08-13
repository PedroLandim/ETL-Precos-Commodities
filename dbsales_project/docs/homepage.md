{% docs __overview__ %}

# ETL de Preços de Commodities

Este repositório mostra um fluxo simples de engenharia de dados para commodities: um script Python coleta preços históricos, grava os dados em Postgres e o dbt transforma essa base junto com uma tabela de movimentações para gerar um datamart final.

## Visão geral do fluxo

1. O script em `src/extract-load.py` usa `yfinance` para buscar preços históricos de commodities como ouro, petróleo, gás natural e prata.
2. Esses dados são carregados em uma tabela `commodities` no PostgreSQL, usando as variáveis de ambiente definidas no projeto.
3. O dbt lê essa tabela como fonte e também consome o seed `movimentacao_commodities.csv`.
4. As duas origens passam por modelos de staging para padronização de nomes e tipos.
5. O modelo `dm_commodities` faz a junção final e calcula o valor da transação e o ganho ou perda associado.

## O que existe no projeto

- `src/extract-load.py` faz a extração dos preços e a carga no banco.
- `src/requirements.txt` lista as dependências Python usadas nesse processo.
- `seeds/movimentacao_commodities.csv` traz a base de movimentação usada no estudo.
- `models/staging/` padroniza as fontes.
- `models/datamart/` concentra a lógica final de negócio.
- `profiles.yml` e `dbt_project.yml` suportam a execução do dbt.

## O que o datamart entrega

O modelo final retorna data, símbolo, preço de fechamento, ação, quantidade, valor da transação e ganho/perda. No estado atual, ele mantém apenas os registros do último dia disponível após a junção entre preços e movimentações.

## Limitações atuais

Este projeto é enxuto e voltado a estudo. Ele não cobre um pipeline de produção completo.

- Não há orquestração automática entre o script Python e o dbt.
- Não há testes de qualidade de dados definidos nos arquivos `schema.yml`.
- Não há histórico versionado de eventos nem camada avançada de observabilidade.
- O carregamento no banco faz truncamento da tabela antes de inserir os dados novos.

## Estrutura atual

- `models/staging/` contém a normalização inicial dos dados.
- `models/datamart/` contém a junção final entre preço e movimentação.
- `seeds/` contém a base de movimentação usada no projeto.

{% enddocs %}


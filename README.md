# Escolas do Brasil 

Script de raspagem de dados para informações das Escolas Brasileiras

## Instalação

Para a instalação basta:

1. criar um ambiente de sua escola( virtualenv, pipenv, conda ) e instalar os requerimentos:
   ```
   pip install -r requirements.txt
   ```
2. Rode o scrpit com:
   ```
   scrapy runspider scrapy.py -o escolas.csv
   ```

## Saida.

Ao final do crawler arquivo escolas.csv estará disponível.
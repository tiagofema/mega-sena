import pandas as pd
import random
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Caminho do arquivo Excel
excel_path = '/Users/tiagoferrazmartins/Downloads/Arquivos/Mega-Sena.xlsx'
# Caminho do novo arquivo CSV
csv_path = '/Users/tiagoferrazmartins/Documents/Tiago/mega-sena-ordenado.csv'

if not os.path.exists(csv_path):
    logging.info('Lendo o arquivo Excel...')
    # Ler o arquivo Excel
    df = pd.read_excel(excel_path)

    logging.info('Extraindo as colunas Bola 1 a Bola 6...')
    # Extrair as colunas Bola 1 a Bola 6
    bolas = df[['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']]

    logging.info('Ordenando os números em cada linha...')
    # Ordenar os números em cada linha
    bolas_ordenadas = bolas.apply(lambda x: sorted(x), axis=1)

    logging.info('Salvando os números ordenados em um novo arquivo CSV...')
    # Salvar em um novo arquivo CSV
    bolas_ordenadas.to_csv(csv_path, index=False, header=False)
else:
    logging.info('Arquivo bolas_ordenadas já existe. Pulando a geração...')

# Ler o arquivo bolas_ordenadas
bolas_ordenadas = pd.read_csv(csv_path, header=None)

# Converter bolas_ordenadas para uma matriz
matriz_bolas_ordenadas = bolas_ordenadas.values.tolist()

# Função para gerar um jogo válido
def gerar_jogo_valido():
    while True:
        jogo = sorted(random.sample(range(1, 61), 6))
        logging.info(f'Jogo gerado temporariamente: {jogo}')
        if not any(set(jogo) == set(linha) for linha in matriz_bolas_ordenadas):
            logging.info(f'Jogo gerado: {jogo}')
            return jogo

logging.info('Gerando 100 novos jogos...')
# Gerar 100 novos jogos
novos_jogos = []
for _ in range(100):
    jogo = gerar_jogo_valido()
    logging.info(f'Novo jogo gerado: {jogo}')
    novos_jogos.append(jogo)

logging.info('Comparando jogos gerados com os existentes...')
# Comparar jogos gerados com os existentes
for i, jogo in enumerate(novos_jogos, start=1):
    logging.info(f'Jogo {i} - Números gerados: {jogo}')

logging.info('Salvando os novos jogos em um novo arquivo CSV...')
# Salvar os novos jogos em um novo arquivo CSV
novos_jogos_df = pd.DataFrame(novos_jogos, columns=[f'No.{i}' for i in range(1, 7)])
novos_jogos_df.to_csv('/Users/tiagoferrazmartins/Documents/Tiago/mega-sena-novos-jogos.csv', index=True)

logging.info('Execução concluída.')

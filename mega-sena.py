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
# Caminho do arquivo de ranking
ranking_path = '/Users/tiagoferrazmartins/Documents/Tiago/mega-sena-ranking.csv'

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
def gerar_jogo_valido(novos_jogos):
    jogo = sorted(random.sample(range(1, 61), 6))
    logging.info(f'Jogo gerado temporariamente: {jogo}')
    if any(set(jogo) == set(linha) for linha in matriz_bolas_ordenadas) or any(set(jogo) == set(linha) for linha in novos_jogos):
        return gerar_jogo_valido(novos_jogos)  # Chamada recursiva
    logging.info(f'Jogo gerado: {jogo}')
    return jogo

def estatisticas_numeros_repetidos(matriz):
    # Extrair apenas os números das strings no objeto matriz
    todos_numeros = []
    for sublista in matriz:
        numeros = [int(''.join(filter(str.isdigit, numero))) for numero in str(sublista).strip('[]').split(', ')]
        todos_numeros.extend(numeros)
    # Contar a frequência de cada número
    contagem = pd.Series(todos_numeros).value_counts()
    # Exibir os números mais frequentes
    logging.info('Números mais frequentes:')
    for numero, frequencia in contagem.head(10).items():
        logging.info(f'Número {numero}: {frequencia} vezes')
    return contagem

def gerar_jogo_com_numeros_frequentes(numeros_frequentes):
    return sorted(random.sample(numeros_frequentes, 6))

if not os.path.exists(ranking_path):
    logging.info('Calculando estatísticas dos números mais repetidos...')
    contagem_numeros = estatisticas_numeros_repetidos(matriz_bolas_ordenadas)
    
    # Salvar o ranking de todos os 60 números em um novo arquivo CSV
    contagem_numeros_df = contagem_numeros.reset_index()
    contagem_numeros_df.columns = ['Número', 'Frequência']
    contagem_numeros_df.to_csv(ranking_path, index=False)
else:
    logging.info('Arquivo de ranking já existe. Pulando a geração...')
    contagem_numeros_df = pd.read_csv(ranking_path)
    contagem_numeros = contagem_numeros_df.set_index('Número')['Frequência']

logging.info('Gerando 100 novos jogos...')
# Gerar 100 novos jogos
novos_jogos = []
for _ in range(100):
    jogo = gerar_jogo_valido(novos_jogos)
    logging.info(f'Novo jogo gerado: {jogo}')
    novos_jogos.append(jogo)

logging.info('Comparando jogos gerados com os existentes...')
# Comparar jogos gerados com os existentes
for i, jogo in enumerate(novos_jogos, start=1):
    logging.info(f'Jogo {i} - Números gerados: {jogo}')

logging.info('Salvando os novos jogos em um novo arquivo CSV...')
# Salvar os novos jogos em um novo arquivo CSV
novos_jogos_df = pd.DataFrame(novos_jogos, columns=[f'No.{i}' for i in range(1, 7)])
novos_jogos_df.to_csv('/Users/tiagoferrazmartins/Documents/Tiago/mega-sena-novos-jogos.csv', index=False)

# Gerar 10 novos jogos usando os 7 números mais frequentes
numeros_mais_frequentes = contagem_numeros.head(7).index.tolist()
logging.info('Gerando 10 novos jogos com os números mais frequentes...')
novos_jogos_frequentes = []
for _ in range(10):
    jogo = gerar_jogo_com_numeros_frequentes(numeros_mais_frequentes)
    logging.info(f'Novo jogo gerado com números frequentes: {jogo}')
    novos_jogos_frequentes.append(jogo)

logging.info('Salvando os novos jogos com números frequentes em um novo arquivo CSV...')
# Salvar os novos jogos com números frequentes em um novo arquivo CSV
novos_jogos_frequentes_df = pd.DataFrame(novos_jogos_frequentes, columns=[f'No.{i}' for i in range(1, 7)])
novos_jogos_frequentes_df.to_csv('/Users/tiagoferrazmartins/Documents/Tiago/mega-sena-most-frequent-new-games.csv', index=False)

logging.info('Execução concluída.')

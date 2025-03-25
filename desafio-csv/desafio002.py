import csv # Trabalhar com arquivo csv
import json # Trabalhar com json
import matplotlib.pyplot as plt  # Importa a biblioteca matplotlib para plotar gráficos
from datetime import datetime  # Importa a classe datetime para trabalhar com datas


class StockData:
    """
    Classe para gerenciar ações a partir de um arquivo csv
    """
    def __init__(self, caminho_csv):
        # método construtor
        self.caminho_csv = caminho_csv # armazena o caminho do arquivo csv
        self.dados = [] # inicializa uma lista para armazenar os arquivos csv
        self.carregar_dados() # carregar daods arquivos csv

    def carregar_dados(self):
        # carrega os dados do csv para a lista de dados
        with open(self.caminho_csv, 'r') as arquivo: # abrindo o arquivo para leitura
            leitor = csv.reader(arquivo) # criando o leitor    
            next(leitor) # pula o cabeçalho csv
            for linha in leitor: # itera sobre cada linha do csv
                self.dados.append({ # adiciona um dicionario com os daods da linha a lista dos dados
                    'data': linha[0], # data da linha
                    'open': float(linha[1]), # valor da abertura da ação
                    'high': float(linha[2]), # valor mais alto da ação
                    'low': float(linha[3]), # valor mais baixo da ação
                    'close': float(linha[4]), # valor de fechamento da ação
                    'volume': float(linha[5]) # valor da negociação
                })

    def maior_valor(self):
        # Encontre o maior valor da coluna High e a data correspondente
        maior = max(self.dados, key=lambda x: x['high']) # encontrar no dicionario o maior valor expressão lambda
        return maior['high'], maior['data'] # retorna o valor e a data maior
    

    def os_15_maiores_valores(self):
        # retorna os 15 maiores valores e os seus indices
        maiores = sorted(self.dados, key=lambda x: x['high'], reverse=True)[:15] # ordenar dados valor high em decresente os e pegar os 15 primeiros
        return [(i, v['high']) for i, v in enumerate(maiores)] # Retorna uma lista de tuplas com o índice e o valor high


    def media_valores(self):
        # calcular as medias dos valores das colunas open, close, high, low
        soma = {
            'open': 0,
            'close': 0,
            'high': 0,
            'low': 0 
        } # inicializa o dicionario para realizara soma
        contador = len(self.dados) # calcula o número de linhas do arquivo csv

        for linha in self.dados: # itera sobre cada linha csv
            soma['open'] += linha['open'] # somando a coluna open
            soma['close'] += linha['close'] # somando a coluna close
            soma['high'] += linha['high'] # somando a coluna high
            soma['low'] += linha['low'] # somando a coluna low
        return {key: valor / contador for key, valor in soma.items()} # retorna um dicionario com as medias calculadas
    
    def remover_linhas_menor_high(self, valor_high):
        # Remove linhas do csv onde o valor high é menor que o especificado

        linhas_removidas = [linha for linha in self.dados if linha['high'] < valor_high] # filtra as linhas com high menow que valor limite
        self.daods = [linha for linha in self.dados if linha['high'] >= valor_high] # atualiza a lista de daods com valor restante
        self.salvar_dados() # salvando as alterações no csv
        return linhas_removidas # retornar linhas removidas
    
    def salvar_dados(self):
        # Salvar dados dos arquivo csv
        with open(self.caminho_csv, 'w', newline='') as arquivo: # abrir o arquivo para escrita
            escritor = csv.writer(arquivo) # escritor para escrever as linhas
            escritor.writerow(['Data', 'Open', 'High', 'Low', 'Close', 'Volume']) # escrever o cabeçalho
            for linha in self.dados: # iterando sobre cada linha na listas dos daods
                # escrever a linha no arquivo csv
                escritor.writerow([linha['data'], linha['open'], linha['high'], linha['low'], linha['close'], linha['volume']]) 

    def csv_para_json(self, file_json):
        # Converter os dados csv para json
        dados_json = {
            linha['data']: {
                'open': linha['open'],
                'close': linha['close'],
                'high_low': (linha['high'] + linha['low']) / 2,
                'volume': linha['volume'] 
            }
            for linha in self.dados
        } # criar um dicionario convertido para json
        with open(file_json, 'w') as arquivi_json: # abrir o arquivo json para escrita
            json.dump(dados_json, arquivi_json, indent=4) # escrevendo os dados em um arquivo json com identação

    def plota_grafico(self):
        # plota grafico dos valores ao longo do tempo
        datas = [datetime.strptime(linha['data'], '%Y-%m-%d') for linha in self.dados] # convertendo datas para formato datetime
        altos = [linha['high'] for linha in self.dados] # criar uma lista com os valores high
        plt.plot(datas, altos) # plotar o grafico
        plt.title('Valores altos das ações') # titulo do grafico
        plt.xlabel('Data') # rotulo eixo x
        plt.ylabel('Valor alto') # rotulo eixo y
        plt.xticks(rotation=45) # rotacionar eixo x
        plt.tight_layout() # ajustar layout
        plt.show() # mostrar o grafico

if __name__ == '__main__':
    # caminho do arquivo
    caminho_csv = "C:\\Users\\Paulo\\OneDrive - MSFT\\Documents\\GitHub\\Desafios\\desafio-csv\\KO_1919-09-06_2025-02-18.csv"
    stock_data = StockData(caminho_csv) # criando uma instancia da classe

    # Exibindo maior valor
    maior_valor, data_maior = stock_data.maior_valor()
    print(f'O maior valor encontra na coluna High é: {maior_valor:.2f} e data {data_maior}')

    print('=-=' * 30)
    # Exibindo os 15 maiores valores
    print('Os 15 maiores valores encontrado na coluna high: ')
    for i, valor in stock_data.os_15_maiores_valores():
        print(f'{i}) {valor:.2f}')

    print('=-=' * 30)
    # Exibindo a média
    media = stock_data.media_valores()
    print(f'A média da coluna open: {media['open']:.2f}')
    print(f'A média da coluna close: {media['close']:.2f}')
    print(f'A média da coluba high: {media['high']:.2f}')
    print(f'A média da coluna low: {media['low']:.2f}')

    print('=-=' * 30)
    # Removendo linhas com high menor que valor
    valor_limite_high = 0
    linha_removidas = stock_data.remover_linhas_menor_high(valor_limite_high)
    print(f'Linha com high menos que {valor_limite_high} removido os arquivos: ')
    for linha in linha_removidas:
        print(linha)

    print('=-=' * 30)
    # Convertendo para json
    stock_data.csv_para_json('dados_json.json')
    print('Arquivo JSON criado!')

    print('=-=' * 20)
    # Plotando gráfico
    stock_data.plota_grafico()
    

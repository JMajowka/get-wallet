import requests
from bs4 import BeautifulSoup

def scrape_bitcoin_puzzle_addresses():
    url = "https://privatekeys.pw/puzzles/bitcoin-puzzle-tx"
    
    try:
        # Fazendo a requisição HTTP
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve erro na requisição
        
        # Parseando o HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrando a tabela com os dados (ajuste o seletor conforme necessário)
        table = soup.find('table')
        if not table:
            print("Nenhuma tabela encontrada no site.")
            return []
        
        # Extraindo linhas da tabela
        rows = table.find_all('tr')[1:]  # Pula o cabeçalho
        
        addresses_with_balance = []
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:  # Verifica se há colunas suficientes
                address = cols[0].get_text(strip=True)
                balance = cols[2].get_text(strip=True)  # Ajuste o índice conforme a estrutura real
                
                # Verifica se há saldo (não zero)
                if balance and balance != "0":
                    addresses_with_balance.append((address, balance))
        
        return addresses_with_balance
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o site: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return []

# Executando a função e exibindo os resultados
addresses = scrape_bitcoin_puzzle_addresses()

if addresses:
    print("Endereços com saldo em BTC:")
    for idx, (address, balance) in enumerate(addresses, 1):
        print(f"{idx}. Endereço: {address} - Saldo: {balance} BTC")
else:
    print("Nenhum endereço com saldo encontrado ou erro ao acessar os dados.")
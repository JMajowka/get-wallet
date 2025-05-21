import requests
from bs4 import BeautifulSoup
import time

# Configurações
url = "https://privatekeys.pw/puzzles/bitcoin-puzzle-tx"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/ '
}

# Tentar até 3 vezes caso ocorra erro temporário
tentativas = 3
delay = 2

for i in range(tentativas):
    try:
        print(f"Tentativa {i + 1} de acesso ao site...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Site acessado com sucesso!\n")
            break
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            if i < tentativas - 1:
                print(f"Aguardando {delay} segundos antes da próxima tentativa...\n")
                time.sleep(delay)
            else:
                print("❌ Não foi possível acessar o site após várias tentativas.")
                exit()

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        if i < tentativas - 1:
            print(f"Aguardando {delay} segundos antes da próxima tentativa...\n")
            time.sleep(delay)
        else:
            print("❌ Falha crítica ao tentar acessar o site.")
            exit()

# Parseando o conteúdo HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrando todos os blocos de endereços
addresses = soup.find_all('div', class_='address')

if not addresses:
    print("⚠️ Nenhum endereço encontrado. O layout do site pode ter mudado.")
    exit()

# Exibindo os resultados
print("Endereços encontrados:")
for addr_block in addresses:
    number = addr_block.find('span', class_='number')
    address = addr_block.find('span', class_='addr')
    balance = addr_block.find('span', class_='balance')

    if not all([number, address, balance]):
        continue

    num_text = number.text.strip()
    addr_text = address.text.strip()
    bal_text = balance.text.strip().replace("BTC", "").strip()

    try:
        bal_value = float(bal_text)
    except ValueError:
        continue

    print(f"Puzzle #{num_text} - {addr_text} - Saldo: {bal_value:.8})

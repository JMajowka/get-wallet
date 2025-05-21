import requests
from bs4 import BeautifulSoup

# URL do site
url = "https://privatekeys.pw/puzzles/bitcoin-puzzle-tx "

# Definir headers para simular navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36'
}

# Fazer a requisição com headers
response = requests.get(url, headers=headers)

# Verificar se a resposta foi bem-sucedida
if response.status_code != 200:
    print(f"❌ Erro ao acessar o site. Código HTTP: {response.status_code}")
    print("Possível causa: Site fora do ar, proteção anti-bot ou conexão bloqueada.")
    exit()

# Continuar com o parse do HTML
soup = BeautifulSoup(response.text, 'html.parser')
addresses = soup.find_all('div', class_='address')

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

    print(f"Puzzle #{num_text} - {addr_text} - Saldo: {bal_value:.8f} BTC")

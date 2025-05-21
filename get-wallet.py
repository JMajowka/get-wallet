import requests
from bs4 import BeautifulSoup
import csv

# URL da página que contém os endereços do puzzle
url = "https://privatekeys.pw/puzzles/bitcoin-puzzle-tx "

# Função para buscar saldo via API do Blockchair
def get_balance(address):
    api_url = f"https://api.blockchair.com/bitcoin/address/ {address}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            balance = int(data['data'][address]['balance']) / 100_000_000  # Converter satoshis para BTC
            return round(balance, 8)
        else:
            return None
    except Exception as e:
        print(f"Erro ao verificar {address}: {e}")
        return None

# Fazer scraping dos endereços
response = requests.get(url)
if response.status_code != 200:
    print("Erro ao acessar o site.")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
addresses = soup.find_all('div', class_='address')

results = []

print("Verificando saldos no blockchain...\n")
for addr_block in addresses:
    number = addr_block.find('span', class_='number')
    address = addr_block.find('span', class_='addr')

    if not all([number, address]):
        continue

    puzzle_num = number.text.strip()
    btc_address = address.text.strip()

    print(f"Puzzle #{puzzle_num} - Consultando {btc_address}...")

    balance = get_balance(btc_address)

    if balance is not None and balance > 0:
        results.append({
            'Puzzle': puzzle_num,
            'Endereço': btc_address,
            'Saldo (BTC)': balance
        })
        print(f" → Saldo: {balance:.8f} BTC\n")
    elif balance == 0:
        print(" → Saldo: 0 BTC\n")
    else:
        print(" → Não foi possível obter o saldo.\n")

# Exibir resultados finais
if results:
    print("\n💰 Endereços com saldo positivo:")
    for r in results:
        print(f"Puzzle #{r['Puzzle']} - {r['Endereço']} - {r['Saldo (BTC)']:.8f} BTC")

    # Salvar em CSV (opcional)
    with open('enderecos_com_saldo.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Puzzle', 'Endereço', 'Saldo (BTC)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print("\n✅ Resultados salvos em 'puzzles_com_saldo.txt'")
else:
    print("\n❌ Nenhum endereço com saldo positivo encontrado.")

import requests
from bs4 import BeautifulSoup
import time

# URL da página alvo
url = "https://privatekeys.pw/puzzles/bitcoin-puzzle-tx "

# Cabeçalhos para simular uma requisição de navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/ ',
}

# Configurações de tentativas
tentativas = 3
delay = 2

# Variável para armazenar a resposta final
response = None

# Tentativa de conexão com retentativa
for i in range(tentativas):
    try:
        print(f"[{i + 1}ª tentativa] Conectando ao site...")
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            print("✅ Conexão bem-sucedida!\n")
            break
        else:
            print(f"❌ Erro HTTP {response.status_code}: Falha ao acessar o site.")
            if i < tentativas - 1:
                print(f"Aguardando {delay} segundos antes da próxima tentativa...\n")
                time.sleep(delay)
            else:
                print("❌ Número máximo de tentativas atingido. Encerrando.")
                exit()

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erro na requisição: {e}")
        if i < tentativas - 1:
            print(f"Aguardando {delay} segundos antes da próxima tentativa...\n")
            time.sleep(delay)
        else:
            print("❌ Não foi possível conectar ao site após várias tentativas.")
            exit()

# Parseando o conteúdo HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Buscando todos os blocos de endereços
addresses = soup.find_all('div', class_='address')

if not addresses:
    print("❌ Nenhum bloco de endereço encontrado. O layout do site pode ter mudado.")
    exit()

# Exibindo resultados
print("🔍 Endereços encontrados:")
print("-" * 80)

for addr_block in addresses:
    number_span = addr_block.find('span', class_='number')
    address_span = addr_block.find('span', class_='addr')
    balance_span = addr_block.find('span', class_='balance')

    # Verifica se todos os campos estão presentes
    if not all([number_span, address_span, balance_span]):
        continue

    puzzle_number = number_span.text.strip()
    btc_address = address_span.text.strip()
    balance_text = balance_span.text.strip().replace("BTC", "").strip()

    # Tenta converter o saldo para float
    try:
        balance_btc = float(balance_text)
    except ValueError:
        continue

    # Formata a saída
    print(f"Puzzle #{puzzle_number:<2} | {btc_address} | Saldo: {balance_btc:.8f} BTC")

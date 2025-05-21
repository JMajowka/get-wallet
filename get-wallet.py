import requests
from bs4 import BeautifulSoup

# Configuração
url = "https://privatekeys.pw/puzzles/bitcoin-puzzle-tx "
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36'
}

# Fazendo requisição
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("❌ Erro ao acessar o site:", response.status_code)
    exit()

# Parseando o HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Extraindo texto completo da página
content = soup.get_text()

# Informações-chave extraídas do conteúdo
info = {
    "Status": None,
    "Prize Total": None,
    "Remaining BTC": None,
    "Creator": None,
    "Start Date": None,
    "Bitcoin Address": None,
    "Last Solved": [],
    "Recommended Targets": []
}

# Extrair dados linha por linha
for line in content.split('\n'):
    line = line.strip()
    if line.startswith("Status:"):
        info["Status"] = line.replace("Status:", "").strip()
    elif line.startswith("Prize:"):
        prize_info = line.replace("Prize:", "").strip()
        info["Prize Total"] = prize_info.split(',')[0].strip()
        for part in prize_info.split(','):
            if 'remaining' in part:
                info["Remaining BTC"] = part.replace('remaining', '').strip()
    elif line.startswith("Creator:"):
        info["Creator"] = line.replace("Creator:", "").strip()
    elif line.startswith("Start Date:"):
        info["Start Date"] = line.replace("Start Date:", "").strip()
    elif line.startswith("Address:"):
        info["Bitcoin Address"] = line.replace("Address:", "").strip().replace(" ", "")
    elif "puzzle #" in line.lower() and "was solved" in line.lower():
        info["Last Solved"].append(line)
    elif "focus on solving puzzle" in line.lower() or "recommended targets" in line.lower():
        parts = line.split('#')
        for part in parts[1:]:
            number = part.split()[0].strip()
            if number.isdigit():
                info["Recommended Targets"].append(f"# {number}")

# Mostrando as informações extraídas
print("📊 Status do Puzzle Bitcoin:")
print("-" * 60)
print(f"📌 Status: {info['Status']}")
print(f"💰 Prêmio Total: {info['Prize Total']}")
print(f"🟡 BTC Restante: {info['Remaining BTC']}")
print(f"👤 Criador: {info['Creator']}")
print(f"📅 Data de início: {info['Start Date']}")
print(f"🔐 Endereço mestre: {info['Bitcoin Address']}")

if info["Last Solved"]:
    print("\n✅ Últimos puzzles resolvidos:")
    for line in info["Last Solved"]:
        print(f"   - {line}")

if info["Recommended Targets"]:
    print("\n🎯 Próximos alvos recomendados:")
    for target in info["Recommended Targets"]:
        print(f"   - {target}")

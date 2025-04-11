import requests 
import json 
import os
from dotenv import load_dotenv

from processFigmaData import process_figma_data

load_dotenv()

FIGMA_API_TOKEN = os.getenv("FIGMA_API")
FILE_ID = "pl626SjC0gXeZDzzoTalO8"

# URL da API do Figma para acessar os dados do arquivo
url = f"https://api.figma.com/v1/files/{FILE_ID}"

# Cabeçalhos para autenticação
headers = {
    "X-Figma-Token": f"{FIGMA_API_TOKEN}"
}

# Fazer a requisição para a API do Figma
response = requests.get(url, headers=headers)

# Verificar o status da resposta
if response.status_code == 200:
    figma_data = response.json()
    dataset = process_figma_data(figma_data)

    # Exibir o dataset gerado
    print(json.dumps(dataset, indent=2))

    # Salvando o dataset em um arquivo JSON
    with open('dataset_wireframes.json', 'w') as f:
        json.dump(dataset, f, indent=2)
else:
    print(f"Erro ao acessar os dados: {response.status_code}")
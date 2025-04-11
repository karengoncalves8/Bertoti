import requests 
import json 
import os
from dotenv import load_dotenv

load_dotenv()

FILE_ID = "BktXntn4CpO1aMh9dSPkJj"

# URL da API do Figma para acessar os dados do arquivo
url = f"https://api.figma.com/v1/files/{FILE_ID}"

# Cabeçalhos para autenticação
headers = {
    "Authorization": f"Bearer {FIGMA_API_TOKEN}"
}

# Fazer a requisição para a API do Figma
response = requests.get(url, headers=headers)

# Verificar o status da resposta
if response.status_code == 200:
    figma_data = response.json()
    print(figma_data)  # Exibe os dados do arquivo em formato JSON
else:
    print(f"Erro ao acessar os dados: {response.status_code}")
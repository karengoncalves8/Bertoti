import requests 
import json 
import os
from dotenv import load_dotenv

from processFigmaData import process_figma_data

# Cabeçalhos para autenticação
headers = {
    "X-Figma-Token": f""
}

data_folder = os.path.join(".", "data")
with open(os.path.join(data_folder, "loginFigma.json"), 'r', encoding='utf-8') as f:
    figma_jsons = json.load(f)

login_dataset = []

for data in figma_jsons:
    # URL da API do Figma para acessar os dados do arquivo
    url = f"https://api.figma.com/v1/files/{data['file_id']}"

    # Fazer a requisição para a API do Figma
    response = requests.get(url, headers=headers)

    # Verificar o status da resposta
    if response.status_code == 200:
        figma_data = response.json()
        try:
            output = process_figma_data(figma_data)
            login_dataset.append({"prompt": data['prompt'], "output": output})
        except Exception as e:
            print(f"Erro ao processar os dados do Figma para o file_id {data['file_id']}: {str(e)}")
    else:
        print(f"Erro ao acessar os dados do Figma para o file_id {data['file_id']}: {response.status_code} - {response.text}")
        
# Salvando o dataset em um arquivo JSON
datasets_folder = os.path.join(".", "models", "datasets")
with open(os.path.join(datasets_folder, "login_wireframes_dataset.jsonl") , 'w', encoding='utf-8') as f:
     for item in login_dataset:
        json.dump(item, f, ensure_ascii=False)
        f.write('\n') 
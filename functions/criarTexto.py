import os
import re
import unicodedata
import ollama
from datetime import datetime
from pathlib import Path

def obter_pasta_downloads():
    if os.name == 'nt':  # Windows
        return str(Path.home() / "Downloads")
    elif os.name == 'posix':  # Linux/macOS
        return str(Path.home() / "Downloads")
    else:
        raise Exception("Sistema operacional não suportado")

def gerar_nome_relatorio(texto):
    try:
        resposta = ollama.chat(
            model="gemma:2b",
            messages=[
                {"role": "system", "content": "Gere um nome curto (máximo 3 palavras) e objetivo para um arquivo baseado no texto. O nome deve estar em português, ser direto, sem frases longas, sem números, sem listas, sem abreviações e sem pontuação. Use apenas palavras chaves relacionadas ao conteúdo."},
                {"role": "user", "content": texto}
            ]
        )
        nome_gerado = resposta['message']['content'].strip()

        nome_gerado = nome_gerado.replace("\n", " ").strip()

        nome_gerado = unicodedata.normalize('NFKD', nome_gerado).encode('ASCII', 'ignore').decode('utf-8')

        nome_gerado = re.sub(r'[^\w\s-]', '', nome_gerado)  # Remove caracteres especiais
        nome_gerado = re.sub(r'\s+', '_', nome_gerado)  # Substitui espaços por "_"

        if not nome_gerado:
            nome_gerado = "Relatorio_" + datetime.today().strftime('%Y-%m-%d')

        pasta_downloads = obter_pasta_downloads()

        return os.path.join(pasta_downloads, nome_gerado)
    
    except Exception as e:
        return os.path.join(obter_pasta_downloads(), f"Relatorio_{datetime.today().strftime('%Y-%m-%d')}")  # fallback seguro

def criar_estrutura(texto, nome_relatorio):
    os.makedirs(nome_relatorio, exist_ok=True)

    arquivos = [
        {"caminho": f"{nome_relatorio}/resumo.txt", "conteudo": texto}
    ]

    for file in arquivos:
        with open(file["caminho"], "w", encoding="utf-8") as f:
            f.write(file["conteudo"])  

    return {"diretorio": nome_relatorio, "arquivos": arquivos}

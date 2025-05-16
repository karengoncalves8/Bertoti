import os
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv

load_dotenv()

hf = os.getenv("HH_TOKEN")

MODEL_ID = "google/flan-t5-large"

# Carrega tokenizer e modelo uma única vez
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=hf)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID, token=hf)

def obter_pasta_downloads() -> str:
    return str(Path.home() / "Downloads")

def gerar_nome_relatorio(texto: str) -> str:
    prompt = f"Gerar um título curto em português (máx. 3 palavras) para:\n\n{texto}"
    try:
        # tokeniza e trunca entrada em 512 tokens
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        # gera título
        outputs = model.generate(
            **inputs,
            max_length=10,
            num_beams=5,
            early_stopping=True
        )
        nome = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        # normalização e limpeza
        nome = unicodedata.normalize('NFKD', nome) \
                         .encode('ASCII', 'ignore') \
                         .decode('utf-8')
        nome = re.sub(r'[^\w\s]', '', nome)
        nome = re.sub(r'\s+', '_', nome)
        if not nome:
            raise ValueError("Título vazio")
    except Exception:
        nome = "Relatorio_" + datetime.today().strftime('%Y-%m-%d')
    return os.path.join(obter_pasta_downloads(), nome)

def salvar_texto_no_arquivo(texto: str, nome_relatorio: str) -> str:
    # Prepara o caminho do arquivo (com o nome gerado)
    arquivo_saida = (
        nome_relatorio
        if nome_relatorio.endswith('.txt')
        else nome_relatorio + '.txt'
    )
    
    # Garante que o diretório de saída existe
    os.makedirs(os.path.dirname(arquivo_saida), exist_ok=True)
    
    # Salva o texto original no arquivo
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write(texto)

    return texto

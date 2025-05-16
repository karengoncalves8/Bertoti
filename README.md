**Como executar**

    python -m venv venv

    .\venv\Scripts\activate

    pip install -r requirements.txt

    uvicorn app:app --host 0.0.0.0 --port {PORTA} --reload

**Endpoints**

    Acessar localhost:{PORTA}/docs

**FIGMA GENERATOR**
    
    Funções relacionadas ao Figma Generator disponíveis:
        - Gerar dataset -> utils/generateDatasets.py: Necessário um token do figma e uma arquivo de lista de jsons com a seguinte estrutura:  
            {
                "file_id": Id do arquivo do figma (deve ser público),
                "prompt": prompt/pergunta do usuário que iria gerar o resultado do figma 
            }
        - Fine Tunnig do modelo GPT2 -> models/fineTuningGPT2.py: Treina o modelo com um determinado dataset
        - Upload dataset para o Hugging Face -> utils/uploadDataset.py: Faz o upload do dataset local para o repositório do HF (atente-se para mudar o caminho do arquivo)
        - Upload modelo para o Hugging Face -> utils/uploadModel.py: Faz o upload do modelo local para o repositório do HF (atente-se para mudar o caminho do arquivo) 
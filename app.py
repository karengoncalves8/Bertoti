from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from functions.criarTexto import gerar_nome_relatorio, criar_estrutura

app = FastAPI()

class RelatorioRequest(BaseModel):
    texto: str

@app.post("/criar")
async def criar_relatorio(request: RelatorioRequest):
    try:
        nome_relatorio = gerar_nome_relatorio(request.texto)  
        estrutura = criar_estrutura(request.texto, nome_relatorio)  

        return {"status": "ok", "mensagem": "Relatório criado com sucesso!", "estrutura": estrutura}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
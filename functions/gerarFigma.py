import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Carregar o modelo fine-tunado (GPT-2)
model = GPT2LMHeadModel.from_pretrained("..\\fine_tuned_gpt2\\")
tokenizer = GPT2Tokenizer.from_pretrained("..\\fine_tuned_gpt2\\")

# Definir o pad_token_id explicitamente (se necessário)
tokenizer.pad_token = tokenizer.eos_token  # Definindo o token de pad como o token de fim de sequência

# Função para gerar o JSON do wireframe com o modelo fine-tunado
def gerar_json_wireframe(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=512, num_return_sequences=1)
    resposta = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Tentar converter a resposta para um JSON válido
    try:
        resposta_json = json.loads(resposta)
        return resposta_json
    except json.JSONDecodeError:
        # Caso a resposta não seja um JSON válido, retornar um aviso ou manipulação personalizada
        return {"error": "Não foi possível gerar um JSON válido"}

# Testar com um novo prompt
prompt = "Crie um wireframe de uma página de cadastro com nome, email e senha."
json_resposta = gerar_json_wireframe(prompt)

print(json_resposta)

import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Caminho para o modelo fine-tunado
model_path = "C:\\Users\\Autaza\\Documents\\Fatec\\Bertoti\\fine_tuned_gpt2"

# Carregar modelo e tokenizer
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token  # Necessário para compatibilidade

# Função para gerar saída
def gerar_json_wireframe(prompt):
    prompt_formatado = f"{prompt}\n"  # Formatação do prompt
    inputs = tokenizer.encode(prompt_formatado, return_tensors="pt")
    
    # Criação da atenção de máscara
    attention_mask = (inputs != tokenizer.pad_token_id).long()

    # Geração com máscara de atenção
    outputs = model.generate(
        inputs,
        max_length=512,
        num_return_sequences=1,
        do_sample=True,            # Sampling ajuda a evitar repetições
        top_k=20,                  # Limita a escolha de tokens aos top 50
        top_p=0.95,                # Nucleus sampling
        temperature=0.2,           # Aleatoriedade controlada
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
        attention_mask=attention_mask  # Passa a máscara de atenção
    )

    resposta = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extrair somente o que vem após o prompt
    resposta_limpa = resposta.replace(prompt_formatado, "").strip()

    print("🧠 Saída bruta do modelo:\n", resposta_limpa)

    # Tenta converter a parte útil em JSON
    try:
        return json.loads(resposta_limpa)
    except json.JSONDecodeError:
        return {"error": "Não foi possível gerar um JSON válido", "raw": resposta_limpa}

# Teste
prompt = "Crie um wireframe de uma página de cadastro com nome, email e senha."
resultado = gerar_json_wireframe(prompt)

print("\n✅ Resultado final:")
print(json.dumps(resultado, indent=2))

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os 
from dotenv import load_dotenv

load_dotenv()

hf = os.getenv("HH_TOKEN")

# Function to generate wireframe JSON output based on a text prompt
def gerar_json_wireframe(prompt):
    # Load the pretrained model and tokenizer from Hugging Face Hub
    model = GPT2LMHeadModel.from_pretrained("karencgoncalves/figma_wireframe_generator", token=hf)
    tokenizer = GPT2Tokenizer.from_pretrained("karencgoncalves/figma_wireframe_generator", token=hf)

    # Set the padding token to be the end-of-sequence token (needed for some generation configs)
    tokenizer.pad_token = tokenizer.eos_token  

    # Format the prompt by adding a newline character at the end
    prompt_formatado = (
        prompt +
        """
    Formato esperado (exemplo de saída):
    {
    "elements": [
        {"type": "input", "name": "Email", "position": {"x": 10, "y": 20}, "size": {"width": 200, "height": 30}},
        {"type": "input", "name": "Senha", "position": {"x": 10, "y": 70}, "size": {"width": 200, "height": 30}},
        {"type": "button", "name": "Login", "position": {"x": 10, "y": 120}, "size": {"width": 200, "height": 40}}
    ]
    }
    """
    )
    
    # Encode the prompt into token IDs, returning a PyTorch tensor
    inputs = tokenizer.encode(prompt_formatado, return_tensors="pt")
    
    # Create the attention mask to tell the model which tokens are real (not padding)
    attention_mask = (inputs != tokenizer.pad_token_id).long()

    # Generate output tokens with specified decoding parameters
    outputs = model.generate(
        inputs,
        max_length=512,             # Maximum length of generated sequence
        num_return_sequences=1,     # Number of sequences to generate
        do_sample=True,             # Use sampling instead of greedy decoding to increase diversity
        top_k=20,                   # Limit token selection to top 20 candidates at each step
        top_p=0.95,                 # Use nucleus (top-p) sampling to consider tokens with cumulative probability 0.95
        temperature=0.7,            # Controls randomness in generation (lower is less random)
        eos_token_id=tokenizer.eos_token_id,  # End generation when EOS token is produced
        pad_token_id=tokenizer.eos_token_id,  # Use EOS token as padding token ID for generation
        attention_mask=attention_mask          # Pass attention mask so model ignores padding tokens
    )

    # Decode generated tokens back to string, skipping special tokens like EOS
    resposta = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove the original prompt from the generated text to keep only the generated content
    resposta_limpa = resposta.replace(prompt_formatado, "").strip()

    return resposta_limpa

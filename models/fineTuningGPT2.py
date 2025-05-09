import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# Carrega modelo e tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token  # GPT2 não tem pad_token, usamos o eos_token

# Caminho do dataset
login_dataset_path = "C:\\Users\\Autaza\\Documents\\Fatec\\Bertoti\\models\\datasets\\login_wireframes_dataset.jsonl"

# Carrega o dataset
raw_dataset = load_dataset("json", data_files=login_dataset_path)["train"]

# Divide dataset: 80% treino, 10% validação, 10% teste
split_dataset = raw_dataset.train_test_split(test_size=0.2, seed=42)
valid_test = split_dataset["test"].train_test_split(test_size=0.5, seed=42)
dataset = {
    "train": split_dataset["train"],
    "validation": valid_test["train"],
    "test": valid_test["test"]
}

# Pré-processamento no formato input + output concatenado
def preprocess_dataset(batch):
    prompts = [str(p) for p in batch["prompt"]]
    outputs = [str(o) for o in batch["output"]]

    combined = [f"{prompt}\n{output}" for prompt, output in zip(prompts, outputs)]

    tokenized = tokenizer(combined, padding="max_length", truncation=True, max_length=512)
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

# Aplica a tokenização em todos os splits
tokenized_dataset = {
    split: dataset[split].map(preprocess_dataset, batched=True)
    for split in dataset
}

# Argumentos de treinamento
training_args = TrainingArguments(
    output_dir="./results",
    eval_steps=500,
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=10,
    weight_decay=0.01,
    logging_dir='./logs',
    save_total_limit=2,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"]
)

# Treina
trainer.train()

# Avaliação final no conjunto de teste
metrics = trainer.evaluate(tokenized_dataset["test"])
print("Test set evaluation metrics:", metrics)

# Salva o modelo e tokenizer fine-tunados
model.save_pretrained("./fine_tuned_gpt2")
tokenizer.save_pretrained("./fine_tuned_gpt2")

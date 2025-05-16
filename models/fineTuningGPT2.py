import os
from huggingface_hub import HfApi
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# Loading the model and its tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token  

# Hugging Face authentication 
api = HfApi()
hf_token = ""

# Loading dataset from hugging face repository
dataset = load_dataset("karencgoncalves/login_wireframe_json", use_auth_token=hf_token)

# Spliting the dataset between: 80% for train, 10% to evaluation and 10% to test
split_dataset = dataset["train"].train_test_split(test_size=0.2, seed=42)
valid_test = split_dataset["test"].train_test_split(test_size=0.5, seed=42)

# Final dataset 
dataset = {
    "train": split_dataset["train"],
    "validation": valid_test["train"],
    "test": valid_test["test"]
}

# Pre-processing dataset in concatened input + output (expected structure by GPT2)
def preprocess_dataset(batch):
    prompts = [str(p) for p in batch["prompt"]]
    outputs = [str(o) for o in batch["output"]]

    combined = [f"{prompt} em JSON. \n Resultado esperado: {output}" for prompt, output in zip(prompts, outputs)]
    print('combined', combined)
    tokenized = tokenizer(combined, padding="max_length", truncation=True, max_length=512)
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

# Aplyig tokenization at all datasets splits
tokenized_dataset = {
    split: dataset[split].map(preprocess_dataset, batched=True)
    for split in dataset
}

# Training args
training_args = TrainingArguments(
    output_dir="./results",  # Folder to save the results/metrics
    eval_steps=500,
    save_strategy="epoch", # Rate training at each epoch (epoch is the number of iterations over the dataset, how many times it will be processed
    learning_rate=2e-5, # Learning rate (how fast the model will reajust weights)
    per_device_train_batch_size=4, # Size of training batch (subset/slice of the dataset) - number of inputs the model will process each time
    per_device_eval_batch_size=4, # Size of validation batch 
    num_train_epochs=10,  # number of epochs 
    weight_decay=0.01,  # controls the weights of the model - helps generalization of the model (avoid overfitting)
    save_total_limit=2, 
)

# Creating Trainer object
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"]
)

# Initializing training
trainer.train()

# Final evaluation at test set
metrics = trainer.evaluate(tokenized_dataset["test"])
print("Test set evaluation metrics:", metrics)

# Saving fine tunned models
model.save_pretrained("./fine_tuned_gpt2")
tokenizer.save_pretrained("./fine_tuned_gpt2")

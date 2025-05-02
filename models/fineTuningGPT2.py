import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# Load model and its tokenizer 
model = GPT2LMHeadModel.from_pretrained("gpt2")  # download the model the first time
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Set pad_token as eos_token
tokenizer.pad_token = tokenizer.eos_token

# Load dataset (make sure the path is correct)
login_dataset_path = "D:\\FATEC\\3 sem\\Bertoti\\models\\datasets\\login_wireframes_dataset.jsonl"
dataset = load_dataset("json", data_files=login_dataset_path)

# Pre processing dataset - tokenizing prompts (inputs) and expected results (targets)
def preprocess_dataset(dataset):
    inputs = dataset["prompt"]
    targets = dataset["output"]
    
    inputs = [str(i) for i in inputs]
    targets = [str(t) for t in targets]
    
    # Tokenizando os dados
    model_inputs = tokenizer(inputs, padding=True, truncation=True, max_length=512, return_tensors="pt")
    labels = tokenizer(targets, padding=True, truncation=True, max_length=512, return_tensors="pt")
    
    # Adicionando as labels ao dicionário de entradas
    model_inputs["labels"] = labels["input_ids"]
    
    return model_inputs

# Applying pre processing
tokenized_dataset = dataset.map(preprocess_dataset, batched=True)

# Training the model 
training_args = TrainingArguments(
    output_dir="./results",  # Folder to save the model
    eval_steps=500,   # Evaluate every 500 steps 
    no_cuda=True, 
    learning_rate=2e-5,  # Learning rate (how fast the model will readjust weights)
    per_device_train_batch_size=2,  # Size of training batch (subset/slice of the dataset) - number of inputs the model will process each time
    per_device_eval_batch_size=2,  # Size of validation batch 
    num_train_epochs=3,  # number of epochs (epoch is the number of iterations over the dataset, how many times it will be processed)
    weight_decay=0.01,  # Controls the weights of the model - helps generalization of the model (avoid overfitting)
    logging_dir='./logs', 
)

# Creating Trainer object
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"]
)

# Initializing training
trainer.train()

# Saving fine-tuned models
model.save_pretrained("./fine_tuned_gpt2")
tokenizer.save_pretrained("./fine_tuned_gpt2")

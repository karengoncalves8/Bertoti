
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# Load model and its tokenizer 
model = GPT2LMHeadModel.from_pretrained("gpt2") # download its model only the first time
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Load dataset
dataset = load_dataset("json", data_files={"train": "data.jsonl"})

# Pre processing dataset - tokenizing prompts (inputs) and expected results (targets)
def preprocess_dataset(dataset):
    # List of the inputs at dataset
    inputs = [data["prompt"] for data in dataset["train"]]
    # List of the inputs at targets
    targets = [data["output"] for data in dataset["train"]]
    
    # Tokenizing the lists
    # Tokenizer args: - max_lenght: maximum amount of tokens; - truncation: in case it reaches max_lenght, truncate it (cut some of it); - padding: if its shorter than max_lenght, it will be filled. 
    # Basically, makes sure every input has the same size
    model_inputs = tokenizer(inputs, max_lenght=512, truncation=True, padding="max_lenght")
    labels = tokenizer(targets, max_lenght=512, truncation=True, padding="max_lenght")
    
    # Adding the labels to input dictionary
    model_inputs["labels"] = labels["inputs_id"]
    
    return model_inputs

# Applying pre processing
tokenized_dataset = dataset.map(preprocess_dataset, batched=True)

# Training the model 
training_args = TrainingArguments(
    output_dir="./results", # Folder to save the model
    evaluation_strategy="epoch", # Rate training at each epoch (epoch is the number of iterations over the dataset, how many times it will be processed)
    learning_rate=2e-5, # Learning rate (how fast the model will reajust weights)
    per_device_train_batch_size=8, # Size of training batch (subset/slice of the dataset) - number of inputs the model will process each time
    per_device_eval_batch_size=8, # Size of validation batch 
    num_train_epochs=3, # number of epochs 
    weight_decay=0.01, # controls the weights of the model - helps generalization of the model (avoid overfitting)
)

# Creating Trainer object
trainer = Trainer(
    model = model,
    args = training_args,
    train_dataset=tokenized_dataset["train"]
)

# Initializing training
trainer.train()

# Saving fine tunned models
model.save_pretrainer("./fine_tuned_gpt2")
tokenizer.save_pretrained("./fine_tuned_gpt2")
import os
import requests
import numpy as np
from datasets import load_dataset
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, f1_score

# --- STEP 1: LOCAL DATA DOWNLOAD BYPASS ---
print("--- Step 1: Downloading Data Manually ---")
os.makedirs("data", exist_ok=True)

def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {url}...")
        r = requests.get(url, allow_redirects=True)
        with open(filename, 'wb') as f:
            f.write(r.content)
        print("Done.")

train_url = "https://huggingface.co/datasets/ag_news/resolve/main/data/train-00000-of-00001.parquet"
test_url = "https://huggingface.co/datasets/ag_news/resolve/main/data/test-00000-of-00001.parquet"

download_file(train_url, "data/train.parquet")
download_file(test_url, "data/test.parquet")

dataset = load_dataset("parquet", data_files={"train": "data/train.parquet", "test": "data/test.parquet"})

# --- STEP 2: TOKENIZING ---
print("--- Step 2: Tokenizing ---")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

train_set = dataset["train"].shuffle(seed=42).select(range(1000))
test_set = dataset["test"].shuffle(seed=42).select(range(200))

tokenized_train = train_set.map(tokenize_function, batched=True)
tokenized_test = test_set.map(tokenize_function, batched=True)

# --- STEP 3: FINE-TUNING BERT ---
print("--- Step 3: Training (Fine-Tuning) ---")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=4)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    acc = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average="weighted")
    return {"accuracy": acc, "f1": f1}

# FIXED: 'eval_strategy' instead of 'evaluation_strategy' for latest transformers
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch", 
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    num_train_epochs=1,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,
    compute_metrics=compute_metrics,
)

trainer.train()

# --- STEP 4: SAVE THE MODEL ---
print("--- Step 4: Saving Model ---")
os.makedirs("./fine_tuned_bert", exist_ok=True)
model.save_pretrained("./fine_tuned_bert")
tokenizer.save_pretrained("./fine_tuned_bert")

print("\nSUCCESS: Model saved to './fine_tuned_bert'.")
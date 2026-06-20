# Presswire - Obsidian Intelligence

Presswire is a high-performance news topic classification application. It uses a fine-tuned BERT model to categorize news headlines into four distinct categories: World, Sports, Business, and Sci/Tech.

## Project Overview

This project implements a complete NLP pipeline, covering data acquisition, transformer fine-tuning, and a professional-grade deployment using Streamlit with a custom "Obsidian Black" UI.

## Prerequisites

Ensure you have Python 3.9+ installed. It is highly recommended to use a virtual environment:

```bash
# Create and activate virtual environment
python -m venv venv

# On Windows:
.\venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Workflow & Execution

### 1. Data Preparation & Training

The `train.py` script automates the full training lifecycle.

```bash
python train.py
```

#### Process:

- **Downloads:** Fetches the AG News dataset in Parquet format.
- **Tokenizes:** Preprocesses the text data using BertTokenizer.
- **Fine-Tunes:** Trains the `bert-base-uncased` model using the Hugging Face Trainer API.
- **Saves:** Exports the fine-tuned model, tokenizer, and configuration files to the `./fine_tuned_bert` directory.

### 2. Launching the Application

Once the model directory is created, launch the interactive dashboard:

```bash
streamlit run app.py
```

The application will open in your default browser (usually at `http://localhost:8501`).

## Project Structure

- `app.py`: The main Streamlit dashboard application with custom CSS.
- `train.py`: Training script for fine-tuning BERT.
- `requirements.txt`: Project dependency list.
- `./fine_tuned_bert/`: Directory containing the trained model.
- `./data/`: Dataset storage (tracked via Git LFS).
- `./results/`: Training checkpoints and logs (tracked via Git LFS).

## Skills Gained

- **NLP using Transformers:** Working with BERT and Hugging Face libraries.
- **Transfer Learning:** Fine-tuning pre-trained models on custom classification tasks.
- **Evaluation Metrics:** Utilizing accuracy and F1-score for performance tracking.
- **Lightweight Deployment:** Building functional, aesthetically pleasing UIs with Streamlit.
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
import os

# Download and save DistilBERT model and tokenizer
try:
    model_name = "distilbert-base-uncased"
    model = DistilBertForSequenceClassification.from_pretrained(model_name)
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)

    os.makedirs("models", exist_ok=True)
    model.save_pretrained("models/distilbert")
    tokenizer.save_pretrained("models/distilbert")
except Exception as e:
    print(f"Error downloading or saving model: {e}")
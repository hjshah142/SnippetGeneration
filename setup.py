import nltk
import tensorflow_hub as hub
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from fastai.text.learner import load_learner

nltk.download('punkt')
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
embeddings = embed([
    "The quick brown fox jumps over the lazy dog.",
    "I am a sentence for which I would like to get its embedding", "Agree?"])

print(embeddings)
tokenizer = AutoTokenizer.from_pretrained("chkla/roberta-argument")
arg_model = AutoModelForSequenceClassification.from_pretrained("chkla/roberta-argument")
print(arg_model.config)
model_path = "../pretrained_models"
claim_classifier = load_learner(model_path)
print(claim_classifier)
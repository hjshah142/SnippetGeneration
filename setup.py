import nltk
import tensorflow_hub as hub

nltk.download('punkt')


embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
embeddings = embed([
    "The quick brown fox jumps over the lazy dog.",
    "I am a sentence for which I would like to get its embedding", "Agree?"])

print(embeddings)



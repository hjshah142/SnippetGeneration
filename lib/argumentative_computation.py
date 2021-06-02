from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import fastai
import os
from fastai.text import *


class ArgumentativeComputation:
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        # model_dir = "C:\\Users\\harsh\\Downloads\\HuggingFaceModels"
        ''' Pretrained_model: https://huggingface.co/chkla/roberta-argument'''
        self.tokenizer = AutoTokenizer.from_pretrained("chkla/roberta-argument")
        self.arg_model = AutoModelForSequenceClassification.from_pretrained("chkla/roberta-argument" )
        # self.model_path = r"C:\Users\harsh\OneDrive - mail.uni-paderborn.de\pretrained_models"
        self.model_path = os.path.join(script_dir, "../../pretrained_models")

        self.claim_classifier = load_learner(self.model_path)

        # predicted_prob = self.predict_argumentative_score(
        #  "In 2011 there were about 730,322 abortions reported to the centers for disease control.")
        # print(predicted_prob)

    def predict_argumentative_score(self, sentence):
        """predict probability of sentence representing argumentative structure"""
        tokenized_sentence = self.tokenizer(
            sentence,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )

        pt_outputs = self.arg_model(**tokenized_sentence)
        pt_predictions = F.softmax(pt_outputs.logits, dim=-1)
        predicted_prob = pt_predictions.detach().numpy()
        arg_prob = predicted_prob[0][1]
        return arg_prob

    def predict_claim_probability(self, text):
        """predict probability of sentence representing a claim

        awd_lstm model fine-tuned on IMHO claim dataset (IMHO Fine-Tuning Improves Claim Detection Tuhin Chakrabarty, Christopher Hidey, Kathy McKeown )
        """

        preds = self.claim_classifier.predict(text)
        prob_tensor = preds[2][1]
        prob = prob_tensor.item()
        # print(type(prob))
        return prob

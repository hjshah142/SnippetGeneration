import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import os
from fastai.text.learner import load_learner
import warnings


class ArgumentativeComputation:
    def __init__(self):
        """
        fine-tuned two models from argumentation mining domain to measure the argumentativeness of the sentence:
        Argumentative SentenceClassifier. In this section we provide implementation details for building this mod

        """
        script_dir = os.path.dirname(__file__)
        # model_dir = "C:\\Users\\harsh\\Downloads\\HuggingFaceModels"
        ''' Pretrained_model: https://huggingface.co/chkla/roberta-argument'''
        self.tokenizer = AutoTokenizer.from_pretrained("chkla/roberta-argument")
        self.arg_model = AutoModelForSequenceClassification.from_pretrained("chkla/roberta-argument")
        # self.model_path = r"C:\Users\harsh\OneDrive - mail.uni-paderborn.de\pretrained_models"
        self.model_path = os.path.join(script_dir, "../../pretrained_models2")
        # specify gpu if available for prediction
        # self.device = torch.cuda.is_available()
        self.claim_classifier = load_learner(self.model_path)

    def predict_argumentative_score(self, sentence):
        """predict probability of sentence representing argumentative structure.
        Uses RobERTArg model from the Transformers library (https://huggingface.co/chkla/roberta-argument)[6]
        to compute the argumentative score of the sentence.Model is fine-tuned on trained on 25k manually annotated
        sentences from cross topic argumentation mining dataset [7] (Stab et al. 2018 )"""
        tokenized_sentence = self.tokenizer(
            sentence,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )
        with torch.no_grad():
        # pt_outputs = self.arg_model(**tokenized_sentence.to(self.device))
            pt_outputs = self.arg_model(**tokenized_sentence)
            pt_predictions = F.softmax(pt_outputs.logits, dim=-1)
            predicted_prob = pt_predictions.detach().numpy()
            arg_prob = predicted_prob[0][1]
            return arg_prob

    def predict_claim_probability(self, text):
        """claim classifier model to predict probability of sentence representing a claim
        Model is implemented using the same approach employed by (Chakrabarty et al.,2019)[5] for claim detection.
        The model was implemented in the fastai library using the transfer learning technique
        "Universal Language Model Fine-tuning" .
        Awd_lstm model is fine-tuned on IMHO claim dataset to predict the probability of sentence  representing a claim
        (Dataset Reference: IMHO Fine-Tuning Improves Claim Detection [5] (Chakrabarty et al.,2019 )
        """
        # to ignore warning of fastai optmization for 64 bit tensor error
        warnings.filterwarnings("ignore")
        with torch.no_grad():
            preds = self.claim_classifier.predict(text)
            prob_tensor = preds[2][1]
            prob = prob_tensor.item()
            # print(type(prob))
            return prob

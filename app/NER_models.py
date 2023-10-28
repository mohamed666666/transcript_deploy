import numpy as np
import torch
from flair.data import Sentence
from flair.models import SequenceTagger
from transformers import BertTokenizerFast, BertForTokenClassification, pipeline
from transformers import AutoModelForTokenClassification, AutoTokenizer


class Ner_Models:
    def __init__(self):
        pass

    def ner_en(self,text):
    # load tagger
        tagger = SequenceTagger.load("flair/ner-english")

    # make example sentence
        sentence = Sentence(text)

    # predict NER tags
        pred = tagger.predict(sentence)
    
    # iterate over entities and print
        entities, labels = [], []
        for entity in sentence.get_spans('ner'):
            entities.append(entity.text)
            labels.append(entity.labels[0].value)
        return entities, labels

    
    def ner_es(self,text):
    # load tagger
        tagger = SequenceTagger.load("flair/ner-spanish-large")

    # make example sentence
        sentence = Sentence(text)

    # predict NER tags
        pred = tagger.predict(sentence)
    
    # iterate over entities and print
        entities, labels = [], []
        for entity in sentence.get_spans('ner'):
            entities.append(entity.text)
            labels.append(entity.labels[0].value)
        return entities, labels

    def ner_it(self,text):

        tokenizer = BertTokenizerFast.from_pretrained("osiria/bert-italian-cased-ner")
        model = BertForTokenClassification.from_pretrained("osiria/bert-italian-cased-ner")

        ner = pipeline("ner", model = model, tokenizer = tokenizer, aggregation_strategy="first")
        nlp = ner(text)
    
    # iterate over entities
        entities, labels = [], []
        for entity in nlp:
            entities.append(entity['word'])
            labels.append(entity['entity_group'])
        return entities, labels

    def ner_ar(self,text):

        ner_model = AutoModelForTokenClassification.from_pretrained("ychenNLP/arabic-ner-ace")
        ner_tokenizer = AutoTokenizer.from_pretrained("ychenNLP/arabic-ner-ace")

        ner = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer, grouped_entities=True)
        nlp = ner(text)
    
    # iterate over entities
        entities, labels = [], []
        for entity in nlp:
            entities.append(entity['word'])
            labels.append(entity['entity_group'])
        return entities, labels

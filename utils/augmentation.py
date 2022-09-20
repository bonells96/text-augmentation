from matplotlib.pyplot import text
import pandas as pd
import numpy as np
import logging
import re 
import tensorflow as tf
import nltk
from nltk.corpus import wordnet
from nltk import word_tokenize
from nltk import pos_tag
from deep_translator import GoogleTranslator
import random
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.char as nac
import inflect
import spacy

import json
from os import getcwd
from os.path import join, dirname

PATH_REPO = dirname(getcwd())

#PATH_REPO = join(dirname(getcwd()), 'ds-ModelExplainability')
PATH_CONFIG = join(PATH_REPO, 'config')


a_file = open(join(PATH_CONFIG, 'entities.json'), "r")
dict_entities = json.loads(a_file.read())

COMPANIES_ = ["Tesla", "Amazon", "Microsoft", "BMW", "Merck", "Citibeats", "Mercedes-Benz", "SEAT", "Iberia", "NTT", "Cisco"]
GPE_ = ["Spain", "Barcelona", "France", "Paris", "USA", "New York", "Senegal", "Dakar", "Tunisia", "Tunis", 
    "Vietnam", "Hanoi", "China", "Pekin", "Brasil", "Rio janeiro", "Mexico", "Bolivia", "Venezuela", "Caracas", "Italy",
    "Rome", "Hawai"]
PERSON_ = ["Obama", "Michelle", "Meryem", "Arnault", "Mehdi", "Alex", "Raphinha", "Priya", "Ana", "Valeria"]
NORP_ = ["spanish", "american", "african", "vietnamese", "cambodian", "french", "catholic", "muslim", "budist"]

COMPANIES_ = [entity for entity, value in dict_entities.items() if value=='ORG']
GPE_ = [entity for entity, value in dict_entities.items() if value=='GPE']
PERSON_ = [entity for entity, value in dict_entities.items() if value=='PERSON']
NORP_ = [entity for entity, value in dict_entities.items() if value=='NORP']
PRODUCT_ = [entity for entity, value in dict_entities.items() if value=='PRODUCT']



def augmentation_tests(dict_tests):
    """
    Augment the tests data
    """
    # Create the dictionnary of augmented tests
    dict_augmented_tests = {}
    dict_augmented_tests.update(dict_tests)

    # Use nlp aug to augment the samples
    aug = naw.ContextualWordEmbsAug(model_path='bert-base-uncased', action="insert")
    dict_augmented_tests.update({aug.augment(text)[0]:label for text, label in dict_tests.items()})

    # Use wordnet synonims to augment the samples 
    dict_augmented_tests.update({get_syn_sentence(text):label for text, label in dict_tests.items()})

    # Use wordnet antonyms to augment the samples
    dict_augmented_tests.update({get_neg_ant_sentence(text):label for text, label in dict_tests.items()})

    # Use backtranslation
    dict_augmented_tests.update({backtranslate_text(text):label for text, label in dict_tests.items()})

    # Use nlp character augmenter to augment samples with noise
    aug_char = nac.OcrAug() 
    dict_augmented_tests.update({aug_char.augment(text)[0]:label for text, label in dict_tests.items()})

    dict_augmented_tests.update({ner_augment(text):label for text, label in dict_tests.items()})

    dict_augmented_tests.update({plural_transform(text):label for text, label in dict_tests.items()})

    dict_augmented_tests.update({singular_transform(text):label for text, label in dict_tests.items()})



    return dict_augmented_tests
  

def get_synonyms(word, pos=None):
    """
    Get the synonym of a word

    Inputs:
        - word, str
        - pos, str: the pos of the word -> verb, noun, adjective etc...
    
    Output: a synonim of the word
    """
    wordnet_pos = {
        "NN": wordnet.NOUN,
        "NNS":wordnet.NOUN,
        #"VB": wordnet.VERB,
        #"VBD": wordnet.VERB,
        #"VBG": wordnet.VERB,
        #"VBN": wordnet.VERB,
        #"VBP": wordnet.VERB,
        "JJ": wordnet.ADJ,
        "JJS":wordnet.ADJ
        #"RB": wordnet.ADV,
        #"RBR": wordnet.ADV,
        #"RBS": wordnet.ADV,
    }
    if pos:
        if pos in list(wordnet_pos.keys()):
            synsets = wordnet.synsets(word, pos=wordnet_pos[pos])
            synonyms = []
            for synset in synsets:
                synonyms += [str(lemma.name()) for lemma in synset.lemmas()]
            synonyms = [synonym.replace("_", " ") for synonym in synonyms]
            synonyms = list(set(synonyms))
            synonyms = [synonym for synonym in synonyms if synonym != word]
            if synonyms:
                return synonyms[0]
    return ''


def get_antonyms(word, pos=None):
    """
    Get the antonym of a word

    Inputs:
        - word, str
        - pos, str: the pos of the word -> verb, noun, adjective etc...
    
    Output: an antonym of the word
    """
    wordnet_pos = {
        "NN": wordnet.NOUN,
        "NNS":wordnet.NOUN,

        #"VB": wordnet.VERB,
        #"VBD": wordnet.VERB,
        #"VBG": wordnet.VERB,
        #"VBN": wordnet.VERB,
        #"VBP": wordnet.VERB,
        "JJ": wordnet.ADJ,
        "JJS":wordnet.ADJ

        #"RB": wordnet.ADV,
        #"RBS": wordnet.ADV,
        #"RBR": wordnet.ADV,
    }
    if pos:
        if pos in list(wordnet_pos.keys()):
            synsets = wordnet.synsets(word, pos=wordnet_pos[pos])
            antonyms = []
            for synset in synsets:
                antonyms += [str(antonym.antonyms()[0].name()) for antonym in synset.lemmas() if antonym.antonyms()]
            antonyms = [antonym.replace("_", " ") for antonym in antonyms]
            antonyms = list(set(antonyms))
            antonyms = [antonym for antonym in antonyms if antonym != word]
            if antonyms:
                return antonyms[0]
    return ''


def get_syn_sentence(text):
    """
    Changes the word that are nouns or adjectives in a sentence by their synonim
    """
    words = text.split()
    words_with_pos_tag = pos_tag(words)
    words_with_pos_tag
    new_sentence_words = []
    for word, pos in words_with_pos_tag:
        synonym = get_synonyms(word, pos)
        if synonym:
            new_sentence_words.append(synonym)
        else:
            new_sentence_words.append(word)
    synonym_sentence = ' '.join(new_sentence_words)
    return synonym_sentence


def get_neg_ant_sentence(text):
    """
    Changes the word that are nouns or adjectives in a sentence by "not" +  antonym
    """
    words = text.split()
    words_with_pos_tag = pos_tag(words)
    words_with_pos_tag
    new_sentence_words = []
    for word, pos in words_with_pos_tag:
        antonym = get_antonyms(word, pos)
        if antonym:
            new_sentence_words.append('not')
            new_sentence_words.append(antonym)
        else:
            new_sentence_words.append(word)
    antonym_sentence = re.sub('not not', '',(' '.join(new_sentence_words)))
    return antonym_sentence


def backtranslate_text(text):
    target_lang = random.choice(['fr', 'es', 'it'])
    translated_text = GoogleTranslator(source='en', target=target_lang).translate(text=text)
    backtranslated_text = GoogleTranslator(source=target_lang, target='en').translate(text=translated_text)
    return backtranslated_text


def ner_augment(text):
    """
    Creates a new text by replacing recognised entities with other entities
    """
    nlp = spacy.load('en_core_web_sm', disable=['tagger', 'parser', 'attribute_ruler', 'lemmatizer'])
    doc = nlp(text)
    ents = show_ents(doc)
    if ents:
        diff_words = 0
        for ent in ents:
            if ent["label"]=="GPE":
                new_word = random.choice(GPE_)
            elif ent["label"]=="ORG":
                new_word = random.choice(COMPANIES_)
            elif ent["label"]=="PERSON":
                new_word = random.choice(PERSON_)
            elif ent["label"]=="PRODUCT":
                new_word = random.choice(PRODUCT_)
            elif ent["label"]=="NORP":
                new_word = random.choice(NORP_)
            else:
                continue
            text=text[:(ent['start']+diff_words)] + new_word + text[(ent["end"]+diff_words):]
            diff_words += len(new_word) - (ent["end"]-ent["start"])
    return text



def show_ents(doc):
    """
    Stores in a list the different entities recognised in a text
    """
    if doc.ents:
        ents_list = []
        for ent in doc.ents:
            ent_ = {'text':ent.text, 'label':ent.label_, 'start':ent.start_char, 'end':ent.end_char }
            ents_list.append(ent_)
        return ents_list
    else:
        return None




def plural_transform(text):
    "transforms singular nouns to plural"
    wordnet_pos = {
        "NN": wordnet.NOUN,
        "JJ": wordnet.ADJ,
    }

    p = inflect.engine()
    words = text.split()
    words_plural = []
    words_with_pos_tag = pos_tag(words)

    for word, pos in words_with_pos_tag:
        if pos in list(wordnet_pos.keys()):
            if p.plural_noun(word)==False:
                words_plural.append(word)
            else:
                words_plural.append(p.plural_noun(word))
        else:
            words_plural.append(word)
    return ' '.join(words_plural)



def singular_transform(text):
    "transforms plural nouns to singular"
    wordnet_pos = {
        "NNS": wordnet.NOUN,
        "JJS": wordnet.ADJ,
    }

    p = inflect.engine()
    words = text.split()
    words_singular = []
    words_with_pos_tag = pos_tag(words)

    for word, pos in words_with_pos_tag:
        if pos in list(wordnet_pos.keys()):
            if p.singular_noun(word)==False:
                words_singular.append(word)
            else:
                words_singular.append(p.singular_noun(word))
        else:
            words_singular.append(word)
    return ' '.join(words_singular)




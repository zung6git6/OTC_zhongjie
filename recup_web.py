#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Modules
import requests
import argparse
import spacy
from nltk.tokenize import sent_tokenize
from dataclasses import dataclass
import csv
from bs4 import BeautifulSoup

# Classe
@dataclass
class Token:
    id:int
    forme:str
    pos_tag:int
    chunk_tag:int
    ner_tag:int

# Fonctions
def recup_web(url:str)->str:
    reponse = requests.get(url)

    if reponse.status_code == 200:
        contenu_html = reponse.text
    elif reponse.status_code == 300:
        url_final = reponse.url
        reponse_finale = requests.get(url_final)
        if reponse_finale.status_code == 200:
            contenu_html = reponse_finale.text
    else:
        print("Site inachevable")

    return contenu_html

def html_parser(contenu_html:str):

    soup = BeautifulSoup(contenu_html, 'html.parser')

    corpus = ""

    for balise in soup.find_all("p", recursive=True):
        if balise.text.strip(): 
            corpus += balise.text.strip() + "\n" 

    return corpus


def get_chunk_tags(doc) -> list:

    """dict_chunk_tags = {
        0: 'O', 1: 'B-ADJP', 2: 'I-ADJP', 3: 'B-ADVP', 4: 'I-ADVP',
        5: 'B-CONJP', 6: 'I-CONJP', 7: 'B-INTJ', 8: 'I-INTJ',
        9: 'B-LST', 10: 'I-LST', 11: 'B-NP', 12: 'I-NP',
        13: 'B-PP', 14: 'I-PP', 15: 'B-PRT', 16: 'I-PRT',
        17: 'B-SBAR', 18: 'I-SBAR', 19: 'B-UCP', 20: 'I-UCP',
        21: 'B-VP', 22: 'I-VP'
    }"""


    list_chunk_tag_index = []

    # Afficher les chunks taggés
    for chunk in doc:

        chunk_tag_index = None
        
        if chunk.pos_ == "LIST":  # Liste
            chunk_tag_index = 9 if chunk.dep_ == "list" else 10
        elif chunk.pos_ == "PROPN" or chunk.pos_ == "NOUN":  # Nom propre et nom
            chunk_tag_index = 11 if chunk.i == 0 or (doc[chunk.i - 1].pos_ != "NOUN" and doc[chunk.i - 1].pos_ != "PROPN") else 12
        elif chunk.pos_ == "ADJ":  # Adj
            chunk_tag_index = 1 if chunk.i == 0 or doc[chunk.i - 1].pos_ != "ADJ" else 2
        elif chunk.pos_ == "ADP":  # Préposition
            chunk_tag_index = 13 if chunk.i == 0 or doc[chunk.i - 1].pos_ != "ADP" else 14
        elif chunk.pos_ == "VERB" or chunk.pos_ == "AUX":  # Verbe et auxiliaire
            chunk_tag_index = 21 if chunk.i == 0 or (doc[chunk.i - 1].pos_ != "VERB" and doc[chunk.i - 1].pos_ != "AUX") else 22
        elif chunk.pos_ == "ADV":  # Adv
            chunk_tag_index = 3 if chunk.i == 0 or doc[chunk.i - 1].pos_ != "ADV" else 4
        elif chunk.pos_ == "CONJ":  # Conjonction
            chunk_tag_index = 5 if chunk.i == 0 or doc[chunk.i - 1].pos_ != "CONJ" else 6
        elif chunk.pos_ == "INTJ":  # Interjection
            chunk_tag_index = 7 if chunk.i == 0 or doc[chunk.i - 1].pos_ != "INTJ" else 8
        elif chunk.pos_ == "PART":  # Particule
            chunk_tag_index = 15 if chunk.i == 0 or doc[chunk.i - 1].pos_ != "PART" else 16
        elif chunk.pos_ == "SCONJ":  # Conjonction de subordination
            chunk_tag_index = 17 if chunk.i == 0 or doc[chunk.i - 1].pos_ != "SCONJ" else 18
        elif chunk.pos_ == "X":  # Les autres
            chunk_tag_index = 19 if chunk.i == 0 or doc[chunk.i - 1].pos_ != "X" else 20
        else:
            chunk_tag_index = 0

        if chunk_tag_index is not None:
            list_chunk_tag_index.append(chunk_tag_index)

    return list_chunk_tag_index

def get_pos(doc) -> list:

    dict_pos = {0 : "ADJ", 1 : "ADP", 2 : "ADV", 
                3 : "AUX", 4 : "CCONJ", 5 : "DET",
                6 : "INTJ", 7 : "NOUN", 8 : "NUM",
                9 : "PART", 10 : "PRON", 11 : "PROPN",
                12 : "PUNCT", 13 : "SCONJ", 14 : "SYM",
                15 : "VERB", 16 : "X", 17 : "LIST"}

    list_pos_index = []

    for pos in doc:
        pos_index = -1

        for a, b in dict_pos.items():
            if pos.pos_ == b:
                pos_index = a
                list_pos_index.append(pos_index)
    return list_pos_index

def get_ner_tags(doc) -> list:
    
    # dict_ner_tags = {'O': 0, 'B-PER': 1, 'I-PER': 2, 'B-ORG': 3, 'I-ORG': 4, 'B-LOC': 5, 'I-LOC': 6, 'B-MISC': 7, 'I-MISC': 8}

    list_tags = ["NORP","FAC","PRODUCT","EVENT","WORK_OF_ART","LAW","LANGUAGE","DATE","TIME","PERCENT","MONEY","QUANTITY","ORDINAL","CARDINAL"]

    list_ner_tags = []

    for ent in doc.ents:
        ner_tag = ""
        if ent.label_ == "PERSON":
            ner_tag = "12"
        elif ent.label_ == "ORG":
            ner_tag = "34"
        elif ent.label_ == "GPE":
            ner_tag = "56"
        elif ent.label_ in list_tags:
            ner_tag = "78"
        list_ner_tags.append(ner_tag)

    return list_ner_tags

def get_tokens(corpus:str):

    nlp = spacy.load("en_core_web_sm")

    list_sents:list = sent_tokenize(corpus)
    list_sents_nlp:list = []
    list_tokens = []

    for sent in list_sents:
        sent_nlp = nlp(sent)
        list_sents_nlp.append(sent_nlp)
    
    for i, sent in enumerate(list_sents_nlp):

        list_tokens.append([])

        for tok in sent:
            token = Token(int(tok.i), str(tok.text), -1, -1, 0)
            list_tokens[-1].append(token)
        
        for ii, chunk in enumerate(get_chunk_tags(sent)):
            list_tokens[i][ii].chunk_tag = int(chunk)

        for ii, pos in enumerate(get_pos(sent)):
            list_tokens[i][ii].pos_tag = int(pos)

        for ii, ner in enumerate(get_ner_tags(sent)):
            if ner != "":
                if list_tokens[i][ii].chunk_tag % 2 != 0:
                    list_tokens[i][ii].ner_tag = int(ner[0])
                else:
                    list_tokens[i][ii].ner_tag = int(ner[1])
    
    list_dict_results = []
    for i, sent in enumerate(list_tokens):
        dict_results = {}
        list_formes = [tok.forme for tok in sent]
        list_pos = [tok.pos_tag for tok in sent]
        list_chunk = [tok.chunk_tag for tok in sent]
        list_ners = [tok.ner_tag for tok in sent]
        dict_results['ID'] = int(i)
        dict_results['tokens'] = list_formes
        dict_results['pos_tags'] = list_pos
        dict_results['chunk_tags'] = list_chunk
        dict_results['ner_tags'] = list_ners
        list_dict_results.append(dict_results)
    
    return list_dict_results


def main() -> None:

    parsing = argparse.ArgumentParser()

    parsing.add_argument("-url", type=str, required=True)

    args = parsing.parse_args()

    url = args.url

    contenu_html = recup_web(url)


    corpus = html_parser(contenu_html)

    list_dict_results = get_tokens(corpus)

    with open('tableau_output.tsv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(list_dict_results[0].keys())
        for sent in list_dict_results:
            writer.writerow([sent['ID'], sent['tokens'], sent['pos_tags'], sent['chunk_tags'], sent['ner_tags']])


    return None

# Main
if __name__ == '__main__':
    main()
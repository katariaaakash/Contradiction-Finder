from __future__ import unicode_literals

import spacy
import requests
from nltk.corpus import wordnet

nlp = spacy.load('en')

def noun_extractor(document, nouns):
    for word in document:
        if(word.pos_ == 'PROPN' or word.pos_ == 'NOUN'):
            nouns.append(word)

def antonym_finder_by_nltk(word1, word2):
    for syn in wordnet.synsets(word1):
        for l in syn.lemmas():
            if l.antonyms():
                if l.antonyms()[0].name() == word2:
                    return 1
    return 0

def maximum_number(num1, num2):
    if num1 > num2:
        return num1
    return num2

def contradiction_finder(sentence_1, sentence_2):
    doc_1 = nlp(u'' + sentence_1)
    doc_2 = nlp(u'' + sentence_2)
    nouns_sentence_1 = []
    nouns_sentence_2 = []
    noun_extractor(doc_1, nouns_sentence_1)
    noun_extractor(doc_2, nouns_sentence_2)
    similarity_score = 0
    for word_1 in nouns_sentence_1:
        for word_2 in nouns_sentence_2:
            similarity_score += word_1.similarity(word_2)
    for word_1 in nouns_sentence_2:
        for word_2 in nouns_sentence_1:
            similarity_score += word_1.similarity(word_2)

    antonym_count = 0
    for word1 in doc_1:
        for word2 in doc_2:
            antonym_found = 0
            antonym_found = antonym_finder_by_nltk(word1.text, word2.text)
            antonym_count += antonym_found

    negation_count_1 = 0
    negation_count_2 = 0
    for word in doc_1:
        if ("not" in word.text.lower() or "'nt" in word.text.lower()):
            negation_count_1 += 1
    for word in doc_2:
        if ("not" in word.text.lower() or "'nt" in word.text.lower()):
            negation_count_2 += 1

    contradiction = 0
    probability_contradiction = 0
    len_1 = len(sentence_1.split(' '))
    len_2 = len(sentence_2.split(' '))
    if similarity_score > 0.5:
        probability_contradiction += (antonym_count / maximum_number(len_1, len_2)) * 65
        if negation_count_1 > 0 or negation_count_2 > 0:
            probability_contradiction += (abs(negation_count_1 - negation_count_2) / maximum_number(negation_count_1, negation_count_2)) * 35

    if probability_contradiction > 0.3:
        print("Sentences contradicts")
    else:
        print("Sentences do not contradicts")

sentence_1 = input("Enter Sentence 1 ")
sentence_2 = input("Enter Sentence 2 ")
contradiction_finder(sentence_1, sentence_2)


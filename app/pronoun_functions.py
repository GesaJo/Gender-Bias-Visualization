"""Functions to swap pronouns in input-sentences."""

import re
from nltk import pos_tag, word_tokenize


f = open("data/gendered_words_list.txt", 'r')
gendered_words = f.read()
f.close()
gendered_words = gendered_words.split(', ')

g_pronouns = ["he", "she", "him", "her", "his", "her", "himself", "herself"]


def swap(sentence):
    """function that does part-of-speech tagging on the text,
        swaps gendered nouns and pronouns with their counterparts
        and returns the sentence as a list of words."""

    tagged = pos_tag(word_tokenize(sentence))
    words = [i[0] for i in tagged]
    words = [w.lower() for w in words]
    tags = [i[1] for i in tagged]
    gender = "Another"
    swapped = []
    for n, word in enumerate(words):
        if word in gendered_words:
            if gendered_words.index(word) % 2 == 0:  # male
                swapped.append(gendered_words[gendered_words.index(word)+1])
            else:
                swapped.append(gendered_words[gendered_words.index(word)-1])
        elif tags[n] == 'PRP$' and word == "his":
            swapped.append("hers")
        elif tags[n] == "PRP$" and word == "her":
            if words[n+1] in [".", ",", ":", ";", "?", "!", "(", ")"]:
                swapped.append('him')
            else:
                swapped.append('his')
        elif tags[words.index(word)] != "PRP" and word == "hers":
            swapped.append('his')
        elif word in g_pronouns[::2]:
            swapped.append(g_pronouns[g_pronouns.index(word)+1])
        elif word in g_pronouns[1::2]:
            swapped.append(g_pronouns[g_pronouns.index(word)-1])
        else:
            swapped.append(word)

        if word in g_pronouns[::2] or word in gendered_words[::2]:
            gender = "The female"
        elif word in g_pronouns[1::2] or word in gendered_words[1::2]:
            gender = "The male"
    return swapped, gender


def clean_up(text):
    """capitalizing and joining of words into sentences without
    whitespaces before punctuation"""

    capitalized = []
    for num, element in enumerate(text):
        if num == 0:
            element = element.title()
            capitalized.append(element)
        else:
            capitalized.append(element)

    cleaned = ' '.join(capitalized)
    cleaned = re.sub(r' (?=\W)', '', cleaned)
    cleaned = re.sub(r"'\s", "'", cleaned)
    return cleaned


def adjust_verbs(sentence, conjugator, lemmatizer):
    """adjusts verbs in sentences to their respective plural form"""

    tagged = pos_tag(word_tokenize(sentence))
    adjusted = []
    for t in tagged:
        if t[1] == 'VBZ':
            lem = lemmatizer.lemmatize(t[0], pos="v")
            if lem == 'go':
                conj = (conjugator.conjugate(lem).conjug_info['indicative']
                        ['indicative present']['3p'])
                adjusted.append((conj[2:], 'ph'))
            else:
                conj = (conjugator.conjugate(lem).conjug_info['indicative']
                        ['indicative present']['3p'])
                adjusted.append((conj, 'ph'))
        elif t[1] == 'VBD':
            lem = lemmatizer.lemmatize(t[0], pos="v")
            if lem == 'go':
                conj = (conjugator.conjugate(lem).conjug_info['indicative']
                        ['indicative past tense']['3p'])
                adjusted.append((conj[2:], 'ph'))
            else:
                conj = (conjugator.conjugate(lem).conjug_info['indicative']
                        ['indicative past tense']['3p'])
                adjusted.append((conj, 'ph'))
        else:
            adjusted.append(t)
    return adjusted


def swap_they(adjusted_words, model_spacy):
    """Swaps pronouns to plural form"""

    words = [i[0] for i in adjusted_words]
    words = [w.lower() for w in words]
    tags = [i[1] for i in adjusted_words]

    swapped = []
    for n, word in enumerate(words):
        # establish first subject of sentence
        sent_m = model_spacy(" ".join(words))
        first_subject = [t for t in sent_m if t.dep_ == "nsubj"]
        if (first_subject[0].text in g_pronouns[1::2] and
               word in g_pronouns[::2]):
            swapped.append(word)
        elif (first_subject[0].text in g_pronouns[::2] and
               word in g_pronouns[1::2]):
            swapped.append(word)
        elif tags[n] == 'PRP$':
            swapped.append("their")
        elif word in ("he", "she"):
            swapped.append("they")
        elif word in("him", "her"):
            swapped.append("them")
        elif word in ("himself", "herself"):
            swapped.append("themselves")
        else:
            swapped.append(word)
    return swapped

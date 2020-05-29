from nltk.corpus import wordnet as wn


def get_synonyms(word):
    """Getting a list of synonyms from a seed-word"""
    
    synonyms = []
    for syn in wn.synsets(word):
        for lm in syn.lemmas():
            lemma = lm.name()
            if lemma not in synonyms:
                synonyms.append(lemma)
    return synonyms

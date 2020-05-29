"""Getting bias-scores from input text and the assigned colour-codes"""

import numpy as np
import gensim
from sklearn.decomposition import PCA
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer

model_w2v = (
    gensim.models.KeyedVectors.load_word2vec_format
    ('data/GoogleNews-vectors-negative300.bin',
     binary=True))
lemmatizer = WordNetLemmatizer()

gender_pairs = [['woman', 'man'], ['girl', 'boy'], ['she', 'he'],
                ['mother', 'father'], ['daughter', 'son'], ['gal', 'guy'],
                ['female', 'male'], ['her', 'his'], ['herself', 'himself'],
                ['Mary', 'John']]

matrix = []
for a, b in gender_pairs:
    center = (model_w2v[a] + model_w2v[b])/2
    matrix.append(model_w2v[a] - center)
    matrix.append(model_w2v[b] - center)
matrix = np.array(matrix)
pca = PCA(n_components=10)
fitted = pca.fit(matrix)
g = fitted.components_[0]
center_wm = (model_w2v["woman"] + model_w2v["man"])/2


def get_relevant(sentence_o):
    """Filter out adjectives, nouns and verbs for analysis"""

    tagged = pos_tag(word_tokenize(sentence_o))
    rel_words = []
    rel_tags = ["FW", "JJ", "JJR", "JJS", "NN", "NNP",
                "NNPS", "NNS", "RBR", "RBS"]
    for i in tagged:
        if i[1] in rel_tags:
            rel_words.append(i[0])
    return rel_words


def get_bias(word_list, gv=g, center=center):
    """Get the gender a word is associated with and the intensity of the bias
        from the input list of words."""

    gender = []
    intensity = []
    words = []
    for word in word_list:
        try:
            v = np.dot((model_w2v[word]-center_wm), gv)
            if v < -0.13:  # threshold: 50% ov values lie between -0.11 and 0.15.
                gender.append("f")
                words.append(word)
            elif v > 0.13:
                gender.append('m')
                words.append(word)
            if abs(v) > 1:
                intensity.append(5)
            elif abs(v) > 0.7:
                intensity.append(4)
            elif abs(v) > 0.5:
                intensity.append(3)
            elif abs(v) > 0.3:
                intensity.append(2)
            elif abs(v) > 0.10:
                intensity.append(1)
        except KeyError:
            pass
    return words, gender, intensity


def get_colours(orig_sentence, words, gender, intensity):
    """get colours assigned to bias-intensity-levels:
        shades of red for male, shades of blue for female."""

    sen = []
    colours = []
    if not isinstance(orig_sentence, list):
        orig_sentence = orig_sentence.split()
    for i in orig_sentence:
        if i not in words:
            sen.append(i)
            colours.append("#030303")
        elif i in words:
            sen.append(i)
            index = words.index(i)
            wordgender = gender[index]
            if wordgender == "m":
                if intensity[index] == 1:
                    colours.append("#bf6d72")
                elif intensity[index] == 2:
                    colours.append("#e79096")
                elif intensity[index] == 3:
                    colours.append("#eaa6ab")
                elif intensity[index] == 4:
                    colours.append("#f4bcc0")
                elif intensity[index] == 5:
                    colours.append("#f4bcc0")
            else:
                if intensity[index] == 1:
                    colours.append("#076296")
                elif intensity[index] == 2:
                    colours.append("#3971A4")
                elif intensity[index] == 3:
                    colours.append("#6094C9")
                elif intensity[index] == 4:
                    colours.append("#86B7EF")
                elif intensity[index] == 5:
                    colours.append("#ACDDFF")

    return sen, colours


def lengthen(sentence_list, colour_list):
    to_pad = 20 - len(sentence_list)
    for _ in range(to_pad):
        sentence_list.append(" ")
        colour_list.append(" ")
    return sentence_list, colour_list


def colours_bias(o_sentence):
    rel_words = get_relevant(o_sentence)
    w, gen, intense = get_bias(rel_words)
    s, c = get_colours(o_sentence, w, gen, intense)
    sen, colors = lengthen(s, c)
    return sen, colors

"""Preparing the data to be plotted with bokeh"""

import pickle
import numpy as np
from scipy import spatial
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA


with open('glove_dict.p', "rb") as file_imp:
    embeddings_dict = pickle.load(file_imp)


def get_gender_vector():
    """calculate a general gender-vector"""
    gender_pairs = [['woman', 'man'], ['girl', 'boy'], ['she', 'he'],
                    ['mother', 'father'], ['daughter', 'son'], ['gal', 'guy'],
                    ['female', 'male'], ['her', 'his'], ['herself', 'himself']]
    matrix = []
    for a, b in gender_pairs:
        center = (embeddings_dict[a] + embeddings_dict[b])/2
        matrix.append(embeddings_dict[a] - center)
        matrix.append(embeddings_dict[b] - center)
    matrix = np.array(matrix)
    pca = PCA(n_components=10)
    fitted = pca.fit(matrix)
    g_vector = fitted.components_[0]
    return g_vector


gv = get_gender_vector()


def find_closest(embedding):
    """find similar vectors"""
    return sorted(embeddings_dict.keys(),
                  key=lambda ev_word:
                  spatial.distance.euclidean(embeddings_dict[ev_word],
                                             embedding))[:50]


def get_list_closest(word):
    """"get list with closest vectors to a word and respective labels"""
    embeddings = []
    labels = []
    if isinstance(word, str):
        closest = find_closest(embeddings_dict[word.lower()])
        for similar_word in closest:
            labels.append(similar_word)
            embeddings.append(embeddings_dict[word.lower()])
    else:
        closest = find_closest(word)
        for similar_word in closest:
            labels.append(similar_word)
            embeddings.append(word)
    return embeddings, labels


def go_direction(word, direction, gender_vector=gv):
    """shift key-vector via gender direction"""

    key_vector = embeddings_dict[word.lower()]
    if direction == "male":
        new = key_vector - (gender_vector*3)
    elif direction == "female":
        new = key_vector + (gender_vector*3)
    return new


def two_dimensional(vectors):
    """break vectors down into two dimensionality"""
    tsne = TSNE(perplexity=30, n_components=2)
    transformed = tsne.fit_transform(vectors)
    x = transformed[:, 0]
    y = transformed[:, 1]
    return x, y


def do_it_all(word):
    closest, labels = get_list_closest(word)
    x, y = two_dimensional(closest)
    return x, y, labels


def cloud_comparison(labels_x, labels_y):
    """Create lists that include all words unique to each
    of the two clouds"""

    only_x = []
    only_y = []
    for label in labels_x:
        if label not in labels_y:
            only_x.append(label)
    for label in labels_y:
        if label not in labels_x:
            only_y.append(label)
    return ", ".join(only_x), ", ".join(only_y)

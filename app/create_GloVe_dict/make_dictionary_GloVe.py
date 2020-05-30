"""Creating a dictionary from the GloVe-data with words as keys
    and vectors as values"""

import pickle
import numpy as np

embeddings_dict = {}
with open("data/glove.6B.50d.txt", 'r', encoding="utf-8") as file_imp:
    for line in file_imp:
        values = line.split()
        word = values[0]
        vector = np.asarray(values[1:], "float32")
        embeddings_dict[word] = vector

with open('data/glove_dict.p', 'wb') as file_imp2:
    pickle.dump(embeddings_dict, file_imp2)

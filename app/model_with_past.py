"""function to finish sentences with GPT2-Model and function
    to capitalize appropriate words in output-sentence"""

import torch
import numpy as np


def next_word(seed_words, tokenizer, model, number_of_words=40):
    """loop to predict the following word and append it to the original
    sentence.
    Sentence is ended after given number if words or if last token is
    a period, question mark or exclamation mark.
    The next word is chosen from the top ten predictions under their
    probability-distribution."""

    sentence = seed_words
    end_of_sentence = [13, 30, 5145, 764, 526]

    indexed_tokens = tokenizer.encode(" ".join(sentence))
    past = None
    tokens_tensor = torch.tensor([indexed_tokens])
    one_token = tokens_tensor

    for _ in range(number_of_words):
        with torch.no_grad():  # no autograd engine (more speed, no backprop)
            outputs, past = model(one_token, past=past)
            predictions = outputs

        predictions_np = predictions[0, -1, :].numpy()
        top10 = np.argpartition(predictions_np, -10)[-10:]
        probas = predictions_np[(top10)]
        probas = probas - probas.max()
        exponentials = np.exp(probas)
        softmaxed = exponentials/(sum(exponentials))
        predicted_index = (np.random.choice(top10, p=softmaxed))
        if predicted_index in end_of_sentence:
            indexed_tokens.append(predicted_index)
            sentence = tokenizer.decode(indexed_tokens)
            break
        else:
            indexed_tokens.append(predicted_index)
            one_token = torch.tensor([[predicted_index]])
        sentence = tokenizer.decode(indexed_tokens)
    return sentence


def capitalize_sentence(sentence):
    """Capitalize first word of the sentence."""

    sentence_list = sentence.split(" ")
    capitalized = []
    for num, element in enumerate(sentence_list):
        if num == 1:
            element = element.title()
            capitalized.append(element)
        else:
            capitalized.append(element)
    return " ".join(capitalized)

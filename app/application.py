"""create website with Flask"""

from flask import Flask, render_template, request
from nltk.stem import WordNetLemmatizer
import mlconjug
import spacy
from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel
from pronoun_functions import swap, clean_up, adjust_verbs, swap_they
from model_with_past import next_word, capitalize_sentence
from bokeh_plots import bokeh_magic
from prepare_cloud import do_it_all, go_direction, cloud_comparison
from thesaurus import get_synonyms

# load models
model_spacy = spacy.load('en_core_web_md')
conjugator = mlconjug.Conjugator(language='en')
lemmatizer = WordNetLemmatizer()
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')
model.eval()

from in_sentence import colours_bias, get_bias, get_colours, lengthen

app = Flask(__name__)

@app.route('/')
def start():
    return render_template('start.html')


@app.route('/sentence_start')
def sentence_vis_start():
    return render_template('sentence_start.html')


@app.route('/sentence')
def sentence_vis():
    user_input = dict(request.args)
    sentence = list(user_input.values())
    sen, colors = colours_bias(sentence[0])
    return render_template('sentence.html',
                           sen=sen,
                           colors=colors)


@app.route('/pronouns_start')
def pronouns_start():
    return render_template('pronouns_start.html')


@app.route('/pronouns')
def swap_pronouns():
    user_input = dict(request.args)
    sentence = list(user_input.values())
    # change to male/female
    swapped, _ = swap(sentence[0])
    ready = clean_up(swapped)
    # change to non-binary
    adjusted = adjust_verbs(sentence[0], conjugator, lemmatizer)
    swapped_they = swap_they(adjusted, model_spacy)
    ready_they = clean_up(swapped_they)
    return render_template('pronouns.html',
                           ready=ready,
                           ready_they=ready_they,
                           sentence=sentence)

@app.route("/thesaurus_start")
def thesaurus_start():
    return render_template("thesaurus_start.html")


@app.route('/thesaurus')
def thesaurus():
    o_word = dict(request.args)
    orig_word = list(o_word.values())[0]
    synonyms = get_synonyms(orig_word)
    words, gender, intensity = get_bias(synonyms)
    th_words, cols = get_colours(" ".join(synonyms), words, gender, intensity)
    th_words, cols = lengthen(th_words, cols)
    return render_template('thesaurus.html',
                           orig_word=orig_word,
                           th_words=th_words,
                           cols=cols)

@app.route("/next_start")
def next_start():
    return render_template("next_start.html")


@app.route('/next')
def finish_sentence():
    user_input_n = dict(request.args)
    sentence_n = list(user_input_n.values())
    to_cap = next_word(sentence_n, tokenizer, model)
    ready_n = capitalize_sentence(to_cap)
    swapped_next, gender = swap(sentence_n[0])
    to_cap2 = next_word(swapped_next, tokenizer, model)
    ready_n2 = capitalize_sentence(to_cap2)

    return render_template('next.html',
                           ready_n=ready_n,
                           ready_n2=ready_n2,
                           gender=gender)


@app.route("/cloud_start")
def cloud_start():
    return render_template("cloud_start.html")


@app.route("/cloud")
def clouds():
    user_input_c = dict(request.args)
    word = list(user_input_c.values())

    # original cloud
    x, y, labels = do_it_all(word[0])
    script, divtag = bokeh_magic(x, y, labels, "#fcd1af")

    # clouds with direction
    new1 = go_direction(word[0], "female")
    x_f, y_f, labels_f = do_it_all(new1)
    script_f, divtag_f = bokeh_magic(x_f, y_f, labels_f, "#71afd2")
    new2 = go_direction(word[0], "male")
    x_m, y_m, labels_m = do_it_all(new2)
    script_m, divtag_m = bokeh_magic(x_m, y_m, labels_m, "#f38188")
    only_f, only_m = cloud_comparison(labels_f, labels_m)

    return render_template("cloud.html",
                           word=word,
                           script=script,
                           divtag=divtag,
                           script_f=script_f,
                           divtag_f=divtag_f,
                           script_m=script_m,
                           divtag_m=divtag_m,
                           only_f=only_f,
                           only_m=only_m)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

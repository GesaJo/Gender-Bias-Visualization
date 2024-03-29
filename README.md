<img style="float:right;" src="app/static/images/logo.png">

## Project to visualize gender-bias in language models  

(Currently not deployed)

As has been known for some time, many machine learning models reproduce, and
sometimes amplify, human biases regarding race, gender, age etc.
However, it is usually not the model in its design that is biased. The problem is
the data we train it on: the language we use everyday, representing our
prejudices.
This is important because language models  are given more and more agency for example in search rankings,
translations, hiring decisions etc. and their replicating the biases
can lead to and intensify inequalities in many different real-world areas.

This project offers tools to visualize the gender bias in pre-trained language
models to better understand the prejudices in the data. However, the results
still need to be interpreted: do they represent a statistical reality
(e.g. there are more female hairdressers than male ones) and/or a prejudice?
 Is the gender-dimension inherent to the word (e.g. mustache, pregnancy)?
These tools should only be a first step into the exploration of gender biases
and their roots.
Also, it needs to be said that this bias-concept is based on a binary idea of
gender, which does not represent reality. Due to the fact that the training
data shows nearly no indication of other gender identities, and so this
dimension can’t be properly studied in this case, the tools presented here
also concentrate on “male” and “female”.

## Five ways to visualize gender-bias:
  <li>Sentence: returns a given sentence showing bias on the word-level
    through colorization</li>
  <li>Thesaurus: presents (colorized) synonyms of a given word to
    demonstrate bias on a concept-level</li>
  <li>Pronouns: swaps pronouns to illustrate stereotypes on a higher
    level (sentences, paragraphs)</li>
  <li>Word Prediction: finishes a sentence in a "male" and a "female" version</li>
  <li>Wordcloud: shows closest words to a given seedwords if shifted in male or female direction</li>

All of these Tools are explained in more detail on their respective sites.

Models and tech used (among others):
Word2Vec, GloVe, WordNet, GPT2, python, spacy, scipy, pytorch, bokeh, sklearn, HTML, CSS, jinja, hosted on GCP.


<img src="overview.gif" width="1000"/>


## Background: Gender-vector
Words are represented by high-dimensional vectors (word embeddings) that
capture their meaning and usage. The basic assumptions underlying the analysis
with word embeddings are firstly, that the closer together the embeddings are, the
 more similar their semantic meaning is.  Secondly, that the relationships
 between them is captured by their mathematical differences.
To visualize the biases, a “gender-direction” can be constructed with help of
inherently gendered word-pairs like "man" - "woman", "he" - "she", "son" -
"daughter" and their differences in vectorspace.
This gender-vector is then used to calculate a score (the dotproduct of a given
word and the gender-vector) to indicate if there is a bias and how strong it is.


This project has been developed as final project @Spiced Bootcamp.

## To use locally with docker:
- clone this repo
- get data and store in directory app/data:
  - download GoogleNews-vectors-negative300.bin.gz from [here](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing) and gunzip.
  - download glove.6B.zip [here](http://nlp.stanford.edu/data/glove.6B.zip) and unzip.
-  cd into folder app and run:  
`docker run --rm -d -p 5000:5000 -v "$PWD/data:/app/data" --name gb-container gesajo/genderbias`
- run:
`docker logs -f gb-container`
- wait a little while....
- open the specified address (should be: localhost:5000) in your browser and the website should appear (although the initial load could also take some time...)

## To use locally without docker:
- clone this repo
- get data and store in directory app/data:
  - download GoogleNews-vectors-negative300.bin.gz from [here](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing) and gunzip.
  - download glove.6B.zip [here](http://nlp.stanford.edu/data/glove.6B.zip) and unzip.
- pip install requirements.txt
- download spacy model with `python -m spacy download en_core_web_md`
- download WordNet with `python -m nltk.downloader punkt averaged_perceptron_tagger wordnet`
- cd into app-folder and run `python application.py`
- wait a little while....
- open the specified address (should be: localhost:5000) in your browser and the website should appear (although the initial load could also take some time...)

## To Do:
-  ~~add more documentation~~
- ~~dockerize~~
- ~~host on GCP~~ 
- tests
- new feature: bias in whole dataset and most biased words


## Sources and further reading:

* Bolukbasi, T./ Chang, K.-W. / Zou, J./ Saligrama, V./ Kalai, A.: Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings (2016).  
* Bordia, S./ Bowman, S.R.: Identifying and Reducing Gender Bias in Word-Level Language Models (2019).
* Caliskan-Islam, A./ Bryon, J.J./ Narayanan, A.: Semantics derived automatically from language corpora necessarily contain human biases (2017).
* Chang, S./ McKeown, K.: Automatically Inferring Gender Associations from Language (2019).
* Garg, N./ Schiebinger, L. / Jurafsky, D. / Zou, James: Word embeddings quantify 100 years of gender and ethnic stereotypes  (2018).   
* Gonen, H./  Goldberg, Y.: Lipstick on a Pig: Debiasing Methods Cover up Systematic Gender Biases in Word Embeddings But do not Remove Them (2019).   
* Hoyle, A./ Wolf-Sonkin, L./ Wallach, H. / Augenstein, I. / Cotterell, R.: Unsupervised Discovery of Gendered Language through Latent-Variable Modeling (2019).  
* Zhao, J./ Zhou, Y./ Li, Z. / Wang, W./ Chang, K.W.: Learning Gender-neutral Word Embeddings (2018).


MIT License

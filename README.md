# text-augmentation

This repository helps you augmenting text data for nlp projects. The main purpose of the repository is to use it for augmenting your train/test data by applying label-invariant transformations on them.


## Demo

* [Demo Notebook](demo_notebook.ipynb)

## Augmentation Functions


|Funtion|Description| Example |
|:---:|:----:|:-------:|
|Synonym Replacement|We change the adjectives and nouns on a text by a synonim using wordnet | *I am smart my friend* -> *I am intelligent my protagonist*|
|Antonym Replacement|We change the adjectives and nouns on a text by a negation + antonym using wordnet |*I am smart my friend -> I am not stupid my not foe* |
|Add Stopwords|We add stopwords to our text using [nlpaug](https://github.com/makcedward/nlpaug)|*I like you because I think you are really smart my friend* -> *now i quite like teasing you because again i think you are really smart my friend*|
|Add random characters|We add characters to our text using [nlpaug](https://github.com/makcedward/nlpaug) for simulating typos, mispelling etc..|*I like you because I think you are really smart my friend* -> *I like you because 1 think y0o ake rea11y smart my friend*|   
|Backtranslation| Translate our text and then backtranslate it using [GoogleTranslator from deep translator](https://deep-translator.readthedocs.io/en/latest/) | *I like you because I think you are really smart my friend* -> *I love you because you are very smart my friend*|
|NER Replacement| We replace an entity by another| *I want to go to Barcelona and visit the offices of Apple* -> *I want to go to Miami and visit the offices of Sun*|
|Plural transform|Nouns and adjectives in singular are converted to plural|*I like you because I think you are really smart my friend* -> *I like you because I think you are really smarts my friends*|
|Singular transform|Nouns and adjectives in plural are converted to singular|*Tomorrow bring me my pencils* -> *Tomorrow bring me my pencil* |


## Executing all the augmentation functions
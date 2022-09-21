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

For running the augmentations on your data, first clone the project: 

````
git clone https://github.com/bonells96/text-augmentation.git
````

Then store you data in the data folder as a **.json** file. Your data should be a dictionnary where **text samples** are the **keys** and the **label** of each text are the **values**.

Example: Below you will see an example of data dictionnary. The labels in these case are 1 or 0. 1 means that the text is a request and 0 means that it is not a request.

```
{"Please join me":1, "You must do your homework":1, "You should follow her":0, "You have to study more":1,
                "What is your name?":0, "Are you happy with your new job?":0, "I request you to give me your phone":1, 
                "he is always requesting":0, "I like this hotel":0, "Give me my glasses":1, "I am 13 years old":0}
```

Once your data is stored in the data folder, enter in the repo folder and execute the code with the command:

````
python run_augmentation.py
````

It will give you this output:

```
INFO:root:Loading data...
INFO:root:Augmenting data...
INFO:root:Your original data had 11 samples and your new data has 54 samples. The process lasted 16.7396080493927 seconds
INFO:root:Saving datafile: data_augmented.json in /Users/alejandrobonell/text-augmentation/output directory
```
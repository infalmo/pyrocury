from readability import Readability
from readability.text.syllables import count as syllableCount
from readability.exceptions import ReadabilityException
from pysyllables import get_syllable_count
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re

def relativeDCReadability(text: str, totalReadability: float) -> float:
    """
    A function that returns a Dale-Chall readability score of a excerpt relative to the overall readability of the text.
    text: the passage to be evaluated. Has to be more than 100 words, or an exception will be thrown
    totalReadability: the overall readability score of the whole text
    """
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    r = Readability(text)

    try:
        textDC = r.dale_chall()
    except ReadabilityException:
        #if excerpt is too short, duplicate excerpt to required length.
        textExtensionFactor = int(100 / len(text.split(" "))) + 1
        return relativeDCReadability(text * textExtensionFactor, totalReadability)
    return textDC.score/totalReadability

def lexicalDiversity(text:str)->float:
    """
    Returns the fraction of words in a given text that are not stopwords.
    """
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    textWords = word_tokenize(text)
    stopWords = set(stopwords.words('english'))
    punctSet = set(string.punctuation)
    textWords = [w for w in textWords if not w.lower() in punctSet]
    textLength = len(textWords)
    textWords = [w for w in textWords if not w.lower() in stopWords]
    return len(textWords)/textLength

def posFractions(text:str)->dict:
    """
    Given a string, returns the share of various parts of speech.
    """
    try:
        nltk.data.find('taggers\\averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')


    tokens = word_tokenize(text)
    punctSet = set(string.punctuation)
    #strip punctuation
    tokens = [w for w in tokens if not w in punctSet]
    totalWords = len(tokens)
    tagged_words = nltk.pos_tag(tokens)
    tokenCounter = dict()
    for token in tagged_words:
        if token[1] in tokenCounter.keys():
            tokenCounter[token[1]] += 1
        else:
            tokenCounter[token[1]] = 1
    for pos in tokenCounter.keys():
        tokenCounter[pos] = round(tokenCounter[pos]/totalWords, 3)
    return tokenCounter

def syllablesPerSecond(text:str, time: float)->float:
    """
    Given a string and the time it takes to speak said string (in seconds), 
    return the speaking rate in terms of syllables per second.
    text: the text to be parsed.
    time: the time in seconds it took to speak
    """
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    tokens = word_tokenize(text)
    punctSet = set(string.punctuation)
    #strip punctuation
    tokens = [w for w in tokens if not w in punctSet]
    totalSyllables = 0
    for word in tokens:
        if get_syllable_count(word) != None:
            totalSyllables += get_syllable_count(word)
        else:
            totalSyllables += syllableCount(word)
    return round(totalSyllables/time, 3)
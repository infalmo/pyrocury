from readability import Readability
from readability.exceptions import ReadabilityException
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
"""
TODO: 
readability test (Dale-Chall)
topic frequency w/ symbl.ai
"""

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
    print(textDC.score)
    return textDC.score/totalReadability

def lexicalDiversity(text)->float:
    """
    Returns the fraction of words in a given text that are not stopwords.
    """
    try:
        nltk.data.find('tokenizers/stopwords')
    except LookupError:
        nltk.download('stopwords')
    textWords = word_tokenize(text)
    stopWords = set(stopwords.words('english'))
    punctSet = set(string.punctuation)
    textWords = [w for w in textWords if not w.lower() in punctSet]
    textLength = len(textWords)
    textWords = [w for w in textWords if not w.lower() in stopWords]
    return len(textWords)/textLength

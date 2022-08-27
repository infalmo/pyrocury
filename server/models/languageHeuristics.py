from readability import Readability
from readability.exceptions import ReadabilityException
from contextlib import suppress
import nltk
"""
TODO: 
readability test (Dale-Chall)
topic frequency w/ symbl.ai
"""

def relativeReadability(text: str, totalReadability: float) -> float:
    """
    A function that returns a Dale-Chall readability score of a excerpt relative to the overall readability of the text.
    text: the passage to be evaluated
    totalReadability: the overall readability score of the whole text
    """
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    r = Readability(text)

    with suppress(ReadabilityException):
        textDC = r.dale_chall()
    print(textDC.score)
    return textDC.score/totalReadability


totalText = "First off, Glubb's characterization of the Arabian peninsula is very off. There were several notable kingdoms in the peninsula, namely the Himyarites in Yemen, the Lakhmids in Eastern Arabia, and the Quraysh in Mecca, with their own government and militaries, contrary to Glubb's assertion. In particular, the Quraysh established institutions to collect taxes from the merchant trade, maintain the Kaaba, and provide food and water to pilgrims [5]." +"Prior to Muhammad, Mecca was already unifying and consolidating its power in the Arabian peninsula to become an economic powerhouse. Under the ilaf, which was a deal between Meccan traders and the surrounding tribes to exchanged protection for carrying tribal goods to foreign markets, Meccan trade was both able to greatly extend its reach and develop their tribal allies, leading to their rapid growth in the 6th century [6]. When combined with their advantageous position that could control trade across the Red Sea and the Arabian peninsula, Mecca was in a prime position to grow." +"Indeed, both the Byzantines and the Sassanids noticed the rise of Mecca and the Arabian peninsula in general, and they made moves to exert their influence over the region. On the part of the Byzantines, Aksum, traditionally an ally of Byzantium, launched an expedition in 570, and Uthman ibn al-Huwayrith attempted to have himself installed as king of Mecca with the support of the Byzantines towards the end of the 6th century. The Sassanids exerted their own influence on the Arabian peninsula as well with their annexation of Aden around the time of the Aksumite expedition [7]." +"While it is true that the rapid expansion of the Rashidun Caliphate can partly be attributed to the weakness of the Byzantine and the Sassanid Empires after centuries of conflict, Mecca was quickly becoming a regional power by the time Muhammad came, and increased foreign influence in the region indicates that the Arabian Peninsula was hardly considered a backwater."


#nltk.download('punkt')
overallScore = Readability(totalText).dale_chall().score
print(overallScore)
excerpt = "There were several notable kingdoms in the peninsula, namely the Himyarites in Yemen, the Lakhmids in Eastern Arabia, and the Quraysh in Mecca, with their own government and militaries, contrary to Glubb's assertion"
print(relativeReadability(excerpt, overallScore))
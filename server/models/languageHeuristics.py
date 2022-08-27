from readability import Readability

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
    r = Readability(text)
    return r.dale_chall().score/totalReadability

from utils import correlation_tester


def implications(text: str) -> float:
    """
    Returns the implication weightage of the text.

    POOR CORRELATION
    """

    implicators = {
        "implies": ["implies", "imply"],
        "compound": ["and", "but", "since", "so"],
        "thus": ["thus", "therefore"],
        "steps": ["first", "next", "then", "last", "final"],
        "question": ["why", "which", "where", "how", "when"],
    }
    weights = {
        "implies": 0.0,
        "compound": 1.0,
        "thus": 10.0,
        "steps": 0.0,
        "question": 0.0,
    }

    text = text.lower()

    data = {}
    for (im, arr) in implicators.items():
        data[im] = sum(text.count(x) for x in arr)

    return sum(data[im] * weights[im] for im in implicators)


correlation_tester(implications)

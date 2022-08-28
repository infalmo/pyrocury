import textacy
from textacy.extract import keyterms
from textacy import text_stats


def add_topics(text: str):
    """Parses and adds topics to the video data"""
    try:
        # TODO: The secret is that this always panics, so it's never used.
        # topics = symbl_get_topics(txt, data["video_id"])
        raise RuntimeError()

    except:
        doc = textacy.make_spacy_doc(text, lang="en_core_web_sm")
        topics = keyterms.yake(doc, normalize="lemma", topn=20)
    return topics



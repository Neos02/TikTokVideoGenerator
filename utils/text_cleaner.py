from better_profanity import profanity
from html.parser import HTMLParser


profanity.load_censor_words()


class _HTMLReader(HTMLParser):

    def __init__(self):
        super().__init__()
        self.text = ''

    def handle_data(self, data: str):
        self.text += data


def html_to_text(html: str, preserve_linebreaks=False) -> str:
    """
    Converts an HTML string to plain text
    :param html: html to convert
    :param preserve_linebreaks: whether to preserve or remove linebreaks, defaults to False
    :return: a plain text string
    """

    html_filter = _HTMLReader()
    html_filter.feed(html)

    return html_filter.text.strip() if preserve_linebreaks else html_filter.text.replace('\n', '').strip()


def censor(text: str) -> str:
    """
    Censor profanity out of a string
    :param text: text to censor
    :return: the clean text
    """

    original = text.split(' ')
    censored = profanity.censor(text).split(' ')

    for i in range(len(censored)):
        word = censored[i]

        if len(word) != 0 and word.casefold().startswith('*'):
            censored[i] = word.replace('*', original[i][0], 1)

    return ' '.join(censored)

import re

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


def sanitize_text(text: str) -> str:
    """
    Remove special characters from text and prepare it for TTS
    :param text: text to sanitize
    :return: the modified text
    """

    # Remove special characters
    text = re.sub(r'[(){}[\]*]', '', text)

    # Reformat age and gender
    matches = re.finditer(r'\d+[FfMm]\s', text)
    chars = list(text)
    for match in matches:
        chars[match.end() - 2] = chars[match.end() - 2].upper()

    return ''.join(chars)


def remove_tldr(text: str) -> str:
    """
    Remove the TL;DR section of a post if it exists
    :param text: text to remove TL;DR from
    :return: the modified text
    """

    tl_index = text.casefold().index('tl')
    dr_index = text.casefold().index('dr')

    if 0 < dr_index - tl_index <= 3:
        return text[:tl_index]

    return text

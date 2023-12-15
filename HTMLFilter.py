from html.parser import HTMLParser


class HTMLFilter(HTMLParser):

    def __init__(self):
        super().__init__()
        self.text = ''

    def handle_data(self, data):
        self.text += data


def html_to_text(html):
    html_filter = HTMLFilter()
    html_filter.feed(html)

    return html_filter.text.strip()

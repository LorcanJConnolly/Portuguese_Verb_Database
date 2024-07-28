# Interacts with https://conjugator.reverso.net/conjugation-portuguese.html
# I: A verb or container of verbs.
# O: The verb conjugations.

from bs4 import BeautifulSoup
import requests

class scraper:

    def __init__(self, url) -> None:
        self.url = url
        self.headers = headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
            'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
            'Accept':'text/html,application/xhtml+xml,application/xml;'
            'q=0.9,image/webp,*/*;q=0.8'
            }
        self.verb = None

    def get_html(self):
        """
        """
        try:
            response = requests.get(self.url, headers=self.headers)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(response.content, "html.parser")
    
    def extract_text_from_tags(self, bs):
        """
        """
        # FIXME: Traverse tag trees to ensure order of insetion into text.
        if not bs:
            raise ValueError(f"Error obtaining response from {self.url}.")
        
        # ----- Reverso HTML Exactraction -----
        # Add the root verb layer to the dictionary and its key.
        text = {}
        whie_text = {}
        tense = None
        pronoun = None
        word_constructor = None
        for element in bs.descendants:
            """ HTML tags can get accessed like a dictionary. """ 
            if element.name:   # All HTML tags have name attributes.
                if "blue-box-wrap" in element.get('class', []) and element.get('mobile-tile', []) is not None:
                    tense = element["mobile-title"]
                    text[tense] = []
                if 'graytxt' in element.get('class', []):
                    pronoun = element.get_text()
                if 'auxgraytxt' in element.get('class', []):
                    pronoun += " " + element.get_text()
                if 'verbtxt' in element.get('class', []):
                    word_constructor = element.get_text()
                """ Attempt to insert text. """
                if 'verbtxt-term' in element.get('class', []):
                    word_constructor += element.get_text()
                    try:
                        text[tense].append((pronoun, word_constructor, False))
                    except KeyError:
                        return f"KeyError: TENSE WAS NOT FOUND, UNABLE TO INSERT WORD INTO DATABASE. \nDEBUG INFO: \nPronoun attempted to be inserted: {pronoun} \nWord attempted to be inserted: {word_constructor}"
                    word_constructor, pronoun = None, None
                if 'verbtxt-term-irr' in element.get('class', []):
                    word_constructor += element.get_text()
                    try:
                        text[tense].append((pronoun, word_constructor, True))
                    except KeyError:
                        return f"KeyError: TENSE WAS NOT FOUND, UNABLE TO INSERT WORD INTO DATABASE. \nDEBUG INFO: \nPronoun attempted to be inserted: {pronoun} \nWord attempted to be inserted: {word_constructor}"
                    word_constructor, pronoun = None, None
        return text
    
    def parse(self):
        bs = self.get_html()
        return self.extract_text_from_tags(bs)
        


# x = scraper("https://conjugator.reverso.net/conjugation-portuguese-verb-poder.html")



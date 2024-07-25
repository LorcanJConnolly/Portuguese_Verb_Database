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

    def get_html(self):
        """
        """
        try:
            response = requests.get(self.url, headers=self.headers)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(response.content, "html.parser")
    
    def extract_text_from_html_tags(self):
        """
        """
        bs = self.get_html()
        if not bs:
            return f"Error obtaining response from {self.url}."

        # verbtxt_tags = bs.find_all('i', class_='verbtxt')
        # verbtxt_term_irr_tags = bs.find_all('i', class_='verbtxt-term')
        # verbtxt_term_irr_tags + bs.find_all('i', class_='verbtxt-term-irr')
        # ----- Reverso HTML Exactraction -----
        text = {}
        tense = None
        word_constructor = None
        for element in bs.descendants:
            if element.name:   # All HTML tags have name attributes.
                if element.get('mobile-title', []):
                    tense = element['mobile-title']
                    text[tense] = {}
                if 'verbtxt' in element.get('class', []):
                    word_constructor = element.get_text()
                if 'verbtxt-term' in element.get('class', []):
                    word_constructor += element.get_text()
                    text[tense][word_constructor] = False
                    word_constructor = None
                if 'verbtxt-term-irr' in element.get('class', []):
                    word_constructor += element.get_text()
                    text[tense][word_constructor] = True
                    word_constructor = None
                
        for tense, words in text.items():
            print(f"Tense: {tense}")
            for word, value in words.items():
                print(f"  Word: {word} : {value}")
            print()  # Print a newline for better readability


    def store_conjugations(self):
        pass            
    

x = scraper("https://conjugator.reverso.net/conjugation-portuguese-verb-poder.html")
print(x.extract_text_from_html_tags())


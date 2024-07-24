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
        try:
            response = requests.get(self.url, headers=self.headers)
        except requests.exceptions.RequestException:
            print(f"Error obtaining response from {self.url}.")
            return None
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    
    def parser(self):
        pass

    def get_conjugations(self):
        pass            
    

x = scraper("https://conjugator.reverso.net/conjugation-portuguese.html")
print(x.get_html())


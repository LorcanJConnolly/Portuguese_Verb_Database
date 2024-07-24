# Interacts with https://conjugator.reverso.net/conjugation-portuguese.html
# I: A verb or container of verbs.
# O: The verb conjugations.

from bs4 import BeautifulSoup
import requests

class scraper:

    def __init__(self, url) -> None:
        self.url = url

    def get_html(self):
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException:
            print(f"Error obtaining response from {self.url}.")
            return None
        soup = BeautifulSoup(response.content, "html.parser")
        return soup is not None
    

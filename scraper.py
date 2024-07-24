# Interacts with https://conjugator.reverso.net/conjugation-portuguese.html
# I: A verb or container of verbs.
# O: The verb conjugations.

class scraper:

    def __init__(self, url) -> None:
        self.url = url

    def get_html(self):
        return self.url is not None
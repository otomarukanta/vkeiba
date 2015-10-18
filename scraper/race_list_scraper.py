from scraper.scraper import Scraper


class RaceListScraper(Scraper):

    def _parse(self):
        result = [tag.a["href"] for tag in self.soup.find_all(class_="wsLB")]
        return result

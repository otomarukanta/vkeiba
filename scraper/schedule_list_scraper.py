from scraper.scraper import Scraper


class ScheduleListScraper(Scraper):

    def _parse(self):
        table = [rows.find_all('td')
                 for rows in self.soup.find(class_="scheLs").find_all('tr')]
        result = [row[1].a['href'] for row in table
                  if row and row[1].a is not None]
        return result

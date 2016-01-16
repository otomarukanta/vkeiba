from scraper.scraper import Scraper
from datetime import datetime as dt


class TrainerScraper(Scraper):
    def _parse(self):
        res = dict()

        info = self.soup.find(id='dirTitName')
        res['kana'] = info.p.text.split('|')[0].strip()
        res['name'] = info.h1.text
        lis = info.find_all('li')
        res['birthday'] = dt.strptime(
            lis[0].text.split('：')[1], '%Y年%m月%d日').date().isoformat()
        res['affiliation'] = lis[1].text.split('：')[1].strip()
        res['license'] = lis[2].text.split('：')[1]

        return res

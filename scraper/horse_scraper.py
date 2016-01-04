from scraper.scraper import Scraper
from datetime import datetime as dt


class HorseScraper(Scraper):
    def _parse(self):
        res = dict()

        # base info
        info = self.soup.find(id='dirTitName')
        res['sex'] = info.p.text.split('|')[0].strip()
        res['name'] = info.h1.text
        lis = info.find_all('li')
        res['birthday'] = dt.strptime(
            lis[0].text.split('：')[1], '%Y年%m月%d日').date().isoformat()
        res['color'] = lis[1].text.split('：')[1]
        res['trainer_id'] = lis[2].a['href'].split('/')[3]
        res['owner'] = lis[3].text.split('：')[1]
        res['producer'] = lis[4].text.split('：')[1]
        res['birthplace'] = lis[5].text.split('：')[1]

        # blood
        pedigree = self.soup.find(id='dirUmaBlood').find_all('td')
        labels = ['sire', 'sire_sire', 'sire_sire_sire', 'sire_sire_mare',
                  'sire_mare', 'sire_mare_sire', 'sire_mare_mare', 'mare',
                  'mare_sire', 'mare_sire_sire', 'mare_sire_mare', 'mare_mare',
                  'mare_mare_sire', 'mare_mare_mare']
        for label, name in zip(labels, pedigree):
            res[label] = name.text

        return res

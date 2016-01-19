from scraper.scraper import Scraper
from datetime import date
import re


class RaceResultScraper(Scraper):
    def __init__(self):
        self.regex_race_id = re.compile("race\/result\/(\d+)")
        self.regex_path = re.compile("/\w+/\w+/(\d+)/")
        self.regex_sex_age = re.compile("(\w+)(\d+)")
        self.regex_weight = re.compile("(\d*)\(([+-]?\d*)\)")
        self.regex_day = re.compile(r"(\d*)年(\d*)月(\d*)日.*?(\d*)回"
                                    "(.*?)(\d)日.*?(\d*:\d*)発走")
        self.regex_title = re.compile(r"競馬 - (.+?) 結果 - スポーツナビ")
        self.regex_meta = re.compile(r"(.+?)・(.+?) (\d+?)m \[コースガイド\]"
                                     " \| 天気： \| 馬場： \| (.+?) \| (.+?)"
                                     " \| (.+?) \|")
        self.grades = ['新馬', '未勝利', '500万下',
                       '1000万下', '1600万下', 'オープン']
        super(RaceResultScraper, self).__init__()

    def _parse(self):
        res = dict()
        url = self.soup.find_all(
            'meta', attrs={'property': 'og:url'})[0]['content']
        if 'denma' in url:
            return
        race_id = self.regex_race_id.findall(url)[0]
        res['result'] = self._parse_result()
        for i in range(len(res['result'])):
            res['result'][i]['race_id'] = race_id

        if res['result'] is None:
            return None
        res['info'] = self.parse_info()
        res['info']['race_id'] = race_id
        links = self.parse_link()
        res['horse'] = links['horse']
        res['jockey'] = links['jockey']
        res['trainer'] = links['trainer']
        return res

    def _parse_result(self):
        table = self.soup.find(id='resultLs')
        if table is None:
            return None

        records = [trs.find_all('td') for trs in table.find_all('tr')]
        records = [self.trim_record(record, idx)
                   for idx, record in enumerate(records) if record]

        return records

    def trim_record(self, record, idx):
        res = dict()
        res['row_id'] = str(idx)
        res['final_position'] = record[0].text
        res['frame_number'] = record[1].text
        res['horse_number'] = record[2].text
        res['horse_id'] = self.regex_path.findall(record[3].a['href'])[0]
        res['sex'], res['age'] = self.regex_sex_age.findall(record[4].text)[0]
        res['jockey_id'] = self.regex_path.findall(record[5].a['href'])[0]
        res['time'] = record[6].text.replace('.', ':')
        res['margin'] = record[7].text
        res['passing_position'] = record[8].text
        res['last_3f'] = record[9].text
        res['jockey_weight'] = record[10].text
        weight = self.regex_weight.findall(record[11].text)[0][0]
        if weight:
            res['horse_weight'] = weight
        else:
            res['horse_weight'] = ''
        res['popularity'] = record[12].text
        res['ozz'] = record[13].text
        res['blinker'] = record[14].text

        return {k: v.strip() for k, v in res.items()}

    def parse_info(self):
        # race_info
        res = dict()
        schedule = self.regex_day.findall(
            self.soup.find(id='raceTitDay').text)[0]
        res['date'] = date(int(schedule[0]), int(schedule[1]),
                           int(schedule[2])).isoformat()
        res['times'] = schedule[3]
        res['place'] = schedule[4]
        res['days'] = schedule[5]
        res['start_time'] = schedule[6]
        res['race_name'] = self.regex_title.findall(self.soup.title.text)[0]

        weather = self.soup.find_all(class_='spBg')
        res['weather'] = weather[0]['alt']
        res['track_condition'] = weather[1]['alt']

        # meta
        meta = self.regex_meta.findall(
            self.soup.find(id='raceTitMeta').text)[0]
        res['track_type'] = meta[0]
        res['round'] = meta[1]
        res['distance'] = meta[2]
        res['race_condition'] = meta[3]

        # check grade
        # GIIIがGIで一致してしまうため、逆順で検索
        for grade in ['GIII', 'GII', 'GI']:
            if grade in self.soup.find(class_='fntB').text:
                res['grade'] = grade
                break
        else:
            for grade in self.grades:
                if grade in meta[4]:
                    res['grade'] = grade
                    break
            else:
                raise("Can't find grade")

        res['race_type'] = meta[4]
        res['money'] = meta[5]
        return res

    def parse_link(self):
        all_links = [a_tag.get('href')
                     for a_tag in self.soup.find(id="resultLs").find_all('a')]
        links = dict()
        links['horse'] = [link for link in all_links if 'horse' in link]
        links['jockey'] = [link for link in all_links if 'jocky' in link]
        links['trainer'] = [link for link in all_links if 'trainer' in link]

        return links

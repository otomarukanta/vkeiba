import re
from abc import ABCMeta, abstractmethod
from datetime import datetime as dt
from datetime import date
from datetime import time


class Parser(metaclass=ABCMeta):

    @abstractmethod
    def parse(self, soup):
        pass

class RaceResultParser(Parser):

    regex = dict()

    def __init__(self):
        self.regex['race_id'] = re.compile(r"race\/result\/(\d+)")
        self.regex['final_position'] = re.compile(r"(\w+)")
        self.regex['path'] = re.compile("/\w+/\w+/(\d+)/")
        self.regex['sex_age'] = re.compile("(\w+?)(\d+)")
        self.regex['jockey_weight'] = re.compile("\w*?(\d+\.\d+)")
        self.regex['weight'] = re.compile("(\d*)\((.*?)\)")
        self.regex['day'] = re.compile(r"(\d*)年(\d*)月(\d*)日.*?(\d*)回"
                        "(.*?)(\d*)日.*?(\d*:\d*)発走")
        self.regex['title'] = re.compile(r"競馬 - (.+?) 結果 - スポーツナビ")
        self.regex['meta'] = re.compile(r"(.+?)・(.+?) (\d+?)m \[コースガイド\]"
                            " \| 天気： \| 馬場： \| (.+?) \| (.+?)"
                            " \| (.+?) \|")
        self.grades = ['新馬', '未勝利', '未出走', '500万下', '900万下',
                '1000万下', '1600万下', 'オープン']

    def parse(self, soup):
        res = dict()
        url = self._get_url(soup)
        if any(x in url for x in ['denma', 'regist']):
            return
        race_id = self.regex['race_id'].findall(url)[0]
        res['result'] = self.parse_result(soup)
        for i in range(len(res['result'])):
            res['result'][i]['race_id'] = race_id

        if res['result'] is None:
            return None
        res['info'] = self.parse_info(soup)
        res['info']['race_id'] = race_id
        links = self.parse_link(soup)
        res['horse'] = links['horse']
        res['jockey'] = links['jockey']
        res['trainer'] = links['trainer']
        return res

    def parse_result(self, soup):
        table = soup.find(id='resultLs')
        if table is None:
            return None
        records = [trs.find_all('td') for trs in table.find_all('tr')]
        records = [self.trim_record(record, idx)
                   for idx, record in enumerate(records) if record]
        return records

    def _parse_fp(self, soup):
        pass

    def _parse_time(self, raw):
        if raw.count('.') == 1:
            t = dt.strptime(raw, '%S.%f').time()
        elif raw.count('.') == 2:
            t = dt.strptime(raw, '%M.%S.%f').time()
        else:
            t = None

        return t

    def trim_record(self, record, idx):
        res = dict()
        res['row_id'] = str(idx)
        res['final_position'] = self.regex['final_position'].findall(record[0].text)[0]
        res['frame_number'] = record[1].text
        res['horse_number'] = record[2].text
        res['horse_id'] = self.regex['path'].findall(record[3].a['href'])[0]
        res['sex'], res['age'] = self.regex['sex_age'].findall(record[4].text)[0]
        res['jockey_id'] = self.regex['path'].findall(record[5].a['href'])[0]
        res['jockey_weight'] = self.regex['jockey_weight'].findall(
            record[10].text)[0]
        if res['final_position'].strip() == '取消':
            return {k: v.strip() for k, v in res.items()}
        weight = self.regex['weight'].findall(record[11].text)[0][0]
        if weight:
            res['horse_weight'] = weight
        else:
            res['horse_weight'] = '-1'
        if res['final_position'].strip() == '除外':
            return {k: v.strip() for k, v in res.items()}
        weight = self.regex['weight'].findall(record[11].text)[0][0]
        res['odds'] = record[13].text
        res['blinker'] = record[14].text
        if res['final_position'].strip() == '中止':
            return {k: v.strip() for k, v in res.items()}

        res['time'] = self._parse_time(record[6].text)
        res['margin'] = record[7].text
        res['passing_position'] = record[8].text

        res['last_3f'] = self._parse_time(record[9].text)

        res['popularity'] = record[12].text

        return res
#         return {k: v.strip() for k, v in res.items()}

    def parse_info(self, soup):
        # race_info
        res = dict()
        schedule = self.regex['day'].findall(
            soup.find(id='raceTitDay').text)[0]
        res['race_date'] = date(int(schedule[0]), int(schedule[1]),
                                int(schedule[2])).isoformat()
        res['times'] = schedule[3]
        res['place'] = schedule[4]
        res['days'] = schedule[5]
        res['start_time'] = schedule[6]
        res['race_name'] = self.regex['title'].findall(soup.title.text)[0]

        weather = soup.find_all(class_='spBg')
        res['weather'] = weather[0]['alt']
        res['track_condition'] = weather[1]['alt']

        # meta
        meta = self.regex['meta'].findall(
            soup.find(id='raceTitMeta').text)[0]
        res['track_type'] = meta[0]
        res['rotation'] = meta[1]
        res['distance'] = meta[2]
        res['race_condition'] = meta[3]

        # check grade
        # GIIIがGIで一致してしまうため、逆順で検索
        for grade in ['GIII', 'GII', 'GI']:
            if grade in soup.find(class_='fntB').text:
                res['grade'] = grade
                break
        else:
            for grade in self.grades:
                if grade in meta[4]:
                    res['grade'] = grade
                    break
            else:
                print("Can't find grade. {}".format(res))
                raise

        res['race_type'] = meta[4]
        res['money'] = meta[5]
        return res

    def parse_link(self, soup):
        all_links = [a_tag.get('href')
                     for a_tag in soup.find(id="resultLs").find_all('a')]
        links = dict()
        links['horse'] = [link for link in all_links if 'horse' in link]
        links['jockey'] = [link for link in all_links if 'jocky' in link]
        links['trainer'] = [link for link in all_links if 'trainer' in link]

        return links

    def _get_url(self, soup):
        return soup.find_all('meta', attrs={'property': 'og:url'})[0]['content']

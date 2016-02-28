import re
from datetime import datetime as dt
from datetime import date

regex_race_id = re.compile("race\/result\/(\d+)")
regex_path = re.compile("/\w+/\w+/(\d+)/")
regex_sex_age = re.compile("(\w+?)(\d+)")
regex_jockey_weight = re.compile("\w*?(\d+\.\d+)")
regex_weight = re.compile("(\d*)\((.*?)\)")
regex_day = re.compile(r"(\d*)年(\d*)月(\d*)日.*?(\d*)回"
                       "(.*?)(\d*)日.*?(\d*:\d*)発走")
regex_title = re.compile(r"競馬 - (.+?) 結果 - スポーツナビ")
regex_meta = re.compile(r"(.+?)・(.+?) (\d+?)m \[コースガイド\]"
                        " \| 天気： \| 馬場： \| (.+?) \| (.+?)"
                        " \| (.+?) \|")
grades = ['新馬', '未勝利', '500万下', '900万下',
          '1000万下', '1600万下', 'オープン']


def parse_race_result(soup):
    def parse_result():
        table = soup.find(id='resultLs')
        if table is None:
            return None
        records = [trs.find_all('td') for trs in table.find_all('tr')]

        def trim_record(record, idx):
            res = dict()
            res['row_id'] = str(idx)
            res['final_position'] = record[0].text
            res['frame_number'] = record[1].text
            res['horse_number'] = record[2].text
            res['horse_id'] = regex_path.findall(record[3].a['href'])[0]
            res['sex'], res['age'] = regex_sex_age.findall(record[4].text)[0]
            res['jockey_id'] = regex_path.findall(record[5].a['href'])[0]
            res['jockey_weight'] = regex_jockey_weight.findall(
                record[10].text)[0]
            if res['final_position'].strip() == '取消':
                return {k: v.strip() for k, v in res.items()}
            weight = regex_weight.findall(record[11].text)[0][0]
            if weight:
                res['horse_weight'] = weight
            else:
                res['horse_weight'] = '-1'
            if res['final_position'].strip() == '除外':
                return {k: v.strip() for k, v in res.items()}
            weight = regex_weight.findall(record[11].text)[0][0]
            res['odds'] = record[13].text
            res['blinker'] = record[14].text
            if res['final_position'].strip() == '中止':
                return {k: v.strip() for k, v in res.items()}
            times = record[6].text.split('.')
            if len(times) > 2:
                res['time'] = '{}:{}.{}'.format(*times)
            else:
                res['time'] = '{}.{}'.format(*times)
            res['margin'] = record[7].text
            res['passing_position'] = record[8].text
            last_3f = record[9].text.split('.')
            if len(last_3f) == 3:
                res['last_3f'] = '{}:{}.{}'.format(*last_3f)
            elif len(last_3f) == 2:
                res['last_3f'] = '{}.{}'.format(*last_3f)
            res['popularity'] = record[12].text

            return {k: v.strip() for k, v in res.items()}

        records = [trim_record(record, idx)
                   for idx, record in enumerate(records) if record]
        return records

    def parse_info():
        # race_info
        res = dict()
        schedule = regex_day.findall(
            soup.find(id='raceTitDay').text)[0]
        res['race_date'] = date(int(schedule[0]), int(schedule[1]),
                                int(schedule[2])).isoformat()
        res['times'] = schedule[3]
        res['place'] = schedule[4]
        res['days'] = schedule[5]
        res['start_time'] = schedule[6]
        res['race_name'] = regex_title.findall(soup.title.text)[0]

        weather = soup.find_all(class_='spBg')
        res['weather'] = weather[0]['alt']
        res['track_condition'] = weather[1]['alt']

        # meta
        meta = regex_meta.findall(
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
            for grade in grades:
                if grade in meta[4]:
                    res['grade'] = grade
                    break
            else:
                print("Can't find grade. {}".format(res))
                raise

        res['race_type'] = meta[4]
        res['money'] = meta[5]
        return res

    def parse_link():
        all_links = [a_tag.get('href')
                     for a_tag in soup.find(id="resultLs").find_all('a')]
        links = dict()
        links['horse'] = [link for link in all_links if 'horse' in link]
        links['jockey'] = [link for link in all_links if 'jocky' in link]
        links['trainer'] = [link for link in all_links if 'trainer' in link]

        return links

    res = dict()
    url = soup.find_all(
        'meta', attrs={'property': 'og:url'})[0]['content']
    if any(x in url for x in ['denma', 'regist']):
        return
    race_id = regex_race_id.findall(url)[0]
    res['result'] = parse_result()
    for i in range(len(res['result'])):
        res['result'][i]['race_id'] = race_id

    if res['result'] is None:
        return None
    res['info'] = parse_info()
    res['info']['race_id'] = race_id
    links = parse_link()
    res['horse'] = links['horse']
    res['jockey'] = links['jockey']
    res['trainer'] = links['trainer']
    return res

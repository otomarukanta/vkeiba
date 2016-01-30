import re
from datetime import datetime as dt
from datetime import date


def parse_horse(soup):
    res = dict()

    # base info
    info = soup.find(id='dirTitName')
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
    pedigree = soup.find(id='dirUmaBlood').find_all('td')
    labels = ['sire', 'sire_sire', 'sire_sire_sire', 'sire_sire_mare',
              'sire_mare', 'sire_mare_sire', 'sire_mare_mare', 'mare',
              'mare_sire', 'mare_sire_sire', 'mare_sire_mare', 'mare_mare',
              'mare_mare_sire', 'mare_mare_mare']
    for label, name in zip(labels, pedigree):
        res[label] = name.text

    return res


def parse_race_list(soup):
    result = [tag.a["href"] for tag in soup.find_all(class_="wsLB")]
    return result


def parse_schedule_list(soup):
    table = [rows.find_all('td')
             for rows in soup.find(class_="scheLs").find_all('tr')]
    result = [row[1].a['href'] for row in table
              if row and row[1].a is not None]
    return result


def parse_jockey(soup):
    res = dict()

    info = soup.find(id='dirTitName')
    res['kana'] = info.p.text.split('|')[0].strip()
    res['name'] = info.h1.text
    lis = info.find_all('li')
    res['birthday'] = dt.strptime(
        lis[0].text.split('：')[1], '%Y年%m月%d日').date().isoformat()
    res['affiliation'] = lis[1].text.split('：')[1].split('(')[0].strip()
    res['license'] = lis[2].text.split('：')[1]

    return res


def parse_trainer(soup):
    res = dict()

    info = soup.find(id='dirTitName')
    res['kana'] = info.p.text.split('|')[0].strip()
    res['name'] = info.h1.text
    lis = info.find_all('li')
    res['birthday'] = dt.strptime(
        lis[0].text.split('：')[1], '%Y年%m月%d日').date().isoformat()
    res['affiliation'] = lis[1].text.split('：')[1].strip()
    res['license'] = lis[2].text.split('：')[1]

    return res

regex_race_id = re.compile("race\/result\/(\d+)")
regex_path = re.compile("/\w+/\w+/(\d+)/")
regex_sex_age = re.compile("(\w+)(\d+)")
regex_weight = re.compile("(\d*)\((.*?)\)")
regex_day = re.compile(r"(\d*)年(\d*)月(\d*)日.*?(\d*)回"
                       "(.*?)(\d)日.*?(\d*:\d*)発走")
regex_title = re.compile(r"競馬 - (.+?) 結果 - スポーツナビ")
regex_meta = re.compile(r"(.+?)・(.+?) (\d+?)m \[コースガイド\]"
                        " \| 天気： \| 馬場： \| (.+?) \| (.+?)"
                        " \| (.+?) \|")
grades = ['新馬', '未勝利', '500万下',
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
            res['time'] = record[6].text.replace('.', ':')
            res['margin'] = record[7].text
            res['passing_position'] = record[8].text
            res['last_3f'] = record[9].text
            res['jockey_weight'] = record[10].text
            weight = regex_weight.findall(record[11].text)[0][0]
            if weight:
                res['horse_weight'] = weight
            else:
                res['horse_weight'] = ''
            res['popularity'] = record[12].text
            res['odds'] = record[13].text
            res['blinker'] = record[14].text

            return {k: v.strip() for k, v in res.items()}
        records = [trim_record(record, idx)
                   for idx, record in enumerate(records) if record]
        return records

    def parse_info():
        # race_info
        res = dict()
        schedule = regex_day.findall(
            soup.find(id='raceTitDay').text)[0]
        res['date'] = date(int(schedule[0]), int(schedule[1]),
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
        res['round'] = meta[1]
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
                raise("Can't find grade")

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

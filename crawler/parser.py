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
regex_sex_age = re.compile("(\w+?)(\d+)")
regex_jockey_weight = re.compile("\w*?(\d+\.\d+)")
regex_weight = re.compile("(\d*)\((.*?)\)")
regex_day = re.compile(r"(\d*)年(\d*)月(\d*)日.*?(\d*)回"
                       "(.*?)(\d)日.*?(\d*:\d*)発走")
regex_title = re.compile(r"競馬 - (.+?) 結果 - スポーツナビ")
regex_meta = re.compile(r"(.+?)・(.+?) (\d+?)m \[コースガイド\]"
                        " \| 天気： \| 馬場： \| (.+?) \| (.+?)"
                        " \| (.+?) \|")
grades = ['新馬', '未勝利', '500万下', '900万下',
          '1000万下', '1600万下', 'オープン']



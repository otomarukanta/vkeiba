from datetime import datetime as dt


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

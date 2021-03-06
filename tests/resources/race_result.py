import datetime

expected = {
    "info":
    {
        "days": "1",
        "race_id": "0123456789",
        "rotation": "右",
        "place": "中山",
        "weather": "晴",
        "track_condition": "良",
        "track_type": "ダート",
        "race_name": "サラ系2歳未勝利",
        "money": "本賞金：500、200、130、75、50万円",
        "times": "5",
        "race_date": "2015-12-05",
        "race_condition": "サラ系2歳",
        "start_time": "9:50",
        "grade": "未勝利",
        "distance": "1200",
        "race_type": "未勝利 [指定] 馬齢"
    },
    "jockey":
    [
        "/directory/jocky/00001/",
        "/directory/jocky/00002/",
        "/directory/jocky/00003/",
        "/directory/jocky/00004/"
    ],
    "horse":
    [
        "/directory/horse/0000000001/",
        "/directory/horse/0000000002/",
        "/directory/horse/0000000003/",
        "/directory/horse/0000000004/"
    ],
    "trainer":
    [
        "/directory/trainer/00001/",
        "/directory/trainer/00002/",
        "/directory/trainer/00003/",
        "/directory/trainer/00004/"
    ],
    "result":
    [
        {
            "passing_position": "01-01",
            "age": "2",
            "margin": "",
            "race_id": "0123456789",
            "jockey_id": "00001",
            "time": datetime.time(0, 1, 23, 400000),
            "blinker": "",
            "horse_number": "2",
            "frame_number": "1",
            "odds": "6.9",
            "horse_id": "0000000001",
            "last_3f": datetime.time(0, 0, 38),
            "sex": "牡",
            "jockey_weight": "55.0",
            "final_position": "1",
            "row_id": "0",
            "popularity": "1",
            "horse_weight": "482"
        },
        {
            "passing_position": "02-03",
            "age": "3",
            "margin": "",
            "race_id": "0123456789",
            "jockey_id": "00002",
            "time": datetime.time(0, 1, 23),
            "blinker": "",
            "horse_number": "3",
            "frame_number": "2",
            "odds": "12.3",
            "horse_id": "0000000002",
            "last_3f": datetime.time(0, 0, 37, 900000),
            "sex": "牝",
            "jockey_weight": "55.0",
            "final_position": "2",
            "row_id": "1",
            "popularity": "3",
            "horse_weight": "464"
        },
        {
            "age": "4",
            "race_id": "0123456789",
            "jockey_id": "00003",
            "blinker": "B",
            "horse_number": "5",
            "frame_number": "3",
            "odds": "34.5",
            "horse_id": "0000000003",
            "sex": "せん",
            "jockey_weight": "60.0",
            "final_position": "中止",
            "row_id": "2",
            "popularity": "2",
            "horse_weight": "500"
        },
        {
            "passing_position": "",
            "age": "5",
            "margin": "",
            "race_id": "0123456789",
            "jockey_id": "00004",
            "time": None,
            "blinker": "B",
            "horse_number": "1",
            "frame_number": "1",
            "odds": "34.5",
            "horse_id": "0000000004",
            "last_3f": datetime.time(0, 0, 12, 300000),
            "sex": "せん",
            "jockey_weight": "60.0",
            "final_position": "3",
            "row_id": "3",
            "popularity": "4",
            "horse_weight": "500"
        }
    ]
}

from datetime import datetime

import jaconv

kata_fruits_list = [
    'アケビ',
    'アセロラ',
    'アボカド',
    'アンズ',
    'イチゴ',
    'イチジク',
    'ウメ',
    'カキ',
    'キウイフルーツ',
    'クリ',
    'グレープフルーツ',
    'ココヤシ',
    'サクランボ',
    'ザクロ',
    'スイカ',
    'スターフルーツ',
    'スモモ',
    'ドリアン',
    'パイナップル',
    'ナシ',
    'バナナ',
    'パパイヤ',
    'ブドウ',
    'ブルーベリー',
    'マンゴー',
    'ミカン',
    'ミラクルフルーツ',
    'メロン',
    'モモ',
    'ライチ',
    'ラフランス',
    'リンゴ',
    'レモン',
]
class Cmn_Validation():
    
    def check_object_format(row):

        try:
            fruit_name = row[0]
            Cmn_Validation.check_fruit_name(fruit_name)
            sales = row[1]
            isinstance(sales, int)
            total = row[2]
            isinstance(total, int)
            str_time = row[3]
            isinstance(datetime.strptime(str_time, '%Y-%m-%d %H:%M'), datetime)
        except:
            raise

    def check_fruit_name(fruit_name):

        isinstance(fruit_name, str)

        hira_fruits_list = []
        for fruit in kata_fruits_list:
            hira_fruit = jaconv.kata2hira(fruit)
            hira_fruits_list.append(hira_fruit)

        if fruit_name in kata_fruits_list:
            pass
        elif fruit_name in hira_fruits_list:
            pass
        else:
            raise
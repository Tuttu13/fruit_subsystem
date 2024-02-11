
import re

import jaconv


class Cmn_Fomatter():

    def check_kata_format(target_fruit):

        re_hiragana = re.compile(r'^[あ-ん]+$')
        if re_hiragana.fullmatch(target_fruit):
            kata_fruit_name = jaconv.hira2kata(target_fruit)
            return kata_fruit_name
        else:
            return target_fruit
        
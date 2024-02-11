import re

import pandas as pd
from django_pandas.io import read_frame

from fruit_app.models import FruitsSalesInfo


def get_df_all_sales_info():

        salesinfo = FruitsSalesInfo.objects.all()
        df_salesinfo = read_frame(salesinfo)
        return df_salesinfo
    
def format_sales_info_df():

    target_cols = ['fruit_name', 'sales', 'total', 'sales_at']
    df_salesinfo = get_df_all_sales_info()
    target_df = df_salesinfo[target_cols]
    del_df = target_df.drop(['sales_at'], axis=1)
    jp_df = target_df["sales_at"].dt.tz_convert('Asia/Tokyo')
    jp_time_df = pd.concat([del_df, jp_df], axis=1)
    dateidx_df = jp_time_df.set_index(['sales_at'])

    return dateidx_df

def get_latest_date_list(format_flg:str, dately_df:pd.DataFrame):

    check_data = dately_df.index.levels[1]
    format_time = _check_format_flg(format_flg)
    
    latest_date_list = []
    for check_data in check_data:
        target = check_data.strftime(format_time)
        latest_date_list.append(target)

    return latest_date_list[-3:]

def get_total_amount_list(format_flg:str, check_dately_list:list, monthly_total_dict:dict):

    format_time = _check_format_flg(format_flg)

    try:
        total_amount_list = []

        for i in monthly_total_dict:
            total = monthly_total_dict.get(i)
            check_time = i.strftime(format_time)

            if check_time in check_dately_list[-3:]:
                total_amount_list.append(total['total'])

    finally:
        return total_amount_list

def divide_bills(format_flg:str, chenge_dict:dict, check_dately_list:list):

    format_time = _check_format_flg(format_flg)
    data0, data1, data2 = [], [], []
    for i in chenge_dict:
        data = chenge_dict[i]
        fruit_name = i[0]
        time = i[1].strftime(format_time)

        text_data = _format_text_data(fruit_name, str(data['total']), str(data['sales']))

        if time == check_dately_list[-1]:
            if text_data:
                data0.append(text_data)
        elif time == check_dately_list[-2]:
            if text_data:
                data1.append(text_data)
        elif time == check_dately_list[-3]:
            if text_data:
                data2.append(text_data)

    return data0, data1, data2

def create_three_rows(check_list:list, total_amounty_list:list, data_str1:str, data_str2:str, data_str3:str):
    first_row = None
    second_row = None
    third_row = None
    try:
        first_row = {} if not check_list[-1] else {'month': check_list[-1], 'all': total_amounty_list[-1], 'detail': data_str1}
        second_row = {} if not check_list[-2] else {'month': check_list[-2], 'all': total_amounty_list[-2], 'detail': data_str2}
        third_row = {} if not check_list[-3] else {'month': check_list[-3], 'all': total_amounty_list[-3], 'detail': data_str3}
    finally:
        return first_row, second_row, third_row

def check_list(one, two, three):
    return [value for value in (one, two, three) if value]

def bills_str_formatter(data0:list, data1:list, data2:list):

    arg_list = [data0, data1, data2]
    format_list = []
    for target in arg_list:
        data_str = re.sub(r"[\[\]',]", '', str(target))
        format_list.append(data_str)

    return format_list[0], format_list[1], format_list[2]

def _check_format_flg(format_flg:str):

    if format_flg == 'monthly':
        format_time = '%Y/%m'
    elif format_flg == 'dayly':
        format_time = '%Y/%m/%d'

    return format_time

def _format_text_data(fruit_name, total, sales):
    if sales == '0':
        pass
    else:
        return ' {0}:{1}円({2})'.format(fruit_name, total, sales)
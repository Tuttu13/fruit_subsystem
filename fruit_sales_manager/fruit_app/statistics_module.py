from .models import FruitsSalesInfo
from django_pandas.io import read_frame
import pandas as pd
import re

def get_df_all_sales_info():

        salesinfo = FruitsSalesInfo.objects.all()
        df_salesinfo = read_frame(salesinfo)
        return df_salesinfo
    
def get_salese_info_df():

    target_cols = ['fruit_name', 'sales', 'total', 'sales_at']
    df_salesinfo = get_df_all_sales_info()
    target_df = df_salesinfo[target_cols]
    dateidx_df = target_df.set_index(['sales_at'])

    return dateidx_df

def get_check_list(format_flg:str, dately_df:pd.DataFrame):

    check_data = dately_df.index.levels[1]
    format_time = cmn_check_format_flg(format_flg)
    
    check_dately_list = []
    for check_data in check_data:
        target = check_data.strftime(format_time)
        check_dately_list.append(target)

    return check_dately_list[-3:]

def get_total_amount_list(format_flg:str, check_dately_list:list, monthly_total_dict:dict):

    format_time = cmn_check_format_flg(format_flg)

    try:
        dately_total_list = []

        for i in monthly_total_dict:
            total = monthly_total_dict.get(i)
            check_time = i.strftime(format_time)

            if check_time in check_dately_list[-3:]:
                dately_total_list.append(total['total'])

    finally:
        return dately_total_list

def divide_sales_info(format_flg:str, chenge_dict:dict, check_dately_list:list):

    format_time = cmn_check_format_flg(format_flg)
    data0, data1, data2 = [], [], []
    for i in chenge_dict:
        data = chenge_dict[i]
        fruit_name = i[0]
        time = i[1].strftime(format_time)

        text_data = format_text_data(fruit_name, str(data['total']), str(data['sales']))

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
    
def format_text_data(fruit_name, total, sales):
    if sales == '0':
        pass
    else:
        return ' {0}:{1}円({2})'.format(fruit_name, total, sales)

def create_row(check_list:list, total_amounty_list:list, data_str1:str, data_str2:str, data_str3:str):
    onerow = None
    tworow = None
    threerow = None
    try:
        onerow = {} if not check_list[-1] else {'month': check_list[-1], 'all': total_amounty_list[-1], 'detail': data_str1}
        tworow = {} if not check_list[-2] else {'month': check_list[-2], 'all': total_amounty_list[-2], 'detail': data_str2}
        threerow = {} if not check_list[-3] else {'month': check_list[-3], 'all': total_amounty_list[-3], 'detail': data_str3}
    finally:
        return onerow, tworow, threerow

def check_list(one, two, three):
    return [value for value in (one, two, three) if value]

def cmn_check_format_flg(format_flg:str):

    if format_flg == 'monthly':
        format_time = '%Y/%m'
    elif format_flg == 'dayly':
        format_time = '%Y/%m/%d'

    return format_time

def cmn_data_formatter(data0:list, data1:list, data2:list):

    arg_list = [data0, data1, data2]
    format_list = []
    for target in arg_list:
        data_str = re.sub(r"[\[\]',]", '', str(target))
        format_list.append(data_str)

    return format_list[0], format_list[1], format_list[2]
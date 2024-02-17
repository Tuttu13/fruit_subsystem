import itertools
import sqlite3
import traceback
from datetime import datetime, timedelta

current_datetime = datetime.now()

def get_all_data():
    
    select_all_data_query = "SELECT * FROM fruit_app_fruitssalesinfo" 

    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        cursor.execute(select_all_data_query)

        all_data = cursor.fetchall()
        all_data_list = [row for row in all_data]

        conn.close()
        return all_data_list
    except:
        traceback.print_exc()

def calc_total_amount():
    all_dately_list = get_all_data()
    total_amount = sum([tlist[3] for tlist in all_dately_list])
    return total_amount

def create_dately_key_list():
    
    three_days_ago = current_datetime - timedelta(days=3)

    dately_key_list = [
        (three_days_ago + timedelta(days=i)).strftime('%Y/%m/%d')
        for i in range(1, 4)]
    dately_key_list.sort(reverse=True)

    return dately_key_list

def create_monthly_key_list():

    monthly_key_list = [
        (current_datetime - timedelta(days=i * 30)).replace(day=1).strftime('%Y/%m')
        for i in range(3)]

    return monthly_key_list

def get_dict_lists(all_data_list):

    trimming_lists = _trimming_lists(all_data_list)

    db_cols = ['fruit_name', 'sales', 'total', 'sales_at']
    dict_lists = [dict(zip(db_cols, value)) for value in trimming_lists]

    return dict_lists

def format_datetime(date_type, formatter_dict_lists):

    date_format = _check_date_type(date_type)

    time_zone = timedelta(hours=9)

    for item in formatter_dict_lists:
        jst_time = datetime.strptime(item['sales_at'], '%Y-%m-%d %H:%M:%S') + time_zone
        item['sales_at'] = jst_time.strftime(date_format)

def get_sort_value_list(formatter_dict_lists):
    values_lists = [list(item.values()) for item in formatter_dict_lists]
    sort_list = sorted(values_lists, key=lambda x: x[3], reverse=True)
    return sort_list

def get_latest_three_day_data(key_list, sort_list):

    gruopby_list = [{key: list(group)} for key, group in itertools.groupby(
                    sort_list, key=lambda x: x[3])][:3]

    result_dict = {list(item.keys())[0]: list(item.values())[0] for item in gruopby_list}

    test_list = [result_dict.get(key, []) for key in key_list]

    sorted_data = [sorted(sublist, key=lambda x: x[0]) for sublist in test_list]
    return sorted_data

def create_bill_list(three_list):

    bills_list = []

    for onemonth in three_list:

        one_month_bill = []

        for key, group  in itertools.groupby(onemonth, lambda x: x[0]):
            group_dict = {key: list(group)}
            test_list = list(group_dict.values())

            if len(test_list[0]) > 1:
                max_length = max(map(len, test_list[0]))
                transposed_data = [list(map(lambda x: x[i] if i < len(
                                    x) else 0, test_list[0])) for i in range(max_length)]

                fruit = transposed_data[0]
                sums = [sum(sublist) for sublist in transposed_data[1:3]]
                sums.insert(0, fruit[0])
                one_month_bill.append(tuple(sums))
            else:
                fruit_info = tuple(test_list[0][0])
                one_month_bill.append(fruit_info)

        bills_list.append(one_month_bill)

    return bills_list

def create_bill_info(bills_list):
    rows_list = []
    total_sum_list = []

    for any_items in bills_list:
        bill_list = [_create_bill_str(item) for item in any_items]
        bill_sum_list = [item[2] for item in any_items]

        b = ' '.join(bill_list)
        bill_sum = sum(bill_sum_list)

        total_sum_list.append(bill_sum)
        rows_list.append(b)

    return total_sum_list, rows_list

def format_bill_list(three_date_list, total_sum_list, rows_list):

    format_rows_list = [
            {'month': data, 'all': tsum, 'detail': bill}
            for data, tsum, bill in zip(three_date_list, total_sum_list, rows_list)
        ]
    return format_rows_list

def _trimming_lists(all_data_list):
    trimming_lists = [tlist[1:5] for tlist in all_data_list]
    return trimming_lists

def _check_date_type(date_type):

    if date_type == "daily":
        date_format = '%Y/%m/%d'
    else:
        date_format = '%Y/%m'

    return date_format

def _create_bill_str(item):
    return "{fruit}:{price}円({quantity}) ".format(fruit=item[0], quantity=item[1], price=item[2])
import datetime
import itertools
from itertools import groupby
from operator import itemgetter

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from fruit_app.models import FruitsSalesInfo
from statistics_info import statistics_module as statistics
from statistics_info import statistics_module_r2 as statisticsr2


class SaleListView(LoginRequiredMixin,ListView):
    template_name = 'statistics.html'
    model = FruitsSalesInfo

    def get_context_data(self):
        context = super().get_context_data()

        context['3months_sales'] = GetContext.get_3months_sales_r2()
        context['total_profit'] = GetContext.get_total_profit()
        context['3months_sales'] = GetContext.get_3months_sales()
        context['3days_sales'] = GetContext.get_3days_sales()

        return context

class GetContext():

    def get_total_profit():
        df_salesinfo = statistics.get_df_all_sales_info()
        total_profit = df_salesinfo.total.sum(axis=0)
        return total_profit
    
    def get_3months_sales():

        format_type = 'monthly'

        try:
            all_monthly_df = statistics.format_sales_info_df()

            if all_monthly_df.empty:
                return None
            else:
                monthly_df = all_monthly_df.groupby('fruit_name').resample("ME").sum()
                monthly_dict = monthly_df.to_dict(orient='index')

            monthly_total_df = all_monthly_df.resample("ME").sum()
            del_df = monthly_total_df.drop(['fruit_name', 'sales'], axis=1)
            monthly_total_dict = del_df.to_dict(orient='index')

            latest_monthly_list = statistics.get_latest_date_list(format_type, monthly_df)

            monthly_total_amount_list = statistics.get_total_amount_list(format_type, latest_monthly_list, monthly_total_dict)

            first_bill, second_bill, third_bill = statistics.divide_bills(format_type, monthly_dict, latest_monthly_list)

            bill_str1, bill_str2, bill_str3 = statistics.bills_str_formatter(first_bill, second_bill, third_bill)

            first_row, second_row, third_row = statistics.create_three_rows(latest_monthly_list, monthly_total_amount_list, bill_str1, bill_str2, bill_str3)

            bills_list = statistics.check_list(first_row, second_row, third_row)

            return sorted(bills_list, key=lambda x: x['month'], reverse=True)
        
        except Exception as e:
            print(e)
            return None
    
    def get_3days_sales():
        
        format_type = 'dayly'

        try:
            all_dately_df = statistics.format_sales_info_df()

            if all_dately_df.empty:
                return None
            else:
                dately_df = all_dately_df.groupby('fruit_name').resample("D").sum()
                dately_dict = dately_df.to_dict(orient='index')

            dately_total_df = all_dately_df.resample("D").sum()
            del_df = dately_total_df.drop(['fruit_name', 'sales'], axis=1)
            dayly_total_dict = del_df.to_dict(orient='index')

            latest_dayly_list = statistics.get_latest_date_list(format_type, del_df)
            
            dately_total_amount_list = statistics.get_total_amount_list(format_type, latest_dayly_list, dayly_total_dict)

            first_bill, second_bill, third_bill = statistics.divide_bills(format_type, dately_dict, latest_dayly_list)

            bill_str1, bill_str2, bill_str3 = statistics.bills_str_formatter(first_bill, second_bill, third_bill)

            first_row, second_row, third_row = statistics.create_three_rows(latest_dayly_list, dately_total_amount_list, bill_str1, bill_str2, bill_str3)

            bills_list = statistics.check_list(first_row, second_row, third_row)
            
            return sorted(bills_list, key=lambda x: x['month'], reverse=True)

        except Exception as e:
            print(e)
            return None

    def get_3months_sales_r2():
        # 変数名注意

        all_dately_list = statisticsr2.get_all_data_list()
        
        # クエリしたデータから抽出 関数化
        formatter_lists = []
        for tlist in all_dately_list:
            formatter_list = tlist[1:5]
            formatter_lists.append(formatter_list)

        # 累計金額抽出 関数化
        bill_lists = []
        for tlist in all_dately_list:
            formatter_list = tlist[3]
            bill_lists.append(formatter_list)

        # データ成形 関数化
        db_cols = ['fruit_name', 'sales', 'total', 'sales_at']
        formatter_dict_lists = []

        for item in formatter_lists:
            fruit_info_dixt = dict(zip(db_cols, item))
            fruit_values_dixt = item
            list(fruit_values_dixt)
            jst_time  = datetime.datetime.strptime(fruit_info_dixt['sales_at'], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=9)
            jst_str_time = jst_time.strftime('%Y/%m')
            fruit_info_dixt['sales_at'] = jst_str_time
            formatter_dict_lists.append(fruit_info_dixt)
            # jst_time.strftime('%Y/%m')
            # print(item_time.astimezone(ZoneInfo("Asia/Tokyo")))

        # グルーピングしたい　groupby
        formatter_list_lists = []
        for data_d in formatter_dict_lists:
            print(data_d.values())
            formatter_list_lists.append(data_d.values())

        for key, group in formatter_list_lists:
            print(f'{key}: {list(group)}')



        


        


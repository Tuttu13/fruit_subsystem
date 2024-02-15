import datetime
import itertools

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
        
        # クエリしたデータから抽出
        formatter_lists = [tlist[1:5] for tlist in all_dately_list]

        # 累計金額抽出
        bill_lists = sum([tlist[3] for tlist in all_dately_list])
        print(bill_lists)
    
        # dict化
        db_cols = ['fruit_name', 'sales', 'total', 'sales_at']
        formatter_dict_lists = [dict(zip(db_cols, item)) for item in formatter_lists]

        for item in formatter_dict_lists:
            jst_time = datetime.datetime.strptime(item['sales_at'], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=9)
            item['sales_at'] = jst_time.strftime('%Y/%m')
            # timezone
            # jst_time.strftime('%Y/%m')
            # print(item_time.astimezone(ZoneInfo("Asia/Tokyo")))
        
        values_lists = [list(item.values()) for item in formatter_dict_lists]

        sort_list = sorted(values_lists, key=lambda x: x[3], reverse=True)

        # 3か月分のデータ分割
        gruopby_list = []
        key_list = []
        for k, g in itertools.groupby(sort_list, lambda x: x[3]):
            group_dict = {k: list(g)}
            key_list.append(k)
            gruopby_list.append(group_dict)
            if 3 < len(gruopby_list):
                break
        
        three__list = [
                [item[:3] + item[4:] for item in sorted(list(data.values())[0], key=lambda x: x[0])] for data in gruopby_list
            ]
        print(three__list)
        # 内訳作成
        bills_list = []
        for onemonth in three__list:
            one_month_bill = []
            for k, g in itertools.groupby(onemonth, lambda x: x[0]):
                group_dict = {k: list(g)}
                test_list = list(group_dict.values())
                if 1 < len(test_list[0]):
                    # 各サブリストの最大の長さを取得
                    max_length = max(map(len, test_list[0]))

                    # パディングしてリストの転置
                    transposed_data = [list(map(lambda x: x[i] if i < len(x) else 0, test_list[0])) for i in range(max_length)]

                    # 各行の合計を求める
                    sums = [sum(sublist) for sublist in transposed_data[1:3]]
                    
                    print(sums)
                    one_month_bill.append(sums)
                else:
                    print(test_list)
                    one_month_bill.append(test_list)
            bills_list.append(one_month_bill)

        print(bills_list)





        


        


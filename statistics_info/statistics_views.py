
import traceback

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from fruit_app.models import FruitsSalesInfo
from statistics_info import statistics_module_r2 as statisticsr2


class SaleListView(LoginRequiredMixin,ListView):
    template_name = 'statistics.html'
    model = FruitsSalesInfo

    def get_context_data(self):
        context = super().get_context_data()
        context['total_profit'] = GetContext.get_total_amount()
        context['total_profit'] = GetContext.get_total_amount()
        context['3months_sales'] = GetContext.get_3months_sales()
        context['3days_sales'] = GetContext.get_3days_sales()

        return context

class GetContext():

    def get_total_amount():

        all_dately_list = statisticsr2.get_all_data()
        total_amount = sum([tlist[3] for tlist in all_dately_list])
        return total_amount
    
    def get_3months_sales():

        date_type = "monthly"
        monthly_key_list = statisticsr2.create_monthly_key_list()
        print(monthly_key_list)

        try:
            # 変数名注意
            all_dately_list = statisticsr2.get_all_data()
            # データ成形
            formatter_dict_lists = statisticsr2.get_target_data(all_dately_list)
            statisticsr2.format_datetime(date_type, formatter_dict_lists)
            # ソートしたデータのみ取得
            sort_list = statisticsr2.get_sort_value_list(formatter_dict_lists)
            # 日付とフルーツ情報を取得
            three_list = statisticsr2.get_latest_three_day_data(monthly_key_list, sort_list)
            # 内訳作成
            bills_list = statisticsr2.create_bill_list(three_list)

            total_sum_list, rows_list = statisticsr2.create_bill_info(bills_list)

            format_rows_list = statisticsr2.format_bill_info(monthly_key_list, total_sum_list, rows_list)

            return format_rows_list

        except :
            traceback.print_exc()
            return None

    def get_3days_sales():

        date_type = "daily"
        dately_key_list = statisticsr2.create_dately_key_list()
        print(dately_key_list)

        try:
            # 変数名注意
            all_dately_list = statisticsr2.get_all_data()
            # データ成形
            formatter_dict_lists = statisticsr2.get_target_data(all_dately_list)
            statisticsr2.format_datetime(date_type, formatter_dict_lists)
            # ソートしたデータのみ取得
            sort_list = statisticsr2.get_sort_value_list(formatter_dict_lists)
            # 日付とフルーツ情報を取得
            three_list = statisticsr2.get_latest_three_day_data(dately_key_list, sort_list)
            # 内訳作成
            bills_list = statisticsr2.create_bill_list(three_list)

            total_sum_list, rows_list = statisticsr2.create_bill_info(bills_list)

            format_rows_list = statisticsr2.format_bill_info(dately_key_list, total_sum_list, rows_list)

            return format_rows_list
        except:
            traceback.print_exc()
            return None

import traceback

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from fruit_app.models import FruitsSalesInfo
from statistics_info import statistics_module as statisticsr


class SaleListView(LoginRequiredMixin,ListView):
    template_name = 'statistics.html'
    model = FruitsSalesInfo

    def get_context_data(self):
        context = super().get_context_data()
        context['total_profit'] = GetContext.get_total_amount()
        context['3months_sales'] = GetContext.get_3months_sales()
        context['3days_sales'] = GetContext.get_3days_sales()

        return context

class GetContext():

    def get_total_amount():

        try:
            total_amount = statisticsr.calc_total_amount()
            return total_amount
        except:
            traceback.print_exc()
            return None
    
    def get_3months_sales():

        date_type = "monthly"
        # 当月から3ヶ月取得
        monthly_key_list = statisticsr.create_monthly_key_list()
        try:
            all_data_list = statisticsr.get_all_data()
            # データ成形
            formatter_dict_lists = statisticsr.get_dict_lists(all_data_list)
            statisticsr.converter_datetime(date_type, formatter_dict_lists)
            # ソートしたデータのみ取得
            sort_list = statisticsr.get_sort_lists(formatter_dict_lists)
            # 日付とフルーツ情報を取得
            three_list = statisticsr.get_latest_three_day_data(monthly_key_list, sort_list)
            # 内訳作成
            bills_list = statisticsr.create_bill_list(three_list)
            # 月別集計金額と内訳取得
            total_sum_list, rows_list = statisticsr.generate_bill_info(bills_list)

            format_rows_list = statisticsr.generate_bill_list(monthly_key_list, total_sum_list, rows_list)

            return format_rows_list
        except:
            traceback.print_exc()
            return None

    def get_3days_sales():

        date_type = "daily"
        # 当日から3日間取得
        dately_key_list = statisticsr.create_dately_key_list()
        try:
            # 変数名注意
            all_dately_list = statisticsr.get_all_data()
            # データ成形
            formatter_dict_lists = statisticsr.get_dict_lists(all_dately_list)
            statisticsr.converter_datetime(date_type, formatter_dict_lists)
            # ソートしたデータのみ取得
            sort_list = statisticsr.get_sort_lists(formatter_dict_lists)
            # 日付とフルーツ情報を取得
            three_list = statisticsr.get_latest_three_day_data(dately_key_list, sort_list)
            # 内訳作成
            bills_list = statisticsr.create_bill_list(three_list)
            # 日別集計金額と内訳生成
            total_sum_list, rows_list = statisticsr.generate_bill_info(bills_list)
            # 
            format_rows_list = statisticsr.generate_bill_list(dately_key_list, total_sum_list, rows_list)

            return format_rows_list
        except:
            traceback.print_exc()
            return None
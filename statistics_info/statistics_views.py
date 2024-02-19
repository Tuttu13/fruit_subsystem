
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

        # 時間種別
        date_type = "monthly"
        # 当月から3ヶ月取得
        monthly_key_list = statisticsr.create_monthly_key_list()

        try:
            # データ取得
            all_data_list = statisticsr.get_all_data()
            # データ成形
            fruits_list = statisticsr.format_fruits_list(all_data_list)
            statisticsr.converter_datetime(date_type, fruits_list)
            # ソートしたデータのみ取得
            sort_fruits_list = statisticsr.get_sort_list(fruits_list)
            # 月付とフルーツ情報を取得
            latest_three_list = statisticsr.get_latest_fruits_list(monthly_key_list, sort_fruits_list)
            # 各月別の内訳作成
            bills_list = statisticsr.format_bill_list(latest_three_list)
            # 各月別の集計金額と内訳取得
            total_sum_list, row_list = statisticsr.generate_billinfo_list(bills_list)
            # 各月、売り上げ、内訳を結合
            bill_row_list = statisticsr.generate_bill_list(monthly_key_list, total_sum_list, row_list)

            return bill_row_list
    
        except:
            traceback.print_exc()
            return None

    def get_3days_sales():

        # 時間種別
        date_type = "daily"
        # 当日から3日間取得
        daily_key_list = statisticsr.create_daily_key_list()

        try:
            # データ取得
            all_data_list = statisticsr.get_all_data()
            # データ成形
            fruits_list = statisticsr.format_fruits_list(all_data_list)
            statisticsr.converter_datetime(date_type, fruits_list)
            # ソートしたデータのみ取得
            sort_fruits_list = statisticsr.get_sort_list(fruits_list)
            # 日付とフルーツ情報を取得
            latest_three_list = statisticsr.get_latest_fruits_list(daily_key_list, sort_fruits_list)
            # 各日別の内訳成形
            bills_list = statisticsr.format_bill_list(latest_three_list)
            # 各日別の集計金額と内訳生成
            total_sum_list, row_list = statisticsr.generate_billinfo_list(bills_list)
            # 各日、売り上げ、内訳を結合
            bill_row_list = statisticsr.generate_bill_list(daily_key_list, total_sum_list, row_list)

            return bill_row_list
    
        except:
            traceback.print_exc()
            return None
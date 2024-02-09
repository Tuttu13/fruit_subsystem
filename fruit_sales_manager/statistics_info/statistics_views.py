from fruit_app.models import FruitsSalesInfo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from statistics_info import statistics_module as statistics

class SaleListView(LoginRequiredMixin,ListView):
    template_name = 'statistics.html'
    model = FruitsSalesInfo

    def get_context_data(self):
        context = super().get_context_data()

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
            all_monthly_df = statistics.get_salese_info_df()

            if all_monthly_df.empty:
                return None
            else:
                monthly_df = all_monthly_df.groupby('fruit_name').resample("M").sum()
                monthly_dict = monthly_df.to_dict(orient='index')

            monthly_total_df = all_monthly_df.resample("M").sum()
            del_df = monthly_total_df.drop(['fruit_name', 'sales'], axis=1)
            monthly_total_dict = del_df.to_dict(orient='index')

            latest_monthly_list = statistics.get_check_list(format_type, monthly_df)

            monthly_total_amount_list = statistics.get_total_amount_list(format_type, latest_monthly_list, monthly_total_dict)

            first_detail, second_detail, third_detail = statistics.divide_sales_info(format_type, monthly_dict, latest_monthly_list)

            data_str1, data_str2, data_str3 = statistics.cmn_data_formatter(first_detail, second_detail, third_detail)

            first_row, second_row, third_row = statistics.create_row(latest_monthly_list, monthly_total_amount_list, data_str1, data_str2, data_str3)

            threemonth_list = statistics.check_list(first_row, second_row, third_row)

            return sorted(threemonth_list, key=lambda x: x['month'], reverse=True)
        
        except Exception as e:
            print(e)
            return None
    
    def get_3days_sales():
        
        format_type = 'dayly'

        try:
            all_dately_df = statistics.get_salese_info_df()

            if all_dately_df.empty:
                return None
            else:
                dately_df = all_dately_df.groupby('fruit_name').resample("D").sum()
                dately_dict = dately_df.to_dict(orient='index')

            dately_total_df = all_dately_df.resample("D").sum()
            del_df = dately_total_df.drop(['fruit_name', 'sales'], axis=1)
            dayly_total_dict = del_df.to_dict(orient='index')

            latest_dayly_list = statistics.get_check_list(format_type, dately_df)
            
            dately_total_amount_list = statistics.get_total_amount_list(format_type, latest_dayly_list, dayly_total_dict)

            first_detail, second_detail, third_detail = statistics.divide_sales_info(format_type, dately_dict, latest_dayly_list)

            data_str1, data_str2, data_str3 = statistics.cmn_data_formatter(first_detail, second_detail, third_detail)

            first_row, second_row, third_row = statistics.create_row(latest_dayly_list, dately_total_amount_list, data_str1, data_str2, data_str3)

            threemonth_list = statistics.check_list(first_row, second_row, third_row)
            
            return sorted(threemonth_list, key=lambda x: x['month'], reverse=True)

        except Exception as e:
            print(e)
            return None
from .models import FruitsSalesInfo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from fruit_app import statistics_module as static

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
        df_salesinfo = static.get_df_all_sales_info()
        total_profit = df_salesinfo.total.sum(axis=0)
        return total_profit
    
    def get_3months_sales():

        format_type = 'monthly'

        try:
            dateidx_df = static.get_salese_info_df()

            if dateidx_df.empty:
                return None
            else:
                monthly_df = dateidx_df.groupby('fruit_name').resample("M").sum()
                monthly_dict = monthly_df.to_dict(orient='index')

            monthly_total_df = dateidx_df.resample("M").sum()
            del_df = monthly_total_df.drop(['fruit_name', 'sales'], axis=1)
            monthly_total_dict = del_df.to_dict(orient='index')

            latest_monthly_list = static.get_check_list(format_type, monthly_df)

            monthly_total_list = static.get_total_amount_list(format_type, latest_monthly_list, monthly_total_dict)

            data0, data1, data2 = static.divide_sales_info(format_type, monthly_dict, latest_monthly_list)

            data_str1, data_str2, data_str3 = static.cmn_data_formatter(data0, data1, data2)

            first_row, second_row, third_row = static.create_row(latest_monthly_list, monthly_total_list, data_str1, data_str2, data_str3)

            threemonth_list = static.check_list(first_row, second_row, third_row)

            return sorted(threemonth_list, key=lambda x: x['month'], reverse=True)
        
        except Exception as e:
            print(e)
            return None
    
    def get_3days_sales():
        
        format_type = 'dayly'

        try:
            dateidx_df = static.get_salese_info_df()

            if dateidx_df.empty:
                return None
            else:
                dately_df = dateidx_df.groupby('fruit_name').resample("D").sum()
                dately_dict = dately_df.to_dict(orient='index')

            dately_total_df = dateidx_df.resample("D").sum()
            del_df = dately_total_df.drop(['fruit_name', 'sales'], axis=1)
            monthly_total_dict = del_df.to_dict(orient='index')

            check_dately_list = static.get_check_list(format_type, dately_df)
            
            dately_total_list = static.get_total_amount_list(format_type, check_dately_list, monthly_total_dict)

            data0, data1, data2 = static.divide_sales_info(format_type, dately_dict, check_dately_list)

            data_str1, data_str2, data_str3 = static.cmn_data_formatter(data0, data1, data2)

            oneday, twoday, threeday = static.create_row(check_dately_list, dately_total_list, data_str1, data_str2, data_str3)

            threemonth_list = static.check_list(oneday, twoday, threeday)
            
            return sorted(threemonth_list, key=lambda x: x['month'], reverse=True)

        except Exception as e:
            print(e)
            return None
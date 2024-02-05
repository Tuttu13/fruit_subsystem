from .models import FruitsSalesInfo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django_pandas.io import read_frame
import pandas as pd
import re

class SaleListView(LoginRequiredMixin,ListView):
    template_name = 'statistics.html'
    model = FruitsSalesInfo

    def get_context_data(self):
        context = super().get_context_data()

        context['total_profit'] = GetContext._get_total_profit()
        context['3months_sales'] = GetContext._get_3months_sales()
        context['3days_sales'] = GetContext._get_3days_sales()

        return context

class GetContext():
    
    def _getdf_all_sales_info():
        salesinfo = FruitsSalesInfo.objects.all()
        df_salesinfo = read_frame(salesinfo)
        return df_salesinfo

    def _get_total_profit():
        df_salesinfo = GetContext._getdf_all_sales_info()
        total_profit = df_salesinfo.total.sum(axis=0)
        return total_profit
    
    def _get_3months_sales():

        # 販売情報データ全取得
        target_cols = ['fruit_name', 'sales', 'total', 'sales_at']
        df_salesinfo = GetContext._getdf_all_sales_info()
        target_df = df_salesinfo[target_cols]
        dateidx_df = target_df.set_index(['sales_at'])

        # 月別各果物集計
        monthly_df = dateidx_df.groupby('fruit_name').resample("M").sum()
        monthly_dict = monthly_df.to_dict(orient='index')

        # 各月別の売上金額
        monthly_total_df = dateidx_df.resample("M").sum()
        del_df = monthly_total_df.drop(['fruit_name', 'sales'], axis=1)
        monthly_total_dict = del_df.to_dict(orient='index')

        # 各月売上総額
        monthly_total_list = []
        for i in monthly_total_dict:
           total = monthly_total_dict.get(i)
           monthly_total_list.append(total['total'])

        # 各月日判定用データ
        check_data = monthly_df.index.levels[1]
        check_list = []
        for check_data in check_data:
            target = check_data.strftime('%Y/%m')
            check_list.append(target)

        data0 = []
        data1 = []
        data2 = []
        for i in monthly_dict:
            data = monthly_dict.get(i)
            time = i[1].strftime('%Y/%m')
            if time == check_list[0]:
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                text_data = ' {0}:{1}円({2})'.format(name, total, sales)
                data0.append(text_data)
            if time == check_list[1]:
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                text1_data = ' {0}:{1}円({2})'.format(name, total, sales)
                data1.append(text1_data)
            if time == check_list[2]:
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                text2_data = ' {0}:{1}円({2})'.format(name, total, sales)
                data2.append(text2_data)
            else:
                pass
        data_str1 = re.sub(r"[\[\]',]", '', str(data0))
        data_str2 = re.sub(r"[\[\]',]", '', str(data1))
        data_str3 = re.sub(r"[\[\]',]", '', str(data2))

        onemonth = {
            'month': check_list[0], 
            'all': monthly_total_list[0], 
            'detail': data_str1
        }
        twomonth = {
            'month': check_list[1], 
            'all': monthly_total_list[1], 
            'detail': data_str2
        }
        threemonth = {
            'month': check_list[2], 
            'all': monthly_total_list[2], 
            'detail': data_str3
        }

        threemonth_list = [
            onemonth,
            twomonth,
            threemonth
        ]

        return sorted(threemonth_list, key=lambda x: x['month'], reverse=True)
    
    def _get_3days_sales():
        
        # 販売情報データ全取得
        target_cols = ['fruit_name', 'sales', 'total', 'sales_at']
        df_salesinfo = GetContext._getdf_all_sales_info()
        target_df = df_salesinfo[target_cols]
        dateidx_df = target_df.set_index(['sales_at'])

        # 日別各果物集計
        dately_df = dateidx_df.groupby('fruit_name').resample("D").sum()
        dately_dict = dately_df.to_dict(orient='index')

        # 日別の売上金額
        dately_total_df = dateidx_df.resample("D").sum().tail(3)
        del_df = dately_total_df.drop(['fruit_name', 'sales'], axis=1)
        monthly_total_dict = del_df.to_dict(orient='index')

        # 日別売上総額
        dately_total_list = []
        for i in monthly_total_dict:
           total = monthly_total_dict.get(i)
           dately_total_list.append(total['total'])

        # 各月日判定用データ
        check_data = dately_df.index.levels[1]
        check_list = []
        for check_data in check_data:
            target = check_data.strftime('%Y/%m/%d')
            check_list.append(target)

        data0 = []
        data1 = []
        data2 = []
        for i in dately_dict:
            data = dately_dict.get(i)
            time = i[1].strftime('%Y/%m/%d')
            if time == check_list[-1]:
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                text_data = ' {0}:{1}円({2})'.format(name, total, sales)
                data0.append(text_data)
            if time == check_list[-2]:
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                text1_data = ' {0}:{1}円({2})'.format(name, total, sales)
                data1.append(text1_data)
            if time == check_list[-3]:
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                text2_data = ' {0}:{1}円({2})'.format(name, total, sales)
                data2.append(text2_data)
            else:
                pass
        data_str1 = re.sub(r"[\[\]',]", '', str(data0))
        data_str2 = re.sub(r"[\[\]',]", '', str(data1))
        data_str3 = re.sub(r"[\[\]',]", '', str(data2))

        onemonth = {
            'month': check_list[-1], 
            'all': dately_total_list[-1], 
            'detail': data_str1
        }
        twomonth = {
            'month': check_list[-2], 
            'all': dately_total_list[-2], 
            'detail': data_str2
        }
        threemonth = {
            'month': check_list[-3], 
            'all': dately_total_list[-3], 
            'detail': data_str3
        }

        threemonth_list = [
            onemonth,
            twomonth,
            threemonth
        ]
        

        return sorted(threemonth_list, key=lambda x: x['month'], reverse=True)
    
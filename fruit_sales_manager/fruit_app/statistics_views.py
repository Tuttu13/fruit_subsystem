from .models import FruitsSalesInfo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django_pandas.io import read_frame
import pandas as pd

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

        # monthly_details = [
        #     {'month': "2018-07","sales": 19000 ,"breakdown": "ブルーベリー:3000円(10) レモン:1600円(20) パイナップル:2500円(10)"},
        #     {'month': "2018-06","sales": 13000 ,"breakdown": "ブルーベリー2:3000円(10) レモン:1600円(20) パイナップル:2500円(10)"},
        #     {'month': "2018-05","sales": 12000 ,"breakdown": "ブルーベリー3:3000円(10) レモン:1600円(20) パイナップル:2500円(10)"},
        # ]

        # 販売情報データ全取得
        target_cols = ['fruit_name', 'sales', 'total', 'sales_at']
        df_salesinfo = GetContext._getdf_all_sales_info()
        target_df = df_salesinfo[target_cols]
        dateidx_df = target_df.set_index(['sales_at'])
        
        # 日別各果物集計
        # dately_df = dateidx_df.groupby('fruit_name').resample("D").sum()
        # print(dately_df)

        # 月別各果物集計
        monthly_df = dateidx_df.groupby('fruit_name').resample("M").sum()
        monthly_dict = monthly_df.to_dict(orient='index')
        print(monthly_dict)

        # 各月別の売上金額
        monthly_total_df = dateidx_df.resample("M").sum()
        del_df = monthly_total_df.drop(['fruit_name', 'sales'], axis=1)
        monthly_total_dict = del_df.to_dict(orient='index')
        print(monthly_total_dict)

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
                total_val1 = monthly_total_dict.get(i)
                print(total_val1)
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                text_data = '{0}:{1}円({2})'.format(name, total, sales)
                data0.append(text_data)
            if time == check_list[1]:
                total_val2 = monthly_total_dict.get(i)
                print(total_val2)
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                text1_data = '{0}:{1}円({2})'.format(name, total, sales)
                data1.append(text1_data)
            if time == check_list[2]:
                total_val3 = monthly_total_dict.get(i)
                print(total_val3)
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                text2_data = '{0}:{1}円({2})'.format(name, total, sales)
                data2.append(text2_data)
            else:
                pass

        onemonth = {
            'month': check_list[0], 'all': total_val1, 'detail': data0
        }
        print(onemonth)
        twomonth = {
            'month': check_list[1], 'all': total_val2, 'detail': data1
        }
        print(twomonth)
        threemonth = {
            'month': check_list[2], 'all': total_val3, 'detail': data2
        }
        print(threemonth)

        # del_df = df2.drop(['fruit_name'], axis=1)
        # df_reset = del_df.reset_index()
        # df1 = df_reset['sales_at'].dt.date
        # del_df = df_reset.drop(['sales_at'], axis=1)
        # edit_df = pd.concat([del_df, df1], axis=1)
        # dx_df = edit_df.set_index(['sales_at'])
        # dflkhjg = dx_df.groupby('fruit_name').resample("M").sum()
        # print(dflkhjg)

        # 内訳用
        # target = edit_df.groupby(['sales_at', 'fruit_name']).sum()
        # d_index = target.to_dict(orient='index')
        # print(d_index)
    
    def _get_3days_sales():
        # salesinfo = GetContext._get_all_sales_info()
        return None
    
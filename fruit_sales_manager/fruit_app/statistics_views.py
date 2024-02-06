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

        context['total_profit'] = GetContext.get_total_profit()
        context['3months_sales'] = GetContext.get_3months_sales()
        context['3days_sales'] = GetContext.get_3days_sales()

        return context

class GetContext():

    def get_total_profit():
        df_salesinfo = GetContext._get_df_all_sales_info()
        total_profit = df_salesinfo.total.sum(axis=0)
        return total_profit
    
    def get_3months_sales():

        # 販売情報データ全取得
        dateidx_df = GetContext._get_salese_info_df()

        # 月別各果物集計
        monthly_df = dateidx_df.groupby('fruit_name').resample("M").sum()
        monthly_dict = monthly_df.to_dict(orient='index')

        # 各月別の売上金額
        monthly_total_df = dateidx_df.resample("M").sum()
        del_df = monthly_total_df.drop(['fruit_name', 'sales'], axis=1)
        monthly_total_dict = del_df.to_dict(orient='index')

        # 各月日判定用データ
        check_monthly_list = GetContext._get_check_monthly_list(monthly_df)

        # 各月売上総額
        monthly_total_list = GetContext._get_monthly_total_amount_list(check_monthly_list, monthly_total_dict)

        # 各月内訳生成
        data0, data1, data2 = GetContext._divide_sales_info(monthly_dict, check_monthly_list)

        # 各月内訳成形
        data_str1, data_str2, data_str3 = GetContext._data_formatter(data0, data1, data2)

        onemonth = {'month': check_monthly_list[-1], 'all': monthly_total_list[-1], 'detail': data_str1}
        twomonth = {'month': check_monthly_list[-2], 'all': monthly_total_list[-2], 'detail': data_str2}
        threemonth = {'month': check_monthly_list[-3], 'all': monthly_total_list[-3], 'detail': data_str3}

        threemonth_list = [
            onemonth,
            twomonth,
            threemonth
        ]

        return sorted(threemonth_list, key=lambda x: x['month'], reverse=True)
    
    def get_3days_sales():
        
        # 販売情報データ全取得
        dateidx_df = GetContext._get_salese_info_df()

        # 日別各果物集計
        dately_df = dateidx_df.groupby('fruit_name').resample("D").sum()
        dately_dict = dately_df.to_dict(orient='index')

        # 日別の売上金額
        dately_total_df = dateidx_df.resample("D").sum()
        del_df = dately_total_df.drop(['fruit_name', 'sales'], axis=1)
        monthly_total_dict = del_df.to_dict(orient='index')

        # 各月日判定用データ
        check_data = dately_df.index.levels[1]
        check_list = []
        for check_data in check_data:
            target = check_data.strftime('%Y/%m/%d')
            check_list.append(target)

        # 日別売上総額
        dately_total_list = []
        for i in monthly_total_dict:
            total = monthly_total_dict.get(i)
            check_time = i.strftime('%Y/%m/%d')
            if check_time == check_list[-1]:
                dately_total_list.append(total['total'])
            if check_time == check_list[-2]:
                dately_total_list.append(total['total'])
            if check_time == check_list[-3]:
                dately_total_list.append(total['total'])
            else:
                pass

        data0 = []
        data1 = []
        data2 = []

        chenge_dict = dict(reversed(dately_dict.items()))

        for i in chenge_dict:
            data = chenge_dict.get(i)
            time = i[1].strftime('%Y/%m/%d')
            if time == check_list[-1]:
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                if name == 0:
                    text_data = ' 0円(0)'
                else:
                    text_data = ' {0}:{1}円({2})'.format(name, total, sales)
                data0.append(text_data)
            if time == check_list[-2]:
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                if name == 0:
                    text1_data = ' 0円(0)'
                else:
                    text1_data = ' {0}:{1}円({2})'.format(name, total, sales)
                data1.append(text1_data)
            if time == check_list[-3]:
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                if name == 0:
                    text2_data = ' 0円(0)'
                else:
                    text2_data = ' {0}:{1}円({2})'.format(name, total, sales)
                data2.append(text2_data)
            else:
                pass

        data_str1, data_str2, data_str3 = GetContext._data_formatter(data0, data1, data2)

        oneday = {
            'month': check_list[-1], 'all': dately_total_list[-1], 'detail': data_str1
        }
        twoday = {
            'month': check_list[-2], 'all': dately_total_list[-2], 'detail': data_str2
        }
        threeday = {
            'month': check_list[-3], 'all': dately_total_list[-3], 'detail': data_str3
        }

        threemonth_list = [
            oneday, twoday, threeday
        ]
        
        return sorted(threemonth_list, key=lambda x: x['month'], reverse=True)
    
    def _get_df_all_sales_info():
        """販売情報に登録されている全てのレコードを取得

        Returns:
            Dataframe: 販売情報に登録されている全てのレコード
        """
        salesinfo = FruitsSalesInfo.objects.all()
        df_salesinfo = read_frame(salesinfo)
        return df_salesinfo
    
    def _get_salese_info_df():
        """販売情報に登録されている全てのレコードを成形したデータフレームを取得

            以下の4つのカラムのみ取得
                フルーツ名 : fruit_name
                売上数 : sales
                合計金額 : total
                販売日 : sales_at
    
        Returns:
            Dataframe: 販売情報に登録されている全てのレコードを成形したデータフレーム
        """

        target_cols = ['fruit_name', 'sales', 'total', 'sales_at']
        df_salesinfo = GetContext._get_df_all_sales_info()
        target_df = df_salesinfo[target_cols]
        dateidx_df = target_df.set_index(['sales_at'])

        return dateidx_df
    
    def _get_check_monthly_list(monthly_df:pd.DataFrame):

        check_data = monthly_df.index.levels[1]
        
        check_monthly_list = []
        for check_data in check_data:
            target = check_data.strftime('%Y/%m')
            check_monthly_list.append(target)

        return check_monthly_list
    
    def _get_monthly_total_amount_list(check_monthly_list:list, monthly_total_dict:dict):

        monthly_total_amount_list = []
        for i in monthly_total_dict:
            total = monthly_total_dict.get(i)
            check_time = i.strftime('%Y/%m')
            if check_time == check_monthly_list[-1]:
                monthly_total_amount_list.append(total['total'])
            if check_time == check_monthly_list[-2]:
                monthly_total_amount_list.append(total['total'])
            if check_time == check_monthly_list[-3]:
                monthly_total_amount_list.append(total['total'])
            else:
                pass

        return monthly_total_amount_list

    def _divide_sales_info(monthly_dict:dict, check_monthly_list:list):
        
        data0 = []
        data1 = []
        data2 = []
        for i in monthly_dict:
            data = monthly_dict.get(i)
            time = i[1].strftime('%Y/%m')
            if time == check_monthly_list[-1]:
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                text_data = ' {0}:{1}円({2})'.format(name, total, sales)
                data0.append(text_data)
            if time == check_monthly_list[-2]:
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                text1_data = ' {0}:{1}円({2})'.format(name, total, sales)
                data1.append(text1_data)
            if time == check_monthly_list[-3]:
                name = data['fruit_name']
                total = str(data['total'])
                sales = str(data['sales'])
                text2_data = ' {0}:{1}円({2})'.format(name, total, sales)
                data2.append(text2_data)
            else:
                pass

        return data0, data1, data2

    def _data_formatter(data0:list, data1:list, data2:list):
        """内訳詳細の不要な文字列を整形

        Args:
            data0 (list): 1つ目のデータ
            data1 (list): 2つ目のデータ
            data2 (list): 3つ目のデータ

        Returns:
            list: 3つの各データを成形し文字列に変換したリスト
        """

        arg_list = [data0, data1, data2]
        format_list = []
        for target in arg_list:
            data_str = re.sub(r"[\[\]',]", '', str(target))
            format_list.append(data_str)

        return format_list[0], format_list[1], format_list[2]

    
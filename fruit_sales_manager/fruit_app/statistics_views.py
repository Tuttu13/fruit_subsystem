from .models import FruitsSalesInfo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django_pandas.io import read_frame
import pandas as pd
import re
from collections import OrderedDict

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
    """コンテクストデータの取得クラス
        累計金額取得
        3か月分の月別データ取得
        3日分の日別データ取得
        
    """

    def get_total_profit():
        """累計金額取得

        Returns:
            int: 累計金額
        """
        df_salesinfo = GetContext._get_df_all_sales_info()
        total_profit = df_salesinfo.total.sum(axis=0)
        return total_profit
    
    def get_3months_sales():
        """3か月分の月別データ取得

        Returns:
            list: 3か月分の月別データ
        """

        format_flg = 'monthly'

        try:

            # 販売情報データ全取得
            dateidx_df = GetContext._get_salese_info_df()

            # 月別各果物集計
            if dateidx_df.empty:
                return None
            else:
                monthly_df = dateidx_df.groupby('fruit_name').resample("M").sum()
                monthly_dict = monthly_df.to_dict(orient='index')

            # 各月別の売上金額
            monthly_total_df = dateidx_df.resample("M").sum()
            del_df = monthly_total_df.drop(['fruit_name', 'sales'], axis=1)
            monthly_total_dict = del_df.to_dict(orient='index')

            # 各月日判定用データ
            check_monthly_list = GetContext._get_check_list(format_flg, monthly_df)

            # 各月売上総額
            monthly_total_list = GetContext._get_total_amount_list(format_flg, check_monthly_list, monthly_total_dict)

            # 各月内訳生成
            data0, data1, data2 = GetContext._divide_sales_info(format_flg, monthly_dict, check_monthly_list)

            # 各月内訳成形
            data_str1, data_str2, data_str3 = GetContext._cmn_data_formatter(data0, data1, data2)

            onemonth, twomonth, threemonth = GetContext._create_row(check_monthly_list, monthly_total_list, data_str1, data_str2, data_str3)

            threemonth_list = GetContext._check_list(onemonth, twomonth, threemonth)

            return sorted(threemonth_list, key=lambda x: x['month'], reverse=True)
        
        except Exception as e:
            print(e)
            return None
    
    def get_3days_sales():
        """3日分の日別データ取得

        Returns:
            list: 3日分の日別データ
        """
        
        format_flg = 'dayly'

        try:
        
            # 販売情報データ全取得
            dateidx_df = GetContext._get_salese_info_df()

            # 日別各果物集計
            if dateidx_df.empty:
                return None
            else:
                dately_df = dateidx_df.groupby('fruit_name').resample("D").sum()
                dately_dict = dately_df.to_dict(orient='index')

            # 日別の売上金額
            dately_total_df = dateidx_df.resample("D").sum()
            del_df = dately_total_df.drop(['fruit_name', 'sales'], axis=1)
            monthly_total_dict = del_df.to_dict(orient='index')

            # 各月日判定用データ
            check_dately_list = GetContext._get_check_list(format_flg, dately_df)
            

            # 日別売上総額
            dately_total_list = GetContext._get_total_amount_list(format_flg, check_dately_list, monthly_total_dict)
            # 各日別訳生成
            data0, data1, data2 = GetContext._divide_sales_info(format_flg, dately_dict, check_dately_list)
            # 各日別訳成形
            data_str1, data_str2, data_str3 = GetContext._cmn_data_formatter(data0, data1, data2)

            oneday, twoday, threeday = GetContext._create_row(check_dately_list, dately_total_list, data_str1, data_str2, data_str3)

            threemonth_list = GetContext._check_list(oneday, twoday, threeday)
            
            return sorted(threemonth_list, key=lambda x: x['month'], reverse=True)

        except Exception as e:
            print(e)
            return None

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
    
    def _get_check_list(format_flg:str, dately_df:pd.DataFrame):
        """最新月日を取得

        Args:
            format_flg (str): 月別か日別
            dately_df (pd.DataFrame): 月日別各果物集計

        Returns:
            check_dately_list (list): 最新月日
        """

        check_data = dately_df.index.levels[1]

        format_time = GetContext._cmn_check_format_flg(format_flg)
        
        check_dately_list = []
        for check_data in check_data:
            target = check_data.strftime(format_time)
            check_dately_list.append(target)

        return check_dately_list[-3:]
    
    def _get_total_amount_list(format_flg:str, check_dately_list:list, monthly_total_dict:dict):
        """各月日の総額を取得

        Args:
            format_flg (str): 月別か日別
            check_dately_list (list): 最新月日を取得
            monthly_total_dict (dict): 最新月日の売上金額

        Returns:
            dately_total_list (list): 各月日の総額
        """

        format_time = GetContext._cmn_check_format_flg(format_flg)

        try:

            dately_total_list = []
            for i in monthly_total_dict:
                total = monthly_total_dict.get(i)
                check_time = i.strftime(format_time)
                if check_time == check_dately_list[-1]:
                    dately_total_list.append(total['total']) 
                    continue
                if check_time == check_dately_list[-2]:
                    dately_total_list.append(total['total'])
                    continue
                if check_time == check_dately_list[-3]:
                    dately_total_list.append(total['total'])
                    continue
        finally:
            return dately_total_list
    
    def _divide_sales_info(format_flg:str, chenge_dict:dict, check_dately_list:list):
        """内訳を分割

        Args:
            format_flg (str): 月別か日別
            chenge_dict (dict): 最新月日を取得
            check_dately_list (list): 最新月日を取得

        Returns:
            _type_: _description_
        """

        format_time = GetContext._cmn_check_format_flg(format_flg)
        try:
            data0 = []
            data1 = []
            data2 = []

            for i in chenge_dict:
                data = chenge_dict.get(i)
                fruit_name = i[0]
                time = i[1].strftime(format_time)
                if time == check_dately_list[-1]:
                    name = fruit_name
                    total = str(data['total'])
                    sales = str(data['sales'])
                    if name == 0:
                        text_data = ' 0円(0)'
                    elif sales == '0':
                        pass
                    else:
                        text_data = ' {0}:{1}円({2})'.format(name, total, sales)
                    data0.append(text_data)
                    continue
                if time == check_dately_list[-2]:
                    name = fruit_name
                    total = str(data['total'])
                    sales = str(data['sales'])
                    if name == 0:
                        text1_data = ' 0円(0)'
                    elif sales == '0':
                        continue
                    else:
                        text1_data = ' {0}:{1}円({2})'.format(name, total, sales)
                    data1.append(text1_data)
                    continue
                if time == check_dately_list[-3]:
                    name = fruit_name
                    total = str(data['total'])
                    sales = str(data['sales'])
                    if name == 0:
                        text2_data = ' 0円(0)'
                    elif sales == '0':
                        continue
                    else:
                        text2_data = ' {0}:{1}円({2})'.format(name, total, sales)
                    data2.append(text2_data)
                    continue
                else:
                    pass
        finally:
            return data0, data1, data2
    
    def _create_row(check_list:list, total_amounty_list:list, data_str1:str, data_str2:str, data_str3:str):
        """各月or日の最新月日の売上と内訳行を作成

        Args:
            check_list (list): 最新月日のリスト
            total_amounty_list (list): 最新月日の総額リスト
            data_str1 (str): 内訳
            data_str2 (str): 内訳
            data_str3 (str): 内訳

        Returns:
            onerow (dict): 最新月日の売上と内訳
            tworow (dict): 最新月日の売上と内訳
            threerow (dict): 最新月日の売上と内訳
        """
        onerow = {}
        tworow = {}
        threerow = {}

        try:
            if check_list[-1]:
                onerow:dict = {'month': check_list[-1], 'all': total_amounty_list[-1], 'detail': data_str1}
            if check_list[-2]:
                tworow:dict = {'month': check_list[-2], 'all': total_amounty_list[-2], 'detail': data_str2}
            if check_list[-3]:
                threerow:dict = {'month': check_list[-3], 'all': total_amounty_list[-3], 'detail': data_str3}
        finally:
            return onerow, tworow, threerow
    

    def _check_list(one, two, three):

        threemonth_list = []
        if one:
            threemonth_list.append(one)
        if two:
            threemonth_list.append(two)
        if three:
            threemonth_list.append(three)

        return threemonth_list
    
    def _cmn_check_format_flg(format_flg:str):
        """月別か日別を判定

        Args:
            format_flg (str):月別(monthly) or 日別(dayly)

        Returns:
            format_time (str): 月別(%Y/%m) or 日別(%Y/%m/%d)
        """

        if format_flg == 'monthly':
            format_time = '%Y/%m'
        elif format_flg == 'dayly':
            format_time = '%Y/%m/%d'

        return format_time

    def _cmn_data_formatter(data0:list, data1:list, data2:list):
        """内訳詳細の不要な文字列を整形

        
            [: 左角かっこ
            ]: 右角かっこ
            ': シングルクォート
            ,: カンマ

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

    
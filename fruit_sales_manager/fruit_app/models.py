from django.db import models

class FruitsMaster(models.Model):
    fruit_id = models.AutoField(verbose_name = 'フルーツID' ,primary_key=True)
    fruit_name = models.CharField(verbose_name = 'フルーツ名' ,max_length=20)
    price = models.IntegerField(verbose_name = '単価')
    created_at = models.DateTimeField(verbose_name = '作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name = '更新日', auto_now=True)

class FruitsSalesInfo(models.Model):
    fruit_name = models.CharField(verbose_name = 'フルーツ名' ,max_length=20)
    sales = models.IntegerField(verbose_name = '売り上げ数')
    total = models.IntegerField(verbose_name = '売り上げ金額')
    sales_at = models.DateTimeField(verbose_name = '販売日時')
    created_at = models.DateTimeField(verbose_name = '作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name = '更新日', auto_now=True)
from django.forms import ModelForm
from django import forms
from .models import FruitsMaster, FruitsSalesInfo

class FruitForm(ModelForm):
    fruit_name = forms.CharField(label='フルーツ名')
    price = forms.CharField(label='単価')
    class Meta:
        model = FruitsMaster
        fields = ('fruit_name', 'price')

class saleForm(ModelForm):
    fruit_name = forms.CharField(label='フルーツ名')
    sales = forms.CharField(label='売り上げ数')
    total = forms.CharField(label='売り上げ金額')
    sales_at = forms.DateField(label='販売日時')
    class Meta:
        model = FruitsSalesInfo
        fields = ('fruit_name', 'sales', 'sales_at')

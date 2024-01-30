import csv
import io

from django.forms import ModelForm
from django import forms
from .models import FruitsMaster, FruitsSalesInfo
class FruitForm(ModelForm):
    fruit_name = forms.CharField(label='フルーツ名')
    price = forms.CharField(label='単価')
    class Meta:
        model = FruitsMaster
        fields = ('fruit_name','price')

class CSVUploadForm(forms.Form):
    file = forms.FileField(
        label='CSVファイル'
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError(
                '拡張子がcsvのファイルをアップロードしてください'
            )
        csv_file = io.TextIOWrapper(file, encoding='utf-8')
        reader = csv.reader(csv_file)

        for row in reader:
            FruitsSalesInfo.objects.create(
                fruit_name=row[0],
                sales=row[1],
                total=row[2],
                sales_at=row[3]
            )
    
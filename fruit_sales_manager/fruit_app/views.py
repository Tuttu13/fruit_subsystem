from django.views.generic import TemplateView
import csv
import io

from django import forms
from .models import FruitsSalesInfo
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse


class IndexView(TemplateView):
    template_name = 'index.html' 

@login_required
def csvimport(request):
    if request.method == 'POST':
        csv_file = request.FILES['form-data']
        csv_file = io.TextIOWrapper(csv_file, encoding='utf-8')
        reader = csv.reader(csv_file)

    for row in reader:
        FruitsSalesInfo.objects.create(
            fruit_name=row[0],
            sales=row[1],
            total=row[2],
            sales_at=row[3]
        )
    return redirect(reverse('sales')) 
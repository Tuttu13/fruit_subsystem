
import csv
import io

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView
from django.views.generic.list import ListView

from fruit_app.models import FruitsMaster, FruitsSalesInfo
from fruit_sales_manager import cmn_formatter as formatter
from fruit_sales_manager import cmn_validation as valid


class SaleListView(LoginRequiredMixin,ListView):
    template_name = 'fruit_sale/sale_list.html'
    model = FruitsSalesInfo
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) 
        queryset = queryset.order_by('-sales_at')

        return queryset

class SaleDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'fruit_sale/csvimport.html'
    model = FruitsSalesInfo
    success_url = reverse_lazy('sales')

@login_required
def createsale(request):

    template_name = 'fruit_sale/sale_add.html'
    fruits = FruitsMaster.objects.values('fruit_name')
    context = {'fluits_list': fruits,}

    if request.method == 'POST':
        try:
            data = request.POST

            target_fruit = data['fruit_name']
            validtion= valid.Cmn_Validation
            validtion.check_fruit_name(target_fruit)

            sales = data['sales']
            total = _get_total(target_fruit, sales)

            sales_at = data['saledate']

            FruitsSalesInfo.objects.create(
                fruit_name=target_fruit,
                sales=sales,
                total=total,
                sales_at=sales_at
            )
        finally:
            return redirect(reverse('sales')) 
    
    return render(request, template_name, context)

@login_required
def editsale(request, pk):

    template_name = 'fruit_sale/sale_edit.html'
    fruits = FruitsMaster.objects.values('fruit_name')
    context = {'fluits_list': fruits,}

    if request.method == 'POST':
        try:
            data = request.POST

            target_fruit = data['fruit_name']
            validtion= valid.Cmn_Validation
            validtion.check_fruit_name(target_fruit)

            sales = data['sales']
            total = _get_total(target_fruit, sales)

            sales_at = data['saledate']

            FruitsSalesInfo.objects.filter(pk=pk).update(
                fruit_name=target_fruit,
                sales=sales,
                total=total,
                sales_at=sales_at
            )
        finally:
            return redirect(reverse('sales')) 
    
    return render(request, template_name, context)

@login_required
def csvimport(request):
    template_name = 'fruit_sale/sale_list.html'
    try:
        if request.method == 'POST':
            
                csv_file = request.FILES['form-data']
                csv_file = io.TextIOWrapper(csv_file, encoding='utf-8-sig')
                reader = csv.reader(csv_file)

        for row in reader:
            try:
                validtion= valid.Cmn_Validation
                validtion.check_object_format(row)

                target_fruit= row[0]
                kana = formatter.Cmn_Fomatter
                kata_fruit = kana.check_kata_format(target_fruit)
                tz_time = row[3] + " +09:00"

                FruitsSalesInfo.objects.create(
                    fruit_name=kata_fruit,
                    sales=row[1],
                    total=row[2],
                    sales_at=tz_time
                )
            finally:
                continue
    except:
        return render(request, template_name, {'error': '文字コードutf-8形式のcsvをアップロードしてください'})

    return redirect(reverse('sales')) 

def _get_total(target_fruit, sales):
    test = FruitsMaster.objects.values_list('price').get(fruit_name='{0}'.format(target_fruit))
    total = test[0] * int(sales)

    return total

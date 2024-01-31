
from .models import FruitsSalesInfo, FruitsMaster

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DeleteView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

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
        data = request.POST
        target_fruit = data['fruit_name']
        sales = data['sales']
        total = _get_total(target_fruit, sales)
        sales_at = data['saledate']

        FruitsSalesInfo.objects.create(
            fruit_name=target_fruit,
            sales=sales,
            total=total,
            sales_at=sales_at
        )
        return redirect(reverse('sales')) 
    
    return render(request, template_name, context)\

@login_required
def editsale(request, pk):

    template_name = 'fruit_sale/sale_edit.html'
    fruits = FruitsMaster.objects.values('fruit_name')
    context = {'fluits_list': fruits,}

    if request.method == 'POST':
        data = request.POST
        target_fruit = data['fruit_name']
        sales = data['sales']
        total = _get_total(target_fruit, sales)
        sales_at = data['saledate']

        FruitsSalesInfo.objects.filter(pk=pk).update(
            fruit_name=target_fruit,
            sales=sales,
            total=total,
            sales_at=sales_at
        )
        return redirect(reverse('sales')) 
    
    return render(request, template_name, context)

def _get_total(target_fruit, sales):
# .get(target_fruit)
    test = FruitsMaster.objects.values_list('price').get(fruit_name='{0}'.format(target_fruit))
    total = test[0] * int(sales)

    return total

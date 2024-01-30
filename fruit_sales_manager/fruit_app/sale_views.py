from .forms import CSVUploadForm
from .models import FruitsSalesInfo

# クラスベース
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,UpdateView,DeleteView,CreateView
from django.views.generic.list import ListView
from django.views import generic
from django.urls import reverse_lazy, reverse
from fruit_sales_manager import cmn_func as cf

class SaleListView(LoginRequiredMixin, ListView):
    template_name = 'fruit_sale/sale_list.html'
    model = FruitsSalesInfo
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) 
        queryset = queryset.order_by('-sales_at')

        return queryset

class SaleCreateView(CreateView):
    pass

class SaleUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "fruit_sale/sale_edit.html"
    model = FruitsSalesInfo
    # form_class = FruitForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = cf.fix_data()
        return context

    def get_success_url(self):
        return reverse("list")

class SaleDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'fruit_sale/csvimport.html'
    model = FruitsSalesInfo
    success_url = reverse_lazy('sales')

class CsvImportView(generic.FormView):
    template_name = 'fruit_sale/sale_list.html'
    form_class = CSVUploadForm
    success_url = reverse_lazy('sales')
    

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.list import ListView

from .forms import FruitForm
from .models import FruitsMaster


class FruitListView(LoginRequiredMixin, ListView):
    template_name = 'fruit_master/fruits_list.html'
    model = FruitsMaster
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) 
        queryset = queryset.order_by('-created_at')

        return queryset
class FruitCreateView(CreateView):
    template_name = 'fruit_master/fruit_add.html'
    model = FruitsMaster
    form_class = FruitForm
    success_url = reverse_lazy('list')

    def get_success_url(self):
        return reverse("list")

class FruitUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "fruit_master/fruit_edit.html"
    model = FruitsMaster
    form_class = FruitForm

    def get_success_url(self):
        return reverse("list")

class FruitDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'fruit_master/fruits_list.html'
    model = FruitsMaster
    success_url = reverse_lazy('list')

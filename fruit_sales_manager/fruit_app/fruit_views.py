from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView
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

@login_required
def editsale(request, pk):

    template_name = 'fruit_master/fruit_edit.html'

    if request.method == 'POST':
        data = request.POST
        target_fruit = data['fruit_name']
        price = data['price']

        FruitsMaster.objects.filter(pk=pk).update(
            fruit_name=target_fruit,
            price=price,
        )
        return redirect(reverse('list')) 
    
    return render(request, template_name)


class FruitDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'fruit_master/fruits_list.html'
    model = FruitsMaster
    success_url = reverse_lazy('list')

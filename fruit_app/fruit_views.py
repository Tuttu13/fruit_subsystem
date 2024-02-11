from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView
from django.views.generic.list import ListView

from fruit_sales_manager import cmn_formatter as formatter
from fruit_sales_manager import cmn_validation as valid

from .models import FruitsMaster


class FruitListView(LoginRequiredMixin, ListView):
    template_name = 'fruit_master/fruits_list.html'
    model = FruitsMaster
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) 
        queryset = queryset.order_by('-updated_at')

        return queryset
    
@login_required
def createfruit(request):
    template_name = 'fruit_master/fruit_add.html'
    
    if request.method == 'POST':
        try:
            data = request.POST

            target_fruit = data['fruit_name']
            validtion = valid.Cmn_Validation
            validtion.check_fruit_name(target_fruit)
            kana = formatter.Cmn_Fomatter
            kata_fruit = kana.check_kata_format(target_fruit)

            price = data['price']

            FruitsMaster.objects.create(
                fruit_name=kata_fruit,
                price=price,
            )
            return redirect(reverse('list')) 
        except:
            return render(request, template_name, {'error': 'カタカナかひらがなで果物名を入力してください'})
            
    return render(request, template_name)

@login_required
def editsale(request, pk):

    template_name = 'fruit_master/fruit_edit.html'

    if request.method == 'POST':
        try:
            data = request.POST

            target_fruit = data['fruit_name']
            validtion= valid.Cmn_Validation
            validtion.check_fruit_name(target_fruit)
            kana = formatter.Cmn_Fomatter
            kata_fruit = kana.check_kata_format(target_fruit)

            price = data['price']

            FruitsMaster.objects.filter(pk=pk).update(
                fruit_name=kata_fruit,
                price=price,
            )
            return redirect(reverse('list')) 
        except:
            return render(request, template_name, {'error': 'カタカナかひらがなで果物名を入力してください'})

    return render(request, template_name)


class FruitDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'fruit_master/fruits_list.html'
    model = FruitsMaster
    success_url = reverse_lazy('list')


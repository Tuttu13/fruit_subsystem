from .forms import FruitForm
from .models import FruitsMaster

# クラスベース
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,UpdateView,DeleteView,CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse

class FruitListView(LoginRequiredMixin, ListView):
    template_name = 'fruit_master/fruits_list.html'
    model = FruitsMaster
    
    def get_queryset(self, **kwargs):
        # Article.objects.all() と同じ結果
        queryset = super().get_queryset(**kwargs) 
        # is_publishedがTrueのものに絞り、titleをキーに並び変える
        queryset = queryset.order_by('-created_at')

        return queryset
class FruitCreateView(CreateView):
    template_name = 'fruit_master/fruit_add.html'
    model = FruitsMaster
    form_class = FruitForm
    # 投稿に成功した時のURL
    success_url = reverse_lazy('list')

    # 投稿に成功した時に実行される処理
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

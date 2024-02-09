from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse


class IndexView(TemplateView):
    template_name = 'index.html' 


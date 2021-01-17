from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from users.forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('signup_done')
    template_name = 'signup.html'


def signup_done(request):
    return render(request, 'signup_done.html')
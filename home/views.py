
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import Admin_uSignUpForm, UserSignUpForm, NewProspectForm
from django.shortcuts import render
from .models import User, Prospect, Document, Item
# from django.utils.decorators import method_decorator
# from ..decorators import department_required
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)


def home(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'index.html', context)


class Admin_uSignUpView(CreateView):
    model = User
    form_class = Admin_uSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin_u'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user = form.save()
        login(self.request, user)
        return redirect('managers')


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'user'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.upline = self.kwargs['code']
        user = form.save()
        login(self.request, user)
        return redirect('agents')


def managers(request):
    prospects = Prospect.objects.all().filter(code=request.user.invitel)

    if request.method == "POST":
        form = NewProspectForm(request.POST)
        if form.is_valid():
            pp = form.save(commit=False)
            pp.code = request.user.invitel
            pp.agent = request.user
            pp.save()

            return redirect('managers')
    form = NewProspectForm()

    context = {
        'form': form,
        'prospects': prospects,
    }
    return render(request, 'managers.html', context)


def agents(request):
    prospects = Prospect.objects.all().filter(agent=request.user)

    if request.method == "POST":
        form = NewProspectForm(request.POST)
        if form.is_valid():
            pp = form.save(commit=False)
            pp.code = request.user.upline
            pp.agent = request.user
            pp.save()

            return redirect('agents')
    form = NewProspectForm()

    context = {
        'form': form,
        'prospects': prospects,
    }
    return render(request, 'agents.html', context)


def manage_agents(request):
    agents = User.objects.all().filter(upline=request.user.invitel)
    context = {
        'agents': agents,
    }
    return render(request, 'manage-agents.html', context)


def decider(request):
    if request.user.is_manager:
        return redirect('managers')
    elif request.user.is_user:
        return redirect('agents')
    else:
        return redirect('home')


def agents_home(request):
    documents = Document.objects.all()
    if request.method == "POST":
        form = NewProspectForm(request.POST)
        if form.is_valid():
            pp = form.save(commit=False)
            pp.code = request.user.upline
            pp.agent = request.user
            pp.save()

            return redirect('agents')
    form = NewProspectForm()

    context = {
        'form': form,
        'documents': documents

    }
    return render(request, 'agents_home.html', context)

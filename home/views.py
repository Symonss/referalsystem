
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import *
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
    if request.method == "POST":
        formms = NewMessageForm(request.POST)
        if formms.is_valid():
            pp22 = formms.save(commit=False)

            pp22.save()

            return redirect('home')
    formms = NewMessageForm()

    context = {
        'items': items,
        'formms': formms
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
        return redirect('')


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
        return redirect('agents-index')


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

    if request.method == "POST":
        formii = NewServiceForm(request.POST, request.FILES)
        if formii.is_valid():
            pp2 = formii.save(commit=False)

            pp2.save()

            return redirect('managers')
    formii = NewServiceForm()

    context = {
        'form': form,
        'formii': formii,
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

            return redirect('agents-index')
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
        return redirect('home')
    elif request.user.is_user:
        return redirect('agents-index')
    else:
        return redirect('home')


def agents_home(request):
    documents = Document.objects.all()
    prospects = Prospect.objects.filter(agent=request.user)
    print(prospects)
    if request.method == "POST":
        form = NewProspectForm(request.POST)
        if form.is_valid():
            pp = form.save(commit=False)
            pp.code = request.user.upline
            pp.agent = request.user
            pp.save()

            return redirect('agents-index')
    form = NewProspectForm()

    context = {
        'form': form,
        'prospects': prospects,
        'documents': documents

    }
    return render(request, 'admin/admin1.html', context)


def changestatus(request, pk):
    prospect = Prospect.objects.get(id=pk)

    prospect.status = 'initiated'
    prospect.save()

    return redirect('managers')


def approve(request, id):
    prospect = Prospect.objects.get(id=id)

    prospect.status = 'approved'
    prospect.save()

    return redirect('managers')


def decline(request, it):
    prospect = Prospect.objects.get(id=it)

    prospect.status = 'declined'
    prospect.save()

    return redirect('managers')


def tests(request):
    return render(request, 'admin/admin1.html')

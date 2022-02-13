from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView
from django.contrib import messages

from .forms import CreatePollForm, RegisterForm, LoginForm
from .models import Poll


def home(request):
    polls = Poll.objects.all()
    context = {
        'polls': polls
    }
    return render(request, 'home.html', context)


def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accueil')
    else:
        form = CreatePollForm()
    context = {
        'form': form
    }
    return render(request, 'create.html', context)


def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('resultats', poll.id)

    context = {
        'poll': poll
    }
    return render(request, 'vote.html', context)


def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll': poll
    }
    return render(request, 'results.html', context)


class LoginFormView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.add_message(
                self.request, messages.INFO,
                f'Hello {user.username}'
            )
            return super().form_valid(form)
        return super().form_invalid(form)


class RegisterFormView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    form = UserCreationForm()
    success_url = "/"

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data["confirm_password"]

        if password != confirm_password:
            form.add_error('confirm_password', "Les mots de passe ne se correspondent pas")
            return super().form_invalid(form)

        duplicate_users = User.objects.filter(username=username)
        if duplicate_users.exists():
            form.add_error('username', "Ce nom d'utilisateur est déjà utilisé")
            return super().form_invalid(form)
        user = User.objects.create_user(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return super().form_invalid(form)


class LogoutView(SuccessMessageMixin, TemplateView):
    def get(self, request, **kwargs):
        logout(request)
        return redirect("/")
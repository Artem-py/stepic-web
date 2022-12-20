from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import Question, Answer
from .forms import AskForm, AnswerForm, SignUpForm


def test(request):
    return HttpResponse('OK')


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'qa/signup.html', {'form': SignUpForm()})
    elif request.method == 'POST':
        try:
            user = User.objects.create_user(username=request.POST['username'],
                                            password=request.POST['password'])
            user.save()
            login(request, user)
            return redirect('index')
        except IntegrityError:
            return render(request, 'qa/signup.html', {'form': SignUpForm(), 
            'error': 'That username has already been taken. Please choose a new username'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'qa/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'qa/login.html', {'form': AuthenticationForm(),
                            'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('index')


@require_GET
def index(request):
    questions = Question.objects.new()
    paginator = Paginator(questions, 10)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'qa/index.html', {'page_obj': page_obj})


@require_GET
def popular(request):
    questions = Question.objects.popular()
    paginator = Paginator(questions, 10)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'qa/popular.html', {'page_obj': page_obj})


def detail(request, id):
    question = get_object_or_404(Question, id=id)
    answers = Answer.objects.filter(question=question)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.author = request.user
            new_answer.question = question
            new_answer.save()
            return redirect(question.get_absolute_url())
    else:    
        form = AnswerForm()
       
    return render(request, 'qa/detail.html', {'question': question,
                                              'answers': answers,
                                              'form': form})


def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.author = request.user
            new_question.save()
            return redirect(new_question.get_absolute_url())
    else:
        form = AskForm()
    return render(request, 'qa/ask.html', {'form': form})

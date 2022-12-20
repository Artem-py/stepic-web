from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from .models import Question, Answer
from .forms import AskForm, AnswerForm


def test(request):
    return HttpResponse('OK')


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
    question = Question.objects.get(id=id)
    answers = Answer.objects.filter(question=question)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.author = User.objects.get(pk=1)
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
            new_question.author = User.objects.get(pk=2)
            new_question.save()
            return redirect(new_question.get_absolute_url())
    else:
        form = AskForm()
    return render(request, 'qa/ask.html', {'form': form})

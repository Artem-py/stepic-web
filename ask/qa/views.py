from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator

from .models import Question, Answer


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
    return render(request, 'qa/detail.html', {'question': question, 'answers': answers})
    
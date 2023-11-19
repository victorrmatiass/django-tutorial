from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Choice, Question

# Create your views here.
'''
def index(request):
    if request.method == "GET":
        latest_question_list = Question.objects.order_by("-pub_date")[:5]
        context = {"latest_question_list": latest_question_list}
        return render(request, "polls/index.html", context)
    elif request.method == "POST":

        if request.POST.get('_method'):
            Question.objects.all().delete()
            return HttpResponse("Todos os dados deletados")

        question_t = request.POST.get("questao")
        question = Question(question_text=question_t, pub_date=timezone.now())
        question.save()
        return render(request, "polls/index.html")
            

def detail(request, question_id):
    if request.method == "GET":
        question = get_object_or_404(Question, pk=question_id)
        return render(request, "polls/details.html", {"question":question})
    elif request.method == "POST":
        question = Question.objects.get(pk=question_id)
        escolha = request.POST.get("escolha")
        question.choice_set.create(choice_text=escolha, votes=0)
        return render(request, "polls/details.html", {"question":question})
        return HttpResponse("Escolha registrada")

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
'''

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"

    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"    

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {"question":question,
        "error_message": "You didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
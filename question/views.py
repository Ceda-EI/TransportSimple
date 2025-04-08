from django.shortcuts import render
from django.views.generic import DetailView, ListView

from question.models import Question


class QuestionsView(ListView):
    queryset = Question.objects.all()


class QuestionView(DetailView):
    queryset = Question.objects.all()
    context_object_name = "question"

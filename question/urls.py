from django.urls import path

from question import views


urlpatterns = [
    path("", views.QuestionsView.as_view()),
    path("question/<str:slug>/", views.QuestionView.as_view(), name="question"),
]

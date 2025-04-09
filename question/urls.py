from django.urls import path

from question import views

urlpatterns = [
    path("", views.QuestionsView.as_view(), name="home"),
    path("ask-question/", views.CreateQuestionView.as_view(), name="ask-question"),
    path("question/<str:slug>/", views.QuestionView.as_view(), name="question"),
    path("question/<str:slug>/answer/", views.AnswerView.as_view(), name="answer"),
    path("question/<str:slug>/like/", views.ToggleLikeView.as_view(), name="like"),
    path(
        "answer/<int:pk>/like/",
        views.ToggleAnswerLikeView.as_view(),
        name="answer-like",
    ),
]

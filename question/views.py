import time

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.views.generic import CreateView, DetailView, FormView, ListView, View
from django.views.generic.detail import SingleObjectMixin

from question.models import Answer, Like, Question


class QuestionsView(ListView):
    queryset = Question.objects.all()


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']


class QuestionView(DetailView):
    queryset = Question.objects.all()
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['answer_form'] = AnswerForm
        if self.request.user.is_authenticated:
            ctx['liked'] = Like.objects.filter(author=self.request.user, question=self.object).count() > 0
        else:
            ctx['liked'] = False
        return ctx


class AnswerView(LoginRequiredMixin, SingleObjectMixin, FormView):
    form_class = AnswerForm
    model = Question

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        breakpoint()
        answer = form.save(commit=False)
        answer.author = self.request.user
        answer.question = self.object
        answer.save()
        messages.success(self.request, 'Added answer')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ToggleLikeView(LoginRequiredMixin, SingleObjectMixin, View):
    model = Question

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if like := Like.objects.filter(author=self.request.user, question=self.object).first():
            like.delete()
        else:
            Like.objects.create(
                author=self.request.user,
                question=self.object
            )
        return HttpResponseRedirect(self.object.get_absolute_url())


class CreateQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ["title", "body"]


    def _get_unique_slug(self, title):
        max_length: int = Question._meta.get_field('slug').max_length
        slug = slugify(title[:max_length])
        if not Question.objects.filter(slug=slug).count():
            return slug

        slug = slug[:max_length - 1]

        # Try suffixing 0 - 9 first
        for i in range(10):
            slug = slug + str(i)
            if not Question.objects.filter(slug=slug).count():
                return slug

        # Suffix timestamp else
        timestamp = f"{time.time():.2f}"
        return slugify(title[:max_length - len(timestamp)] + timestamp)


    def form_valid(self, form):
        self.object = question = form.save(commit=False)
        question.author = self.request.user
        question.slug = self._get_unique_slug(question.title)
        question.save()
        return super().form_valid(form)

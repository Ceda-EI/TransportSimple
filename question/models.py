from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Question(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="questions",
    )

    def get_absolute_url(self):
        return reverse("question", args=(self.slug,))

    @property
    def num_likes(self):
        return self.likes.aggregate(num=models.Count("author"))["num"]

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="answers",
    )
    body = models.TextField()

    @property
    def num_likes(self):
        return self.likes.aggregate(num=models.Count("author"))["num"]

    def __str__(self):
        return f"{self.author}'s answer of {self.question}"


class Like(models.Model):

    class Meta:
        unique_together = ("question", "author")

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="likes",
    )

    def __str__(self):
        return f"{self.author}: {self.question}"


class AnswerLike(models.Model):

    class Meta:
        unique_together = ("answer", "author")

    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="answer_likes",
    )

    def __str__(self):
        return f"{self.author}: {self.answer}"

from django.db import models
from django.contrib.auth import get_user_model

class Question(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    body = models.TextField()

    def __str__(self):
        return f"{self.author}'s answer of {self.question}"


class Like(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.author}: {self.question}"

    class Meta:
        unique_together = ("question", "author")

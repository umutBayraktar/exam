from django.db import models
from django.contrib.auth import get_user_model

class Choice(models.Model):
    choice_text = models.TextField()

    def __str__(self) -> str:
        return self.choice_text

class Question(models.Model):
    question_text = models.TextField()
    choices = models.ManyToManyField(Choice)
    right_choice = models.ForeignKey(Choice, related_name="questions", on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.question_text

class Exam(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), related_name="exams", on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    score = models.IntegerField()


class ExamScore(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    high_score = models.IntegerField()
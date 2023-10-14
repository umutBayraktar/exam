from django.contrib import admin
from exam.models import Choice,Question,Exam,ExamScore
# Register your models here.

admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Exam)
admin.site.register(ExamScore)
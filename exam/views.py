from typing import Any
from django import forms
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views import View
from .models import Exam, Question, ExamScore
from django.contrib.auth.mixins import LoginRequiredMixin


class QuestionForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for question in questions:
            choices = [(choice.id, choice.choice_text) for choice in question.choices.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label=question.question_text
            )

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Exam

class ExamListView(LoginRequiredMixin,ListView):
    model = Exam
    template_name = 'exam_list.html'
    context_object_name = 'exams'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_queryset(self) -> QuerySet[Any]:
        return Exam.objects.filter(user=self.request.user)

class ExamScoreListView(LoginRequiredMixin, ListView):
    model = ExamScore
    template_name = 'high_scores.html'
    context_object_name = 'exam_scores'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
   
    def get_queryset(self) -> QuerySet[Any]:
        return ExamScore.objects.filter(student=self.request.user)


class ExamView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, exam_id):
        exam = Exam.objects.get(id=exam_id)
        questions = exam.questions.all()
        question_form = QuestionForm(questions)
        return render(request, 'exam.html', {'question_form': question_form, 'exam_id': exam_id})

    def post(self, request, exam_id):
        exam = Exam.objects.get(id=exam_id)
        questions = exam.questions.all()
        question_form = QuestionForm(questions, request.POST)
        score = 0
        
        #import pdb;pdb.set_trace()
        if question_form.is_valid():
            # Kullanıcının seçtiği cevapları al
            user_answers = {}
            for question in questions:
                field_name = f'question_{question.id}'
                user_answer = question_form.cleaned_data[field_name]
                if int(user_answer) == question.right_choice.id:
                    score += 10
            # Kullanıcının cevaplarını kullanarak işlem yapabilirsiniz
            # Örneğin, doğru cevapları kontrol edebilir ve puanı hesaplayabilirsiniz
            # Burada, sadece cevapların ID'lerini alıyoruz
            exam_score = ExamScore.objects.filter(exam=exam, student=request.user).first()
            if exam_score:
                if score > exam_score.high_score:
                    exam_score.high_score = score
                    exam_score.save()
            else:
                ExamScore.objects.create(student=request.user, exam=exam, high_score=score)
            return render(request, 'result.html', {'user_answers': user_answers, 'exam_id': exam_id, 'score': score})
        else:
            # Form geçersizse hataları işleyebilirsiniz
            return render(request, 'exam.html', {'question_form': question_form, 'exam_id': exam_id})

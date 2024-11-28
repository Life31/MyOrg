from django.views.generic import CreateView
import re
import requests
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


from django.core.paginator import Paginator
from django.conf import settings

from django.shortcuts import render, get_object_or_404, redirect, reverse

from django.db.models import Q
from django.utils import timezone
import datetime as dt

from calendar import monthrange
import openpyxl
from openpyxl.styles import  Border, Side, PatternFill, Font, Alignment
#import pythoncom
#from win32com import client
import json
import random

from .models import Test, Question, Unswers
from .forms import QuestionForm, UnswersForm
User = get_user_model()


def show_test(request):
    return render(request, 'tests.html', {'test_id': 1, })


def show_test_result(request, user_id, test_id):

    questions = Question.objects.filter(test_id=test_id)
    unswrs= Unswers.objects.filter(user_id=user_id, test_id=test_id)
    results = {}
    i = 1
    for u in unswrs:
        unswers = [
            u.unswer_1, u.unswer_2, u.unswer_3, u.unswer_4, u.unswer_5,
            u.unswer_6, u.unswer_7, u.unswer_8, u.unswer_9, u.unswer_10,
            u.unswer_11, u.unswer_12, u.unswer_13, u.unswer_14, u.unswer_15,
            u.unswer_16, u.unswer_17, u.unswer_18, u.unswer_19, u.unswer_20,
        ]
        score = 0
        for q in questions: 
            if q.right_unswer == unswers.pop(0):
                score += 1
        results[i] = score
        i += 1
    return render(request, 'test_result.html', {'results': results, 'test_name': Test.objects.filter(id=test_id)[0].name, 'test_id': test_id, })


def test(request, test_id):
    questions = Question.objects.filter(test_id=test_id)
    test_name = Test.objects.filter(id=test_id)[0].name
    data = {}
    i = 1
    for q in questions:
        list = [q.right_unswer, q.unswer_2, q.unswer_3, q.unswer_4]
        random.shuffle(list)
        data[i] = {q.quest: list}
        i += 1
    unswers = Unswers()
    unswers.test_id = test_id
    unswers.user_id = request.user.id
    form = UnswersForm(
        request.POST or None,
        files=request.FILES or None,
        instance=unswers
    )
    if form.is_valid():
        form.save()
        return redirect('show_test_result', request.user.id, test_id)

    return render(request, 'tests.html', {'questions': data, 'test_name': test_name, 'form': form, 'test_id': test_id, } )


def redact_test(request, test_id):
    questions = Question.objects.filter(test_id=test_id)
    test_name = Test.objects.filter(id=test_id)[0].name

    form = QuestionForm(
        request.POST or None,
        files=request.FILES or None,

    )
    if form.is_valid():
        quest = form.save(commit=False)
        quest.id = int(quest.same_id)
        quest.save()
        return redirect('redact_test',  test_id)



    
    return render(request, 'test_redact.html', {
        'questions': questions,
        'test_name': test_name,
        'form': form,
        'test_id': test_id,
        } )



import datetime as dt
import requests
import re
#import win32com.client as win32
#import pythoncom
import time
from datetime import timedelta, date
from calendar import monthrange
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from django.conf import settings
#from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect  #, reverse
from background_task import background

from .forms import PostForm, PostForm_nuc, CommentForm, FeedbackForm
from .models import Comment, Group, Post, User, Feedback, Like, Dislike  #, Follow
from users.models import User_info
import json
import os
import transliterate

MONTH = dt.datetime.now().date().month
YEAR = dt.datetime.now().date().year
dayz = {'0': 'Понедельник',
        '1': 'Вторник',
        '2': 'Среда',
        '3': 'Четверг',
        '4': 'Пятница',
        '5': 'Суббота',
        '6': 'Воскресенье', }


def some_count(request):
    sib_count = Post.objects.filter(group=1, task_state_id=1).count
    acib_count = Post.objects.filter(group=2, task_state_id=1).count
    feedbacks_count = Feedback.objects.filter(state_id__in=[5, 6]).count # Новое, В работе
    users_counts = User.objects.all().count
    users_info = User_info.objects.all()
    users_with_vacation_access = [u.user_id for u in users_info if u.conf_access]
    users_with_task_access = [u.user_id for u in users_info if u.task_access]

    content = {
        'sib_count': sib_count,
        'acib_count': acib_count,
        'feedbacks_count': feedbacks_count,
        'users_counts': users_counts,
        'users_with_vacation_access': users_with_vacation_access,
        'users_with_task_access': users_with_task_access,
        'count_of_1': 0,
    }
    if request.user.username in settings.RIGHTS:
        try:
            ips = {'10.1.98.247', '10.1.98.248', '10.1.98.249', }
            rele_count_of_1 = []
            for ip in ips:
                res = requests.get(
                    'http://admin:admin@' + ip + '/pstat.xml',
                    verify=False,
                    timeout=1,
                )
                rele_count_of_1 += re.findall(r'[>][1][<]', str(res.content))
            content['count_of_1'] = len(rele_count_of_1)
        except Exception:
            content['count_of_1'] = 0
    return content


def rights(request):
    rights = {
        'rights': settings.RIGHTS,
        'storage_rights': settings.STORAGE_RIGHTS,
        'sadec_rights': settings.SADEC_RIGHTS,
        'pro_rights': settings.PRO_RIGHTS,
        'passes_rights': settings.PASSES_RIGHTS,
        **some_count(request),
        'page_name': 'Заявки на испытания',
    }
    return rights


# @cache_page(20)
def index(request):
    '''Календарь всех заявок - стартовая страница'''
    data_check = {}
    post_list = Post.objects.filter(task_state_id=2,)[:100]
    for post in post_list:
        if post.day == post_list[0].day and post.t_start_id >= post.t_stop_id:
            key = (str(post.day.date()+ dt.timedelta(days=1)) + ", " +
                   str(dayz[str((post.day.date()+ dt.timedelta(days=1)).weekday())]))
            data_check[key] = []
            break

    for post in post_list:
        key = str(post.day)[0:10] + ", " + str(dayz[str(post.day.weekday())])
        if key not in data_check.keys():
            data_check[key] = []
        data_check[key].append(post)
    keys = []
    for key in sorted(data_check.keys()):
        keys.append(key)
    for i in range(1, len(keys)):
        for el in data_check[keys[i-1]]:
            if (el.t_start_id >= el.t_stop_id
                and str(el.day.date()+ dt.timedelta(days=1)) == keys[i][0:10]):
                data_check[keys[i]].append(el)

    content = {
        #'data_check': data_check,
        'day': str(dt.date.today()),
    }
    return render(request, 'index.html', {**content, **rights(request)})


def day(request, day: str):
    '''Календарь на день'''

    # поиск предыдущего дня
    previos_day = dt.datetime.strptime(day, '%Y-%m-%d') - dt.timedelta(days=1)
    previos_day_for_search = str(previos_day) + '+00:00'
    previos_day_post_list = Post.objects.filter(
        day=previos_day_for_search,
        task_state_id__in=[2, 3],
    )
    # привод формата дня к timezone
    day_for_search = day + ' 00:00:00+00:00'

    post_list = Post.objects.filter(
        day=day_for_search,
        task_state_id__in=[2, 3],
    )

    data_check = {}
    if len(post_list) > 0:
        data_check[str(day)] = list(post_list.order_by('-t_start'))
    # если заявки из предыдущего переходят в текущий
    if len(previos_day_post_list) > 0:
        for el in list(previos_day_post_list.order_by('-t_start')):
            if el.t_start_id >= el.t_stop_id:
                if str(day) not in data_check.keys():
                    data_check[str(day)] = []
                data_check[str(day)].append(el)

    content = {'data_check': data_check, 'day': str(day), }
    return render(request, "follow.html", {**content, **rights(request)})


def get_key(post, d: int) -> str:  # 2022-11-29, Вторник
    day = post.day.date() + dt.timedelta(days=d)
    return str(day) + ", " + str(dayz[str(day.weekday())])


def week(request, wk):  # не отображает все события переходной недели из года в год
    '''Календарь на неделю'''
    data_check = {}
    days = []
    key = dt.datetime.strptime(str(wk[0:4]) + str(wk[5:]) + str(1), '%Y%W%w')
    previos_day = key.date() - dt.timedelta(days=1)
    previos_day_post_list = Post.objects.filter(
        day=previos_day,
        task_state_id__in=[2, 3],
    )

    days.append(str(key.date()) + ", " + str(dayz[str(key.date().weekday())]))

    for i in range(1, 7):
        key += dt.timedelta(days=1)
        days.append(str(key.date()) + ", " + str(dayz[str(key.date().weekday())]))
    for i in range(len(days)):
        data_check[days.pop()] = []
    year = int(wk[0:4])
    wk = int(wk[5:])
    #post_list = Post.objects.filter(day__range=[key - dt.timedelta(days=7), key],
    #                                task_state_id=2).order_by('-day', '-t_start')
    post_list = Post.objects.filter(day__week=wk,
                                    day__year=year,  # вот почему
                                    task_state_id__in=[2, 3]).order_by('-day', '-t_start')

    for post in post_list:
        key = get_key(post, 0)
        #key = (str(post.day)[0:10] + ", "
        #       + str(dayz[str(post.day.weekday())]))
        #if key not in data_check.keys():
        #    data_check[key] = []
        data_check[key].append(post)
    keys = []
    for key in sorted(data_check.keys()):
        keys.append(key)
    for i in range(1, len(keys)):
        for el in data_check[keys[i - 1]]:
            if (el.t_start_id >= el.t_stop_id
                and str(el.day.date() + dt.timedelta(days=1)) == keys[i][0:10]):
                data_check[keys[i]].append(el)

    if len(previos_day_post_list) > 0:
        for el in list(previos_day_post_list.order_by('-t_start')):
            if el.t_start_id >= el.t_stop_id:
                data_check[keys[0]].append(el)

    content = {'data_check': data_check,
               'day': str(dt.date.today()),
               'wk': str(year) + '-' + str(wk), }
    return render(request, 'week.html', {**content, **rights(request)})


def month(request, month):
    '''Каленгдарь на месяц'''
    data_check = {}
    year = int(month[0:4])
    month = int(month[5:])
    day_start_num = monthrange(year, month)[0]
    day_start_num_for_html = day_start_num * 2
    days = monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, days) + timedelta(1)
    data_by_weeks = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, }
    key_of_week = 0

    day_before = start_date - timedelta(day_start_num)
    day_after_num = (day_start_num + days - 1) % 7
    day_after = date(year, month, days) + timedelta(6 - day_after_num)
    for i in range(day_start_num):
        data_by_weeks[key_of_week][(day_before + timedelta(i)).strftime("%Y-%m-%d") + ", " +
                   dayz[str(i)]] = []

    for i in range(days):
        single_date = start_date + timedelta(i)
        data_check[single_date.strftime("%Y-%m-%d") + ", " +
                   dayz[str(day_start_num)]] = []
        data_by_weeks[key_of_week][single_date.strftime("%Y-%m-%d") + ", " +
                   dayz[str(day_start_num)]] = []
        day_start_num += 1
        if day_start_num == 7:
            key_of_week += 1
            day_start_num = 0

    for i in range(6 - day_after_num):
        data_by_weeks[key_of_week][(end_date + timedelta(i)).strftime("%Y-%m-%d") + ", " +
                   dayz[str(i + day_after_num + 1)]] = []

    post_list = Post.objects.filter(day__range=[day_before, day_after],
                                    task_state_id__in=[2, 3])
    for post in post_list:
        key = str(post.day)[0:10] + ", " + str(dayz[str(post.day.weekday())])
        if key in data_check.keys():
            data_check[key].append(post)
        for k in data_by_weeks.keys():
            if key in data_by_weeks[k].keys():
                data_by_weeks[k][key].append(post)
                break     
    month_all = {
        1:'Январь', 2:'Февраль', 3:'Март',
        4:'Апрель', 5:'Май', 6:'Июнь',
        7:'Июль', 8:'Август', 9:'Сентябрь',
        10:'Октябрь', 11:'Ноябрь', 12:'Декабрь',
    }
    if (month - 1) == 0:
        month_before = month_all[12]
    else:
        month_before = month_all[month - 1]
    if (month + 1) == 13:
        month_after = month_all[1]
    else:
        month_after = month_all[month + 1]

    content = {'data_check': data_check,
               'data_by_weeks': data_by_weeks,
               'day': str(dt.datetime.now().date()),
               'month': str(year) + "-" + str(month),
               'month_before': month_before,
               'month_after': month_after,
               'year': year,
               'current_month': month_all[month],
               'day_start_num_for_html': day_start_num_for_html, }
    return render(request, 'month.html', {**content, **rights(request)})


def calendar(request, year):
    if year == 0:
        year = dt.datetime.today().year
    today = dt.datetime.today().date()
    month_all = full_year(year)

    reqs = Post.objects.filter(day__year=year)
    rev_m = {
        'Январь': '01', 'Февраль': '02', 'Март': '03',
        'Апрель': '04', 'Май': '05', 'Июнь': '06',
        'Июль': '07', 'Август': '08', 'Сентябрь': '09',
        'Октябрь': '10', 'Ноябрь': '11', 'Декабрь': '12',
    }
    days = {}
    for req in reqs:
        if str(req.day.date()) not in days.keys():
            days[str(req.day.date())] = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,}
        days[str(req.day.date())][str(req.group_id)] += 1
        if req.t_start_id > req.t_stop_id:
            n_day = dt.datetime.strptime(str(req.day.date()), '%Y-%m-%d') + dt.timedelta(days=1)
            if str(n_day.date()) not in days.keys():
                days[str(n_day.date())] = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,}
            days[str(n_day.date())][str(req.group_id)] += 1


    for k, v in month_all.items():
        for kk, vv in v.items():
            for i in range(len(vv)):

                if len(str(vv[i])) == 1:
                    if str(year) + '-' + rev_m[k] + '-0' + str(vv[i]) in days.keys():
                        month_all[k][kk][i] = {'name': vv[i], ** days[str(year) + '-' + rev_m[k] + '-0' + str(vv[i])]}
                        #print(str(year) + '-' + rev_m[k] + '-0' + str(month_all[k][kk][i]['name']))
                    else:
                        month_all[k][kk][i] = {'name': vv[i], '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,}
                elif len(str(vv[i])) == 2:
                    if str(year) + '-' + rev_m[k] + '-' + str(vv[i]) in days.keys():
                        month_all[k][kk][i] = {'name': vv[i], ** days[str(year) + '-' + rev_m[k] + '-' + str(vv[i])]}
                        #print(str(year) + '-' + rev_m[k] + '-' + str(month_all[k][kk][i]['name']))
                    else:
                        month_all[k][kk][i] = {'name': vv[i], '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,}
                else:
                    month_all[k][kk][i] = {'name': vv[i], '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0,}

    holidays = {
        2022:{
            'Январь':[1], 'Февраль':[23], 'Март':[8],
            'Апрель':[], 'Май':[1,9], 'Июнь':[],
            'Июль':[], 'Август':[], 'Сентябрь':[],
            'Октябрь':[], 'Ноябрь':[4], 'Декабрь':[31],
        },
        2023:{
            'Январь':[1,2,3,4,5,6,7,8], 'Февраль':[23,24], 'Март':[8],
            'Апрель':[], 'Май':[1,8,9], 'Июнь':[12],
            'Июль':[], 'Август':[], 'Сентябрь':[],
            'Октябрь':[], 'Ноябрь':[6], 'Декабрь':[31],
        }
    }

    if year in holidays.keys():
        h_days = holidays[year]
    else:
        h_days = {}
    content = {
        **rights(request),
        'today': today,
        'year': year,
        'holidays': h_days,
        **month_all,
    }
    return render(request, 'task_calendar.html', {**content, })


def full_year(year):
    month_all = {
        1: 'Январь', 2: 'Февраль', 3: 'Март',
        4: 'Апрель', 5: 'Май', 6: 'Июнь',
        7: 'Июль', 8: 'Август', 9: 'Сентябрь',
        10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь',
    }
    month_new = {}
    for i in range(1, 13):
        day = dt.datetime.today().replace(
            year=year,
            month=i,
            day=1
        )
        mnth_strt_d = day.replace(month=i, day=1).weekday()
        days_in_month = monthrange(year, i)[1]
        weeks, k = {}, 1
        weeks[k] = []
        # добавляем пустые клетки в начале месяца, если он начался не с понедельника
        [weeks[k].append('') for j in range(mnth_strt_d) if mnth_strt_d != 0]
        # заполняем месяц
        for j in range(1, days_in_month + 1):
            if mnth_strt_d < 7:
                weeks[k].append(j)
                mnth_strt_d += 1
            else:
                k += 1
                weeks[k] = []
                weeks[k].append(j)
                mnth_strt_d = 1
        # добавляем пустые клетки в конце месяца, если он закончился не в воскресенье
        [weeks[k].append('') for j in range(mnth_strt_d, 7)]
        month_new[month_all[i]] = weeks
    return month_new


def stend(request, group_id):
    '''Календарь стенда'''
    data_check = {}
    post_list = Post.objects.filter(
        group=group_id,
        task_state_id__in=[2, 3],
    ).order_by('-day', '-t_start')[:100]

    for post in post_list:
        if post.t_start_id >= post.t_stop_id:
            key = get_key(post, 1)
            if key not in data_check.keys():
                data_check[key] = []
            data_check[key].append(post)
        key = get_key(post, 0)
        if key not in data_check.keys():
            data_check[key] = []
        data_check[key].append(post)

    filtrs = []
    if group_id == 4:  # FIB
        filtrs = ['1', '2', '3', '4', '5', 'MDU', '_']
    if group_id == 5:  # NUC
        filtrs = ['227', '237', '238', '239', '_']

    content = {
        'data_check': data_check,
        'day': str(dt.date.today()),
        'group_id': group_id,
        'filtrs': filtrs,
        'stend': Group.objects.filter(id=group_id)[0].title,
    }
    json_filtrs = json.dumps(filtrs)
    return render(request, 'index.html', {'json_filtrs': json_filtrs, **content, **rights(request)})


def stend_filtr(request, group_id, filtr):
    '''Календарь стенда отфильтрован'''
    data_check = {}
    post_list = Post.objects.filter(
        group=group_id,
        task_state_id=2,
    ).order_by('-day', '-t_start')[:200]

    for post in post_list:
        data = post.text.split('(')[1][:-1]
        if data != "":
            if data.find(',') != -1:
                fib_in = data.split(',')
            else:
                fib_in = [data]
            if filtr in fib_in or filtr == "_":
                if post.t_start_id >= post.t_stop_id:
                    key = get_key(post, 1)
                    if key not in data_check.keys():
                        data_check[key] = []
                    data_check[key].append(post)   
                key = get_key(post, 0)
                if key not in data_check.keys():
                    data_check[key] = []
                data_check[key].append(post)

    filtrs = []
    if group_id == 4:  # FIB
        filtrs = ['1', '2', '3', '4', '5', 'MDU', '_']
    if group_id == 5:  # NUC
        filtrs = ['227', '237', '238', '239', '_']

    content = {
        'data_check': data_check,
        'day': str(dt.date.today()),
        'group_id': group_id,
        'filtrs': filtrs,
        'stend': Group.objects.filter(id=group_id)[0].title,
    }
    return render(request, 'index.html', {**content, **rights(request)})


def stend_with_over(request, group_id):
    '''Календарь стенда'''
    data_check = {}
    post_list = Post.objects.filter(
        group=group_id, task_state_id__in=[2, 3],
    ).order_by('-day', '-t_start')[:200]

    for post in post_list:
        key = str(post.day)[0:10] + ", " + str(dayz[str(post.day.weekday())])
        if post.t_start_id >= post.t_stop_id:
            k = (str(post.day.date()+ dt.timedelta(days=1)) + ", " +
                 str(dayz[str((post.day.date()+ dt.timedelta(days=1)).weekday())]))
            if k not in data_check.keys():
                data_check[k] = []
        if key not in data_check.keys():
            data_check[key] = []
        data_check[key].append(post)

    keys = []
    for key in sorted(data_check.keys()):
        keys.append(key)

    for i in range(1, len(keys)):
        for el in data_check[keys[i - 1]]:
            if (el.t_start_id >= el.t_stop_id
                and str(el.day.date() + dt.timedelta(days=1)) == keys[i][0:10]):
                data_check[keys[i]].append(el)

    filtrs = []
    if group_id == 4:
        filtrs = ['1', '2', '3', '4', '5', 'MDU', '_']
    if group_id == 5:
        filtrs = ['227', '237', '238', '239', '_']
    content = {'data_check': data_check,
               'day': str(dt.date.today()),
               'group_id': group_id,
               'filtrs': filtrs,
               'stend': Group.objects.filter(id=group_id)[0].title, }
    return render(request, 'index.html', {**content, **rights(request)})


def stend_filtr_with_over(request, group_id, filtr):
    '''Календарь стенда'''
    data_check = {}
    post_list = Post.objects.filter(
        group=group_id, task_state_id__in=[2, 3],
    ).order_by('-day', '-t_start')[:200]

    for post in post_list:
        data = post.text.split('(')[1][:-1]
        if data != "":
            if data.find(',') != -1:
                fib_in = data.split(',')
            else:
                fib_in = [data]
            for fib in fib_in:
                if fib == filtr or filtr == "_":
                    key = str(post.day)[0:10] + ", " + str(dayz[str(post.day.weekday())])
                    if post.t_start_id >= post.t_stop_id:
                        k = (str(post.day.date() + dt.timedelta(days=1)) + ", "
                             + str(dayz[str((post.day.date() + dt.timedelta(days=1)).weekday())]))
                        if k not in data_check.keys():
                            data_check[k] = []
                    if key not in data_check.keys():
                        data_check[key] = []
                    if post not in data_check[key]:
                        data_check[key].append(post)
        else:
            fib_in = []
    keys = []
    for key in sorted(data_check.keys()):
        keys.append(key)

    for i in range(1, len(keys)):
        for el in data_check[keys[i - 1]]:
            if (
                el.t_start_id >= el.t_stop_id
                and str(el.day.date() + dt.timedelta(days=1)) == keys[i][0:10]
            ):
                data_check[keys[i]].append(el)

    filtrs = []
    if group_id == 4:
        filtrs = ['1', '2', '3', '4', '5', 'MDU', '_']
    if group_id == 5:
        filtrs = ['227', '237', '238', '239', '_']
    content = {'data_check': data_check,
               'day': str(dt.date.today()),
               'group_id': group_id,
               'filtrs': filtrs,
               'stend': Group.objects.filter(id=group_id)[0].title, }
    return render(request, 'index.html', {**content, **rights(request)})


def counts(group):  # group/author
    '''Вспомогательная функция для вычисления кол-ва типовых заявок'''
    counts = {
        'count': group.posts.all().count(),
        'count_new': group.posts.filter(task_state_id=1).count(),
        'count_in_progr': group.posts.filter(task_state_id=2).count(),
        'count_postponed': group.posts.filter(task_state_id=4).count(),
        'count_finished': group.posts.filter(task_state_id=3).count(),
    }
    return counts


def group_posts(request, slug):
    '''Список задач стенда'''
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    content = {"group": group, 'page': page,}
    return render(request, "group.html", {**content, **counts(group), **rights(request)})


def group_posts_states(request, slug, state_id: int):
    '''Список фильтрованых задач стенда'''
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.filter(task_state_id=state_id)
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    content = {"group": group, 'page': page, }
    return render(request, "group.html", {**content, **counts(group), **rights(request)})


def profile(request, username):
    '''Список заявок сотрудника'''
    author = get_object_or_404(User, username=username)
    all_posts = author.posts.all()
    paginator = Paginator(all_posts, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    content = {
        'author': author,
        'page': page,
        **counts(author),
        **rights(request),
    }
    return render(request, 'profile.html', {**content, })


def post_view(request, username, post_id):
    '''Страница заявки'''
    author = User.objects.get(username=username)
    post = Post.objects.select_related('author').get(id=post_id)
    day = str(post.day.date())
    comments = post.comments.all()
    form = CommentForm()

    content = {
        'form': form,
        'post': post,
        'day': day,
        'author': author,
        'comments': comments,
        'dunger': cross_for_view(request, post),
        **rights(request),
        **counts(author),
    }
    return render(request, 'post.html', {**content, })


def cross_for_view(request, post):
    '''Вспомогательная функция для отображения пересечений'''
    dunger = ''
    data_check = {}
    day = str(post.day.date())
    day_for_check = day + ' 00:00:00+00:00'

    data_check[day] = []
    post_list = Post.objects.filter(
        day=day_for_check,
        task_state_id=2,
        group=post.group,
    ).exclude(id=post.id)
    if len(post_list) == 0:
        print(len(post_list))
        return dunger

    for p in post_list:
        data_check[day].append(p)
    if cross(request, post, data_check, day, 'new') != "no_cross":
        dunger = ('Интервал времени данной заявки ПЕРЕСЕКАЕТСЯ'
                  ' с интервалами времени других заявок.')
    return dunger


def post_view_change(request, username, post_id, state_id):
    '''Функция смены статуса заявки'''
    states = {2: 'подтверждена', 3: 'завершена', 4: 'отклонена', }
    author = User.objects.get(username=username)
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    post.task_state_id = state_id
    post.save()
    day = str(post.day.date())
    url = ('http://virtual2025.oak.cc:8000/' + username
           + '/' + str(post.id) + '/')
    mail_text = (f"Заявка {post.text} {states[state_id]} - {url}")
    mail(
        author.email,
        settings.RIGHTS,
        post.text + " " + states[state_id] + ".",
        mail_text,
    )
    comments = post.comments.all()
    form = CommentForm()
    content = {
        'form': form,
        'post': post,
        'author': author,
        'comments': comments,
        'day': day,
        'dunger': cross_for_view(request, post),
        **counts(author),
        **rights(request),
    }
    return render(request, 'post.html', {**content, })


def mail(author, rights, subject, body):
    '''Вспомогательная функция отправки письма'''
    recipients = []
    if len(rights) > 0:
        for user in rights:
            recipients.append(user + '@ic.irkut.com')
    recipients.append(author)
    text = body
    
    text_part = MIMEText(text, 'plain')
    msg_alternative = MIMEMultipart('alternative')
    msg_alternative.attach(text_part)
    msg_mixed = MIMEMultipart('mixed')
    msg_mixed.attach(msg_alternative)
    msg_mixed['From'] = 'rrz@ic.irkut.com'
    msg_mixed['To'] = ", ".join(recipients)
    msg_mixed['Subject'] = subject
    try:
        smtp_obj = smtplib.SMTP('mailserv.oak.cc', port=587)
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.login('rrz', settings.EMAIL_HOST_PASSWORD)
        smtp_obj.sendmail(msg_mixed['From'], recipients, msg_mixed.as_string())
        smtp_obj.quit()
    except Exception:
        print('Почтовая рассылка недоступна')


def words(*args):
    words = {
        'wrong_date':
            (
                f": Нельзя назначить дату и время начала испытаний в прошлом.\n"
            f"Текущая дата - {dt.datetime.now().date()}.\n"
            f"Текущее время - {str(dt.datetime.now().time())[:8]}.\n"
            f"Также нельзя назначить дату испытаний на воскресенье!"),
        'wrong_time': (
            f" : диапазон времени указан неверно!\n"
                       f" Время начала не может быть равно 23:59,\n"
                       f" Время окончания не может быть равно 00:00,\n"
                       f" Время начала не может быть равно времени окончания."),
        'new':
            (
                f"Заявка {args[0].text} создана.\nВыбранный вами интервал "
            f"времени пересекается с интервалом заявки {args[1].text}.\n"
            f"Измените интервал времени, или согласуйте совместное"
            f" проведение работ с автором приоритетной заявки"
            f" {args[1].text}."),
        'edit':
            (
                f"Заявка {args[0].text} изменена.\nВыбранный вами интервал "
            f"времени пересекается с интервалом заявки {args[1].text}.\n"
            f"Измените интервал времени, или согласуйте совместное"
            f" проведение работ с автором приоритетной заявки"
            f" {args[1].text}."),
        'm_new':
            (
                f"Заявка {args[0].text} создана - {args[2]}.\n"
            f"Выбранный вами интервал времени пересекается"
            f" с интервалом заявки {args[1].text} - {args[3]}.\n"
            f"Измените интервал времени, или согласуйте "
            f"совместное проведение работ с автором "
            f"приоритетной заявки {args[1].text}."),
        'm_edit':
            (
                f"Заявка {args[0].text} изменена - {args[2]}.\n"
            f"Выбранный вами интервал времени пересекается"
            f" с интервалом заявки {args[1].text} - {args[3]}.\n"
            f"Измените интервал времени, или согласуйте "
            f"совместное проведение работ с автором "
            f"приоритетной заявки {args[1].text}."),
        'confirm':
            (
                f"Заявка {args[0].text} на стенд {args[0].group} создана. {args[2]} \n"
            f"После подтверждения администратором она отобразится в календарях.\n"
            f"Заявка подана на дату: {str(args[0].day)[:10]} на временной интервал c {args[0].t_start} по {args[0].t_stop}.\n"
            f"Подразделение-инициатор: {args[0].unit}.\n"
            f"Автор заявки: {args[0].author}.\n"
            f"Статус заявки: {args[0].task_state}.\n"
            f"Состав бригады испытателей: {args[0].testers}.\n"
            f"Объект испытаний: {args[0].test_object}.\n"
            f"Цель работ: {args[0].purpose}.\n"
            f"Основание для проведения работ: {args[0].reason}.\n"
            f"Необходимая конфигурация стенда: {args[0].configuration}.\n"
            f"Требуемые инструменты: {args[0].instruments}.\n"
            f"Прочие требования: {args[0].add_requirements}.\n"
            f"Документ: {args[0].doc}.\n"), }
    return words[args[4]]


def cross(request, post, data_check, day, key):
    '''Вспомогательная функция поиска пересечений временных интервалов'''
    ISIB = post.text[:4]
    bracet_post = str(post.text).find('(')
    for p in data_check[str(day)]:
        bracet_p = str(p.text).find('(')
        if (
            (ISIB != 'ISIB' and ISIB != 'NUC-' and ISIB != 'FIB ')
            or post.text[bracet_post:] == p.text[bracet_p:]
            or (bracet_post == -1 and bracet_p == -1)
        ):
            if p.t_start_id > p.t_stop_id:
                STOP = 49
            else:
                STOP = p.t_stop_id
            if (post.t_start_id in range(p.t_start_id, STOP)
                or (p.t_start_id >= post.t_start_id
                    and post.t_stop_id >= STOP)
                or (p.t_start_id >= post.t_start_id
                    and post.t_stop_id in range(p.t_start_id + 1, STOP))
                or (STOP <= post.t_stop_id
                    and post.t_start_id in range(p.t_start_id, STOP - 1))):
                post.save()
                new_url = (
                    'http://virtual2025.oak.cc:8000/'
                    + request.user.username + '/'
                    + str(post.id) + '/'
                )
                url_user = User.objects.filter(id=p.author_id)
                if post.text[:3] == 'FIB':
                    data1 = post.text.split('(')[1][:-1]
                    data2 = p.text.split('(')[1][:-1]
                    if not set(data1.split(',')).isdisjoint(set(data2.split(','))):
                        preor_url = (
                            'http://virtual2025.oak.cc:8000/'
                            + url_user[0].username + '/'
                            + str(p.id) + '/'
                        )
                        confirm = {'new': words(post, p, new_url, preor_url, 'new'),
                                   'edit': words(post, p, new_url, preor_url, 'edit') }
                        mail_text = {'new': words(post, p, new_url, preor_url, 'm_new'),
                                     'edit': words(post, p, new_url, preor_url, 'm_edit') }
                        return ([mail_text[key], confirm[key]])
                else:
                    preor_url = (
                        'http://virtual2025.oak.cc:8000/'
                        + url_user[0].username + '/'
                        + str(p.id) + '/'
                    )
                    confirm = {
                        'new': words(post, p, new_url, preor_url, 'new'),
                        'edit': words(post, p, new_url, preor_url, 'edit'),
                    }
                    mail_text = {
                        'new': words(post, p, new_url, preor_url, 'm_new'),
                        'edit': words(post, p, new_url, preor_url, 'm_edit'),
                    }
                    return ([mail_text[key], confirm[key]])
    return "no_cross"


# Дмитрий Герасимов, Сергей Чадаев
def next_number(text, bm):
    '''Вспомогательная функция расчета следующего номера заявки'''
    curent_year = dt.datetime.today().strftime('%Y')
    slash = text.find('-')
    last_slash = text.rfind('-')
    text_year = text[(slash + 1):last_slash]
    bracet = text.find('(')
    if bracet != -1:
        number = text[(last_slash + 1):bracet]
    else:
        number = text[(last_slash + 1):]
    if bm == '_':
        bm = ''
    if int(curent_year) == int(text_year):
        return (
            text[:slash] + '-'
            + curent_year + '-'
            + str(int(number) + 1) + bm)
    else:
        return text[:slash] + '-' + curent_year + '-1' + bm


# Дмитрий Герасимов
def data_correct(post):
    '''Вспомогательная функция проверки корректности даты заявки'''
    time_start = dt.datetime.strptime(str(post.t_start), '%H:%M')
    # если заявка вчера+
    if post.day.date() < dt.datetime.now().date():
        return False
    # если заявка сегодня, но время старта раньше, чем время создания
    elif post.day.date() == dt.datetime.now().date():
        if post.group_id in range(4, 7):  # Для FIB, NUC, FIB BM
            # возможность создавать заявку в рамках уже идущего часа
            if str(time_start.time())[:2] < str(dt.datetime.now().time())[:2]:
                return False
        elif time_start.time() < dt.datetime.now().time():
            return False
    return True


@login_required
def fib_multi_plus(request, group_id, bm, post_id):

    post = Post.objects.filter(id=post_id)[0]
    data = post.text.split('(')[1][:-1]
    if data != "":
        fib_in = data.split(',')
    else:
        fib_in = []
    if bm in fib_in:
        if len(fib_in) > 1:
            fib_in.remove(bm)
            confirm = f'Из заявки {post.text} удален доступ к fib {bm}. '
        else:
            content = {'form': CommentForm(),
               'post': post,
               'day': str(post.day.date()),
               'author': User.objects.get(username=request.user.username),
               'comments': post.comments.all(),
               'dunger': cross_for_view(request, post) + ' В заявке должен быть хотя бы один блок!', }
            return render(request, 'post.html', {**content, **counts(request.user), **rights(request)})
    else:
        fib_in.append(bm)
        confirm = f'К заявке {post.text} добавлен fib {bm}. '
    text = post.text.split('(')[0] + '('
    all_in = 'FIB:'
    if len(fib_in) > 0:
        for fib in sorted(fib_in):
            text = text + fib + ','
            if  fib != 'MDU':
                all_in =  all_in + ' CPIOM' +  fib + ','
            else:
                all_in =  all_in + ' MDU' + ','
    else:
        all_in = 'FIB: стенд не выбран!'
        text = post.text.split('(')[0] + '(,'
    text = text[:-1] + ')'
    post.text = text
    post.all_in = all_in[:-1]
    post.save()
    return redirect('post', post.author, post.id)


@login_required
def post_new(request, group_id, bm):  # если bm = _, то обычный номер
    '''Функция создания заявки'''
    new = Post()
    new.group_id = group_id
    if group_id in range(3, 8):  # isib, fib, nuc, fib bm, fvb
        new.task_state_id = 2
    else:
        new.task_state_id = 1
    try:
        latest = str(Post.objects.filter(group_id=group_id).latest('id'))
        new.text = next_number(latest, bm)
        stend = Group.objects.filter(id=group_id).latest('id').title
    except Exception:
        stend = Group.objects.filter(id=group_id).latest('id').title
        if bm != '_':
            new.text = stend + '-' + str(dt.datetime.now().year) + '-1' + bm
        else:
            new.text = stend + '-' + str(dt.datetime.now().year) + '-1'

    confirm = ""
    if group_id == 4:  # fib
        if bm != '(MDU)':
            new.all_in = 'FIB: CPIOM' + bm[1:-1]
        else:
            new.all_in = 'FIB: ' + bm[1:-1]

    if group_id != 5:  # nuc
        form = PostForm(request.POST or None,
                        files=request.FILES or None,
                        instance=new)
    else:
        form = PostForm_nuc(request.POST or None,
                            files=request.FILES or None,
                            instance=new)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.pub_date = dt.datetime.now()
        post.t_start_html = post.t_start_id * 2 - 2
        post.t_stop_html = (post.t_stop_id - post.t_start_id) * 2
        post.day += dt.timedelta(hours=3)
        # если выбранная дата некорректна ################################
        if not data_correct(post):
            stend = stend + words(post, post, '', '', 'wrong_date')
            content = {'form': form, 'stend': stend, 'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights(request)})
        # если выбранный интервал времени некорректен ####################
        if int(post.t_start_id) == int(post.t_stop_id) or post.t_start_id == 49 or post.t_stop_id == 1:
            stend = stend + words(post, post, '', '', 'wrong_time')   
            content = {'form': form, 'stend': stend, 'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights(request)})
        #####################################################################
        if post.group_id == 5:
            post.testers = '-'
            post.test_object = '-'
            post.purpose = '-'
            post.reason = '-'
            post.configuration = '-'
            post.instruments = '-'
            post.add_requirements = '-'
            post.doc = '-'
        #####################################################################
        post.save()
        print(post.day)
        url = ('http://virtual2025.oak.cc:8000/' + request.user.username +
               '/' + str(post.id) + '/')
        confirm = words(post, post, url, '', 'confirm')
        if post.group_id in range(4, 7):
            mail(request.user.email, [], post.text + " создана.", confirm)
        else:
            mail(request.user.email, settings.RIGHTS, post.text + " создана.", confirm)
        return redirect('post', post.author, post.id)
    content = {'form': form, 'stend': stend, 'confirm': confirm, }
    return render(request, 'new_post.html', {**content, **rights(request)})


@login_required
def post_new_one(request, stend_id, start_id, day):
    buttons = {}
    sib = {'SIB': '_', }
    acib = {'ACIB': '_', }
    isib = {
        'ISIB (Без БМ)': '_',
        'ISIB (+ БМ1)': '(БМ1)',
        'ISIB (+ БМ2)': '(БМ2)',
        'ISIB (+ БМ3)': '(БМ3)',
    }
    fib = {
        'FIB CPIOM 1': '(1)',
        'FIB CPIOM 2': '(2)',
        'FIB CPIOM 3': '(3)',
        'FIB CPIOM 4': '(4)',
        'FIB CPIOM 5': '(5)',
        'FIB MDU': '(MDU)',
    }
    nuc = {
        'NUC227 (ABSINT)': '(227)',
        'NUC237': '(237)',
        'NUC238': '(238)',
        'NUC239': '(239)',
    }
    fib_bm = {
        'FIB BM Linux': '(Linux)',
        'FIB BM Windows': '(Windows)',
    }
    fvb = {
        'FVB 3': '(3)',
        'FVB 4': '(4)',
        'FVB 5': '(5)',
        'FVB 7': '(7)',
    }

    all_buttons = {1: sib, 2: acib, 3: isib, 4: fib, 5: nuc, 6: fib_bm, 7: fvb, }
    if stend_id == 1 or stend_id == 2:
        return redirect('post_new_from_table', stend_id, '_', start_id, day)
    elif stend_id in range(3, 8):
        buttons = {**all_buttons[stend_id]}

    content = {
        'buttons': buttons,
        'g_id': stend_id,
        'start_id': start_id,
        'day': day,
        'all_buttons': all_buttons,
    }
    return render(request, 'new_post_one.html', {**content, **rights(request)})


@login_required
def post_new_from_table(request, group_id, bm, start_id, day):  # если bm = _, то обычный номер
    '''Функция создания заявки'''
    new = Post()
    new.group_id = group_id
    new.t_start_id = start_id
    new.t_stop_id = 49
    new.day = day

    if group_id in range(3,8):  # isib, fib, nuc, fib bm, fvb
        new.task_state_id = 2
    else:
        new.task_state_id = 1
    try:
        latest = str(Post.objects.filter(group_id=group_id).latest('id'))            
        new.text = next_number(latest, bm)
        stend = Group.objects.filter(id=group_id).latest('id').title
    except Exception as e:
        stend = Group.objects.filter(id=group_id).latest('id').title
        if bm != '_':
            new.text = stend + '-' + str(dt.datetime.now().year) + '-1' + bm
        else:
            new.text = stend + '-' + str(dt.datetime.now().year) + '-1'
    
    confirm = ""
    if group_id == 4:  # fib
        if bm != '(MDU)':
            new.all_in = 'FIB: CPIOM' + bm[1:-1]
        else:
            new.all_in = 'FIB: ' + bm[1:-1]
    
    if group_id != 5:  # nuc
        form = PostForm(request.POST or None,
                        files=request.FILES or None,
                        instance=new)
    else:
        form = PostForm_nuc(request.POST or None,
                            files=request.FILES or None,
                            instance=new)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.pub_date = dt.datetime.now()
        post.t_start_html = post.t_start_id * 2 - 2
        post.t_stop_html = (post.t_stop_id - post.t_start_id) * 2
        post.day += dt.timedelta(hours=3)
        # если выбранная дата некорректна ################################
        if not data_correct(post):
            stend = stend + words(post, post, '', '', 'wrong_date')
            content = {'form': form, 'stend': stend, 'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights(request)})
        # если выбранный интервал времени некорректен ####################
        if int(post.t_start_id) == int(post.t_stop_id) or post.t_start_id == 49 or post.t_stop_id == 1:
            stend = stend + words(post, post, '', '', 'wrong_time')   
            content = {'form': form, 'stend': stend, 'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights(request)})
        #####################################################################
        if post.group_id == 5:
            post.testers = '-'
            post.test_object = '-'
            post.purpose = '-'
            post.reason = '-'
            post.configuration = '-'
            post.instruments = '-'
            post.add_requirements = '-'
            post.doc = '-'
        #####################################################################
        post.save()
        url = ('http://virtual2025.oak.cc:8000/' + request.user.username +
               '/' + str(post.id) + '/')
        confirm = words(post, post, url, '', 'confirm')
        if post.group_id in range(4, 8):
            mail(request.user.email, [], post.text + " создана.", confirm)
        else:
            mail(request.user.email, settings.RIGHTS, post.text + " создана.", confirm)
        return redirect('post', post.author, post.id)
    content = {'form': form, 'stend': stend, 'confirm': confirm, }  
    return render(request, 'new_post.html', {**content, **rights(request)})


@login_required
def post_edit(request, username, post_id):
    '''Функция редактирования заявки'''
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    post.day = str(post.day)[:-15]
    stend = Group.objects.filter(id=post.group_id).latest('id').title
    confirm = ""
    if request.user != post.author:
        if request.user.username not in settings.RIGHTS:
            return redirect('post', username, post_id)
    if post.group_id != 5:
        form = PostForm(request.POST or None,
                        files=request.FILES or None,
                        instance=post)
    else:
        form = PostForm_nuc(
            request.POST or None,
            files=request.FILES or None,
            instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        if post.group_id in range(3,8):  # isib, fib, nuc, fib bm, fvb
            post.task_state_id = 2
        else:
            post.task_state_id = 1
        post.t_start_html =  post.t_start_id * 2 - 2
        post.t_stop_html = (post.t_stop_id - post.t_start_id) * 2
        post.day += dt.timedelta(hours=3)
        # если выбранная дата некорректна ################################
        if not data_correct(post):
            stend = stend + words(post, post, '', '', 'wrong_date')
            content = {'form': form, 'post': post, 'edit': True, 'stend': stend,
                       'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights(request)})
        # если выбранный интервал времени некорректен ####################
        if int(post.t_start_id) == int(post.t_stop_id) or post.t_start_id == 49 or post.t_stop_id == 1:
            stend = stend + words(post, post, '', '', 'wrong_time')
            content = {'form': form, 'post': post, 'edit': True, 'stend': stend,
                       'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights(request)})
        #####################################################################
        post.save()
        url = ('http://virtual2025.oak.cc:8000/' + request.user.username +
               '/' + str(post.id) + '/')
        if post.group_id in range(4, 8):
            mail(request.user.email, [], post.text + " изменена.", url)
        else:
            mail(request.user.email, settings.RIGHTS, post.text + " изменена.", url)
        return redirect('post', post.author, post.id)
    content = {'form': form, 'post': post, 'edit': True, 'stend': stend,
               'month': str(YEAR) + "-" + str(MONTH),'confirm': confirm, }
    return render(request, 'new_post.html', {**content, **rights(request)})


@login_required
def post_copy(request, username, post_id):
    '''Функция создания заявки из шаблона'''
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    post.day = str(post.day)[:-15]
    stend = Group.objects.filter(id=post.group_id).latest('id').title
    new = Post()
    confirm = ""
    latest = str(Post.objects.filter(group_id=post.group_id).latest('id'))
    if post.text.find('(') != -1:
        new.text = next_number(latest, post.text[post.text.find('('):])
    else:
        new.text = next_number(latest, "_")
    new.author = post.author
    new.group = post.group
    new.file = post.file
    new.day = post.day
    new.t_stop = post.t_stop
    new.t_start = post.t_start
    new.testers = post.testers
    new.unit = post.unit
    new.purpose = post.purpose
    new.reason = post.reason
    new.test_object = post.test_object
    new.configuration = post.configuration
    new.instruments = post.instruments
    new.add_requirements = post.add_requirements
    new.doc = post.doc
    new.all_in = post.all_in  # лишняя строчка?
    if new.group_id in range(3, 8):  # isib, fib, nuc, fib bm
        new.task_state_id = 2
    else:
        new.task_state_id = 1
    if request.user != post.author:
        if request.user.username not in settings.RIGHTS:
            return redirect('post', username, post_id)
    if post.group_id != 5:
        form = PostForm(request.POST or None,
                        files=request.FILES or None,
                        instance=new)
    else:
        form = PostForm_nuc(
            request.POST or None,
            files=request.FILES or None,
            instance=new)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.pub_date = dt.datetime.now()
        post.t_start_html = post.t_start_id * 2 - 2
        post.t_stop_html = (post.t_stop_id - post.t_start_id) * 2
        post.day += dt.timedelta(hours=3)
        # если выбранная дата некорректна ################################
        if not data_correct(post):
            stend = stend + words(post, post, '', '', 'wrong_date')
            content = {'form': form, 'post': post, 'edit': False, 'stend': stend,
                       'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights(request)})
        # если выбранный интервал времени некорректен ####################
        if int(post.t_start_id) == int(post.t_stop_id) or post.t_start_id == 49 or post.t_stop_id == 1:
            stend = stend + words(post, post, '', '', 'wrong_time')
            content = {'form': form, 'post': post, 'edit': False, 'stend': stend,
                       'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights(request)})
        #####################################################################
        post.save()
        url = ('http://virtual2025.oak.cc:8000/' + request.user.username +
               '/' + str(post.id) + '/')
        confirm = words(post, post, url, '', 'confirm')
        if post.group_id in range(4, 8):
            mail(request.user.email, [], post.text + " создана.", confirm)
        else:
            mail(request.user.email, settings.RIGHTS, post.text + " создана.", confirm)
        return redirect('post', post.author, post.id)
    content = {'form': form, 'post': post, 'edit': False, 'stend': stend,
               'confirm': confirm, }
    return render(request, 'new_post.html', {**content, **rights(request)})


@login_required
def post_delete(request, username, post_id):
    '''Функция удаления заявки'''
    author = User.objects.get(username=username)
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    if request.user != post.author:
        if request.user.username not in settings.RIGHTS:
            return redirect('profile', username)
    if post.task_state_id == 1 or post.task_state_id == 4:
        mail_text = (f"Заявка {post.text} удалена.")
        mail(author.email, settings.RIGHTS, post.text + " удалена.", mail_text)
        post.delete()
    return redirect('profile', username)


@login_required
def add_comment(request, username, post_id):
    """Добавление комментария"""
    post = get_object_or_404(Post, id=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("post", username, post_id)


@login_required
def add_feedback(request):
    """Добавление предложения"""
    form = FeedbackForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        feedback = form.save(commit=False)
        print(feedback.image)
        feedback.author = request.user
        feedback.save()
        
    return redirect("feedbacks")


@login_required
def feedbacks(request):
    feedbacks = Feedback.objects.all()
    for fb in feedbacks:
        new_word = ""
        for word in fb.text.split():
            if len(word) > 60:
                for i in range(1, len(word) // 60 + 2):   
                    new_word += word[60 * (i - 1):60 * i] + " "
            else:
                new_word += word + " "
        fb.text = new_word[:-1]

    paginator = Paginator(feedbacks, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    dis = []
    for obj in Dislike.objects.all():
        if request.user.id == obj.user_id:
            dis.append(obj.feedback_id)
    likes = []
    for obj in Like.objects.all():
        if request.user.id == obj.user_id:
            likes.append(obj.feedback_id)

    content = {
        'dis': dis,
        'likes': likes,
        'page': page,
        'form': FeedbackForm()
    }
    return render(request, 'feedback.html', {**content, **rights(request)})


@login_required
def delete_feedback(request, feedback_id):
    """Функция удаления предложения"""
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if (
        feedback.author == request.user
        or request.user.username in settings.RIGHTS
    ):
        try:
            os.remove(settings.MEDIA_ROOT + feedback.image.url)
            print(f'Файл {settings.MEDIA_ROOT + feedback.image.url} успешно удален')
        except:
            print(f'Не удалось удалить файл {settings.MEDIA_ROOT + "/" + feedback.image.url}')
        feedback.delete()
        
    return redirect("feedbacks")


@login_required
def add_like(request, feedback_id, user_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    likes = Like.objects.filter(feedback_id=feedback_id, user_id=user_id)
    if likes.count() == 0:
        feedback.likes += 1
        like = Like()
        like.feedback_id = feedback_id
        like.user_id = user_id
        like.save()
        dislike = Dislike.objects.filter(
            feedback_id=feedback_id,
            user_id=user_id,
        )
        if dislike.count() > 0:
            for dis in dislike:
                dis.delete()
            feedback.dislikes -= 1
    else:
        for like in likes:
            like.delete()
        feedback.likes = Like.objects.filter(feedback_id=feedback_id).count()
    feedback.save()
    return redirect("feedbacks")


@login_required
def add_dislike(request, feedback_id, user_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    dislike = Dislike.objects.filter(feedback_id=feedback_id, user_id=user_id)
    if dislike.count() == 0:
        feedback.dislikes += 1
        dis = Dislike()
        dis.feedback_id = feedback_id
        dis.user_id = user_id
        dis.save()
        likes = Like.objects.filter(feedback_id=feedback_id, user_id=user_id)
        if likes.count() > 0:
            for like in likes:
                like.delete()
            feedback.likes -= 1
    else:
        for dis in dislike:
            dis.delete()
        feedback.dislikes = Dislike.objects.filter(feedback_id=feedback_id).count()
    feedback.save()

    feedbacks = Feedback.objects.all()
    content = {'feedbacks': feedbacks, 'form': FeedbackForm(),}
    return redirect("feedbacks")


@login_required
def delete_comment(request, username, post_id, comment_id):
    """Удаление комментария"""
    comment = get_object_or_404(Comment, id=comment_id, post=post_id)
    if comment.author == request.user:
        comment.delete()
    return redirect("post", username, post_id)


def profile_state(request, username, state_id: int):
    """Фильтрация заявок сотрудника по статусу"""
    author = get_object_or_404(User, username=username)
    all_posts = author.posts.filter(task_state_id=state_id) #
    paginator = Paginator(all_posts, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    content = {'author': author, 'page': page, }
    return render(request, 'profile.html', {**content, **counts(author), **rights(request)})


def server_error(request):
    return render(request, "misc/500.html", status=500)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    return render(request, "misc/404.html",{"path": request.path},status=404)

#
def help(request):
    '''Страница с инструкцией'''
    wk = dt.datetime.strptime(str(dt.datetime.now().date()),
                              '%Y-%m-%d').isocalendar()[1]
    return render(request, 'help.html',
                  {**rights(request),
                   'day': str(dt.date.today()),
                   'wk': str(dt.datetime.now().date().year) + '-' + str(wk),
                   'month': str(dt.datetime.now().date().year) + "-" + str(dt.datetime.now().date().month)})


def rele_isib(request):
    return render(request, 'rele_isib.html', {**rights(request), })

def rele_isib_cold(request):
    return render(request, 'rele_isib_cold.html', {**rights(request), })

def rele_fib(request):
    return render(request, 'rele_fib.html', {**rights(request), })

def rele_on_off(request, IP, rele_number, state):
    ips = {'1': '10.1.98.247', # fake IP : real IP
           '10.1.98.248': '10.1.98.248',
           '10.1.98.249': '10.1.98.249',} 
    '''Вспомогательная функция запроса на вкл/выкл реле'''
    if state == 'on':
        requests.get(
            'http://admin:admin@' + ips[IP] + '/protect/rb'+ rele_number + 'n.cgi',
            verify=False,
            timeout=10)
    else:
        requests.get(
            'http://admin:admin@' + ips[IP] + '/protect/rb'+ rele_number + 'f.cgi',
            verify=False,
            timeout=10)

    if IP == '10.1.98.249':
        return render(request, 'rele_isib.html', {**rights(request), })
    elif IP == '10.1.98.248':
        return render(request, 'rele_isib_cold.html', {**rights(request), })
    elif IP == '1':
        return render(request, 'rele_fib.html', {**rights(request), })


rele_cold = {'БМ1':'0', 'БМ2':'1', 'БМ3':'2', }
how_many = {'БМ1': 0, 'БМ2': 0, 'БМ3': 0, }
how_many_bm = set()
IP_fib = '10.1.98.247'
IP_cold = '10.1.98.248'
IP = "10.1.98.249"
no_signal = {'isib': 0, 'cold_isib': 0, 'fib': 0,}


@background(schedule=5)
def hello_world():
    UDP_IP = "10.1.98.46"
    UDP_PORT = 5500

    try:
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        time_as_dt = dt.datetime.now()
        time_as_bytes = str.encode(str(time_as_dt))
        sock.sendto(time_as_bytes, (UDP_IP, UDP_PORT))
    except Exception:
        print('lol')

    '''Функция работы с управляемым реле'''
    rele = {
        'БМ1_1': '0', 'БМ1_2': '1',
        'БМ2_1': '2', 'БМ2_2': '3',
        'БМ3_1': '4', 'БМ3_2': '5',
    }
    rele_fib = {
        'FIB_1': '0',
        'FIB_2': '1',
        'FIB_3': '2',
        'FIB_4': '3',
        'FIB_5': '4',
    }

    today_recs = {
        'all': [], 'future': [], 'now': [], 'over': [],
        'БМ1': [], 'БМ2': [], 'БМ3': [],
        'FIB_1': [], 'FIB_2': [], 'FIB_3': [], 'FIB_4': [], 'FIB_5': [],
        'FIB_MDU': [],
    }
    today = dt.datetime.now()
    groups = [3, 4]

    day_for_search = str(today.date()) + ' 00:00:00+00:00'

    previos_day = today.date() - dt.timedelta(days=1)
    previos_day_for_search = str(previos_day) + ' 00:00:00+00:00'
    previos_day_post_list = Post.objects.filter(
        day=previos_day_for_search,  # previos_day
        task_state_id=2,
        group__in=groups,
    )
    today_post_list = Post.objects.filter(
        day=day_for_search,  # today.date(),
        task_state_id=2,
        group__in=groups,  # fib group=4
    )
    print('_' * 72)
    # Если заявки на сегодня есть,
    if len(today_post_list) != 0:
        for rec in today_post_list:
            bracet = rec.text.find('(')
            if bracet != -1:
                today_recs['all'].append(rec)
    if len(previos_day_post_list) != 0:
        for rec in previos_day_post_list:
            if rec.t_start_id >= rec.t_stop_id:
                bracet = rec.text.find('(')
                if bracet != -1:
                    today_recs['all'].append(rec)

    # Если заявки на ISIB + БМ сегодня есть,
    if len(today_recs['all']) != 0:
        # Распределение заявок - ожидается | в процессе | завершена
        today_now_minutes = today.hour * 60 + today.minute
        print('Заявки на сегодня:')
        for rec in today_recs['all']:
            rec_start_hour = str(rec.t_start).split(':')[0]
            rec_start_minute = str(rec.t_start).split(':')[1]
            rec_start_full = int(rec_start_hour) * 60 + int(rec_start_minute)

            rec_stop_hour = str(rec.t_stop).split(':')[0]
            rec_stop_minute = str(rec.t_stop).split(':')[1]
            rec_stop_full = int(rec_stop_hour) * 60 + int(rec_stop_minute)

            difference_start_min = rec_start_full - today_now_minutes
            difference_stop_min = rec_stop_full - today_now_minutes
            print(rec.text, ': ', rec.t_start, ' - ', rec.t_stop, end="")
            if rec_start_full >= rec_stop_full:
                if rec.day.date() == today.date():
                    if 15 >= difference_start_min >= 0:
                        print(". До начала работ менее 15 минут.")
                        today_recs['now'].append(rec)
                    elif difference_start_min < 0:
                        print(". В работе.")
                        today_recs['now'].append(rec)
                    else:  # if difference_start_min > 15:
                        print(". До начала работ более 15 минут.")
                        today_recs['future'].append(rec)
                else:
                    if difference_stop_min <= -30:
                        print(". Завершена.")
                        today_recs['over'].append(rec)
                    else:
                        print(". В работе.")
                        today_recs['now'].append(rec)
            else:
                if 15 >= difference_start_min >= 0:
                    print(". До начала работ менее 15 минут.")
                    today_recs['now'].append(rec)
                elif difference_start_min < 0:
                    if difference_stop_min <= -30:
                        print(". Завершена.")
                        today_recs['over'].append(rec)
                    else:
                        print(". В работе.")
                        today_recs['now'].append(rec)
                else:  # if difference_start_min > 15:
                    print(". До начала работ более 15 минут.")
                    today_recs['future'].append(rec)
        how_many_bm.clear()
        for rec in today_recs['now']:
            if rec.text.split('(')[1][:-1] == 'БМ1':
                today_recs['БМ1'].append(rec)
                how_many_bm.add('БМ1')
            elif rec.text.split('(')[1][:-1] == 'БМ2':
                today_recs['БМ2'].append(rec)
                how_many_bm.add('БМ2')
            elif rec.text.split('(')[1][:-1] == 'БМ3':
                today_recs['БМ3'].append(rec)
                how_many_bm.add('БМ3')
            else:
                fib_rec = rec.text.split('(')[1][:-1]  # '1,2,3,4,5'
                if fib_rec != '':
                    for r in fib_rec.split(','):
                        today_recs['FIB_' + r].append(rec)
    print('_' * 72)
    # Работа с управляемым реле
    rele_now(today_recs['БМ1'], rele['БМ1_1'], rele['БМ1_2'], 'БМ1')
    rele_now(today_recs['БМ2'], rele['БМ2_1'], rele['БМ2_2'], 'БМ2')
    rele_now(today_recs['БМ3'], rele['БМ3_1'], rele['БМ3_2'], 'БМ3')
    for fib in rele_fib.keys():
        fib_rele_now(today_recs[fib], rele_fib[fib], fib)
    cold_check(today_recs)
    print(today, ' : следующий запрос через 10 минут')
    time.sleep(600)
    # python manage.py process_tasks


def rele_now(recs, number1, number2, bm):
    '''Вспомогательная функция включения/отключения реле'''
    if len(recs) == 0:
        try:
            print(f"Заявок в работе на {bm} - {len(recs)} \n"
                  f"Если питание на {bm} не выключено, то необходимо выключить")
            if rele_state(number1, IP, 'isib') == '1' or rele_state(number2, IP, 'isib') == '1':
                print('Сейчас питание не выключено')
                res = on_off(IP, number1, 'off')
                res = on_off(IP, number2, 'off')
                if rele_state(number1, IP, 'isib') == '0' and rele_state(number2, IP, 'isib') == '0':
                    print('Теперь питание выключено')
            print('_' * 72)
        except Exception as e:
            print("Реле недоступно -", e)
            rele_no_unswer('isib')
    else:
        try:
            print(f"Заявок в работе на {bm} - {len(recs)} \n"
                  f"Если питание на {bm} не включено, то необходимо включить")
            if rele_state(number1, IP, 'isib') == '0'or rele_state(number2, IP, 'isib') == '0':
                print('Сейчас питание не включено')
                res = on_off(IP, number1, 'on')
                res = on_off(IP, number2, 'on')
                if rele_state(number1, IP, 'isib') == '1'and rele_state(number2, IP, 'isib') == '1':
                    print('Теперь питание включено')
            print('_' * 72)
        except Exception as e:
            print("Реле недоступно -", e)
            rele_no_unswer('isib')


def fib_rele_now(recs, number, fib):
    '''Вспомогательная функция включения/отключения реле'''
    if len(recs) == 0:
        try:
            print(f"Заявок в работе на {fib} - {len(recs)} \n"
                  f"Если питание на {fib} не выключено, то необходимо выключить")
            if rele_state(number, IP_fib, 'fib') == '1':
                print('Сейчас питание не выключено')
                res = on_off(IP_fib, number, 'off')
                if rele_state(number, IP_fib, 'fib') == '0':
                    print('Теперь питание выключено')
            print('_' * 72)
        except Exception as e:
            print("Реле недоступно -", e)
            rele_no_unswer('fib')
    else:
        try:
            print(f"Заявок в работе на {fib} - {len(recs)} \n"
                  f"Если питание на {fib} не включено, то необходимо включить")
            if rele_state(number, IP_fib, 'fib') == '0':
                print('Сейчас питание не включено')
                on_off(IP_fib, number, 'on')
                if rele_state(number, IP_fib, 'fib') == '1':
                    print('Теперь питание включено')
            print('_' * 72)
        except Exception as e:
            print("Реле недоступно -", e)
            rele_no_unswer('fib')


def state(IP):
    '''Вспомогательная функция получения статуса всех реле'''
    return requests.get(
        'http://admin:admin@' + IP + '/pstat.xml',
        verify=False,
        timeout=10)


def on_off(IP, rele_number, state):
    '''Вспомогательная функция запроса на вкл/выкл реле'''
    if state == 'on':
        return requests.get(
            'http://admin:admin@' + IP + '/protect/rb' + rele_number + 'n.cgi',
            verify=False,
            timeout=10)
    return requests.get(
        'http://admin:admin@' + IP + '/protect/rb' + rele_number + 'f.cgi',
        verify=False,
        timeout=10)


def rele_state(number, IP, rele_key):
    '''Вспомогательная функция получения статуса реле'''
    try:
        res = state(IP)
        rele_state = re.findall(
            r'[<][r][l][' + number + '][s][t][r][i][n][g][>].',
            str(res.content))[0][-1:]
        if rele_state == 1:
            print(f'Статус реле №{number}: Вкл.')
        elif rele_state == 0:
            print(f'Статус реле №{number}: Выкл.')
        return rele_state
    except Exception as e:
        print(f'Статус реле №{number}: Реле недоступно.', e)
        rele_no_unswer(rele_key)
        return '-1'


def cold_check(recs):
    '''Вспомогательная функция опроса статуса вентиляторов'''
    if len(recs['БМ1']) == 0:
        how_many_times('БМ1', '0')
    else:
        if how_many_times('БМ1', '+1') == 6:
            for key in how_many.keys():
                how_many[key] = 0
            return

    if len(recs['БМ2']) == 0:
        how_many_times('БМ2', '0')
    else:
        if how_many_times('БМ2', '+1') == 6:
            for key in how_many.keys():
                how_many[key] = 0
            return

    if len(recs['БМ3']) == 0:
        how_many_times('БМ3', '0')
    else:
        if how_many_times('БМ3', '+1') == 6:
            for key in how_many.keys():
                how_many[key] = 0
            return


def how_many_times(bm: str, value: str):
    if value == '+1':
        how_many[bm] += 1
        print(f'Количество опросов {bm} - {how_many[bm]}')
        # если вентилятор ВКЛ, то ВЫКЛ
        if_on_then_off(bm, rele_cold[bm], IP_cold)

        if how_many[bm] == 6:
            print('ВКЛЮЧАЕМ ВЕНТИЛЯТОРЫ...')
            for b_m in how_many_bm:
                print(b_m)
                # если вентилятор ВЫКЛ, то ВКЛ
                if_off_then_on(b_m, rele_cold[b_m], IP_cold)        
    else:
        how_many[bm] = 0
        print(f'Количество опросов {bm} - {how_many[bm]}')
        # если вентилятор ВКЛ, то ВЫКЛ
        if_on_then_off(bm, rele_cold[bm], IP_cold)
    print('_' * 72)
    return how_many[bm]


def if_on_then_off(bm, rele_number, IP):
    # если вентилятор ВКЛ, то ВЫКЛ
    try:
        print(
            (f"Если питание вентилятора на {bm} не выключено,"
             f"то необходимо выключить")
        )
        if rele_state(rele_number, IP, 'cold_isib') == '1':
            print('Сейчас питание не выключено')
            on_off(IP, rele_number, 'off')
            if rele_state(rele_number, IP, 'cold_isib') == '0':
                print('Теперь питание выключено')
    except Exception as e:
        print("Реле недоступно -", e)
        rele_no_unswer('cold_isib')


def if_off_then_on(bm, rele_number, IP):
    # если вентилятор ВЫКЛ, то ВКЛ
    try:
        print(
            (f"если питание вентилятора на {bm} не включено,"
             f"то необходимо включить")
        )
        if rele_state(rele_number, IP, 'cold_isib') == '0':
            print('Сейчас питание не включено')
            on_off(IP, rele_number, 'on')
            if rele_state(rele_number, IP, 'cold_isib') == '1':
                print('Теперь питание включено')
    except Exception as e:
        print("Реле недоступно -", e)
        rele_no_unswer('cold_isib')


def rele_no_unswer(rele_key):
    """Функция - счетчик отсутствия ответов реле"""
    if no_signal[rele_key] == 0:
        mail('nikolay.emelyanov@ic.irkut.com',
             settings.RIGHTS,
             f"Реле на {rele_key}",
             f"Реле на {rele_key} недоступно")
    no_signal[rele_key] += 1
    if no_signal[rele_key] == 100:
        no_signal[rele_key] = 0


def statistic(request):
    month = dt.datetime.now().month
    year = dt.datetime.now().year    
    days = monthrange(year, month)[1]
    day_start_num = date(year, month, 1)
    end_date = date(year, month, days) + timedelta(1)
    post_list = Post.objects.filter(
        day__range=[day_start_num, end_date],
        task_state_id=2,
    )

    sib, acib, isib = [], [], []

    for item in post_list:
        if item.group_id == 1:
            sib.append(item)
        elif item.group_id == 2:
            acib.append(item)
        elif item.group_id == 3:
            isib.append(item)

    count = len(post_list)
    count_sib = len(sib)
    count_acib = len(acib)
    count_isib = len(isib)

    sib_days = {}
    sib_results = []
    sib_month = 0
    if len(sib) > 0:
        for item in sib:
            if item.day not in sib_days.keys():
                sib_days[item.day] = []
            sib_days[item.day].append(item)

        result = 0
        day_work_time = 9
        sib_results = sib_days
        for key in sib_days.keys():
            for item in sib_days[key]:
                result += (item.t_stop_id - item.t_start_id) / 2
            sib_results[key] = round(result / day_work_time, 2)
            result = 0

        for key in sib_results.keys():
            sib_month += sib_results[key]
        sib_month = round(sib_month / len(sib_results.keys()), 2)

    acib_days = {}
    acib_results = []
    acib_month = 0
    if len(acib) > 0:
        for item in acib:
            if item.day not in acib_days.keys():
                acib_days[item.day] = []
            acib_days[item.day].append(item)

        acib_results = []
        result = 0
        day_work_time = 9
        acib_results = acib_days
        for key in acib_days.keys():
            for item in acib_days[key]:
                result += (item.t_stop_id - item.t_start_id) / 2
            acib_results[key] = round(result / day_work_time, 2)
            result = 0
        acib_month = 0
        for key in acib_results.keys():
            acib_month += acib_results[key]
        acib_month = round(acib_month / len(acib_results.keys()), 2)

    isib_days = {}
    isib_results = []
    isib_month = 0
    if len(isib) > 0:
        for item in isib:
            if item.day not in isib_days.keys():
                isib_days[item.day] = []
            isib_days[item.day].append(item)

        isib_results = []
        result = 0
        day_work_time = 9
        isib_results = isib_days
        for key in isib_days.keys():
            for item in isib_days[key]:
                result += (item.t_stop_id - item.t_start_id) / 2
            isib_results[key] = round(result / day_work_time, 2)
            result = 0
        isib_month = 0
        for key in isib_results.keys():
            isib_month += isib_results[key]
        isib_month = round(isib_month / len(isib_results.keys()), 2)
    content = {
        'count': count,
        'count_sib': count_sib,
        'count_acib': count_acib,
        'count_isib': count_isib,
        'sib_results': sib_results,
        'sib_month': sib_month,
        'acib_results': acib_results,
        'acib_month': acib_month,
        'isib_results': isib_results,
        'isib_month': isib_month,
    }
    return render(
        request, 'statistic.html', {**content, **rights(request), }
    )

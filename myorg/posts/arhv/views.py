import datetime as dt
import subprocess
import os
import requests
import re
#import win32com.client as win32
import pythoncom
import time
from datetime import timedelta, date
from calendar import monthrange
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse
#from django.views.decorators.cache import cache_page
from background_task import background

from .forms import PostForm, PostForm_nuc, CommentForm, FeedbackForm
from .models import Comment, Follow, Group, Post, User, Feedback, Like, Dislike

#IP = "192.168.1.11"
IP = "10.1.98.249"
MONTH = dt.datetime.now().date().month
YEAR = dt.datetime.now().date().year
dayz = {'0': 'Понедельник',
        '1': 'Вторник',
        '2': 'Среда',
        '3': 'Четверг',
        '4': 'Пятница',
        '5': 'Суббота',
        '6': 'Воскресенье', }

rights = {'rights': settings.RIGHTS,
          'storage_rights': settings.STORAGE_RIGHTS,
          'sadec_rights': settings.SADEC_RIGHTS,
          'pro_rights': settings.PRO_RIGHTS, }


# @cache_page(20)
def index(request):
    '''Календарь всех заявок - стартовая страница'''
    data_check = {}
    post_list = Post.objects.filter(task_state_id=2,)[:100]
    for post in post_list:
        key = str(post.day)[0:10] + ", " + str(dayz[str(post.day.weekday())])
        if key not in data_check.keys():
            data_check[key] = [] 
        data_check[key].append(post)
    content = {'data_check': data_check, 'day': str(dt.date.today()),}
    return render(request, 'index.html', {**content, **rights})


def day(request, day):
    '''Календарь на день'''
    data_check = {}
    post_list = Post.objects.filter(day=day, task_state_id=2)
    if len(post_list) > 0:
        data_check[str(day)] = post_list.order_by('-t_start')
    content = {'data_check': data_check, 'day': str(day), }
    return render(request, "follow.html", {**content, **rights})


def week(request, wk):  # не отображает все события переходной недели из года в год
    '''Календарь на неделю'''
    data_check = {}
    year = int(wk[0:4])
    wk = int(wk[5:])
    post_list = Post.objects.filter(day__week=wk,
                                    day__year=year,  # вот почему
                                    task_state_id=2).order_by('-day', '-t_start')
    for post in post_list:
        key = (str(post.day)[0:10] + ", " +
               str(dayz[str(post.day.weekday())]))
        if key not in data_check.keys():
            data_check[key] = [] 
        data_check[key].append(post)
    content = {'data_check': data_check,
               'day': str(dt.date.today()),
               'wk': str(year) + '-' + str(wk), }
    return render(request, 'week.html', {**content, **rights})


def month(request, month):
    '''Каленгдарь на месяц'''
    data_check = {}
    year = int(month[0:4])
    month = int(month[5:])
    day_start_num = monthrange(year, month)[0]
    day_start_num_for_html = day_start_num*2
    days = monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, days) + timedelta(1)
    data_by_weeks = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{},}
    key_of_week = 0
    
    day_before = start_date - timedelta(day_start_num)
    day_after_num = (day_start_num + days - 1)%7
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
                                    task_state_id=2)
    for post in post_list:
        key = str(post.day)[0:10] + ", " + str(dayz[str(post.day.weekday())])
        if key in data_check.keys():
            data_check[key].append(post)
        for k in data_by_weeks.keys():
            if key in data_by_weeks[k].keys():
                data_by_weeks[k][key].append(post)
                break            
    content = {'data_check': data_check,
               'data_by_weeks': data_by_weeks,
               'day': str(dt.datetime.now().date()),
               'month': str(year) + "-" + str(month),
               'day_start_num_for_html': day_start_num_for_html, }
    return render(request, 'month.html', {**content, **rights})


def stend(request, group_id):
    '''Календарь стенда'''
    data_check = {}
    post_list = Post.objects.filter(group=group_id, task_state_id=2).order_by('-day', '-t_start')[:100]
    for post in post_list:
        key = str(post.day)[0:10] + ", " + str(dayz[str(post.day.weekday())])
        if key not in data_check.keys():
            data_check[key] = [] 
        data_check[key].append(post)
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
    return render(request, 'index.html', {**content, **rights})


def stend_filtr(request, group_id, filtr):
    '''Календарь стенда'''
    data_check = {}
    post_list = Post.objects.filter(group=group_id, task_state_id=2).order_by('-day', '-t_start')[:100]
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
                    if key not in data_check.keys():
                        data_check[key] = []
                    if post not in data_check[key]:
                        data_check[key].append(post)
        else:
            fib_in = []

    
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
    return render(request, 'index.html', {**content, **rights})


def counts(group):  # group/author
    '''Вспомогательная функция для вычисления кол-ва типовых заявок'''
    counts = {'count': group.posts.all().count(),
              'count_new': group.posts.filter(task_state_id=1).count(),
              'count_in_progr': group.posts.filter(task_state_id=2).count(),
              'count_postponed': group.posts.filter(task_state_id=4).count(),
              'count_finished': group.posts.filter(task_state_id=3).count(), }
    return counts


def group_posts(request, slug):
    '''Список задач стенда'''
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    content = {"group": group, 'page': page,}
    return render(request, "group.html", {**content, **counts(group), **rights})


def group_posts_states(request, slug, state_id: int):
    '''Список фильтрованых задач стенда'''
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.filter(task_state_id=state_id)
    paginator = Paginator(posts, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    content = {"group": group, 'page': page,}
    return render(request, "group.html", {**content, **counts(group), **rights})


def profile(request, username):
    '''Список задач сотрудника'''
    author = get_object_or_404(User, username=username)
    all_posts = author.posts.all()
    paginator = Paginator(all_posts, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    content = {'author': author, 'page': page, }
    return render(request, 'profile.html', {**content, **counts(author), **rights})


def post_view(request, username, post_id):
    '''Страница заявки'''
    author = User.objects.get(username=username)
    post = Post.objects.select_related('author').get(id=post_id)
    day = str(post.day.date())
    comments = post.comments.all()
    form = CommentForm()
    
    content = {'form': form,
               'post': post,
               'day': day,
               'author': author,
               'comments': comments,
               'dunger': cross_for_view(request, post), }
    return render(request, 'post.html', {**content, **counts(author), **rights})


def cross_for_view(request, post):
    '''Вспомогательная функция для отображения пересечений'''
    dunger = ''
    data_check = {}
    day = str(post.day.date())
    data_check[day] = []
    post_list = Post.objects.filter(task_state_id=2,
                                    group=post.group,
                                    day=day).exclude(id=post.id)
    if len(post_list) == 0:
        return dunger
    
    for p in post_list:
        data_check[day].append(p)    
    if cross(request, post, data_check, day, 'new') != "no_cross":
        dunger = 'Интервал времени данной заявки ПЕРЕСЕКАЕТСЯ с интервалами времени других заявок.'
    return dunger

    
def post_view_change(request, username, post_id, state_id):
    '''Функция смены статуса заявки'''
    states = {2: 'подтверждена', 3: 'завершена', 4: 'отклонена',}
    author = User.objects.get(username=username)
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    post.task_state_id = state_id
    post.save()
    day = str(post.day.date())
    url = ('http://virtual2025.oak.cc:8000/' + username +
           '/' + str(post.id) + '/')
    mail_text = (f"Заявка {post.text} {states[state_id]} - {url}")
    mail(author.email, settings.RIGHTS, post.text + " " + states[state_id] + ".", mail_text)
    comments = post.comments.all()
    form = CommentForm()
    content = {'form': form,
               'post': post,
               'author': author,
               'comments': comments,
               'day': day,
               'dunger': cross_for_view(request, post), }
    return render(request, 'post.html', {**content, **counts(author), **rights})


##
def mail(author, rights, subject, body):
    '''Вспомогательная функция отправки письма'''
    recipients = []
    if len(rights) > 0:
        for user in rights:
            recipients.append(user + '@ic.irkut.com')
    #recipients = ['nikolay.emelyanov@ic.irkut.com', ]
                  #'ekaterina.mikheeva@ic.irkut.com',
                  #'dmitry.mylnikov@ic.irkut.com']
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

    smtp_obj = smtplib.SMTP('mailserv.oak.cc', port=587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.login('rrz', 'Ticket!2348')
    smtp_obj.sendmail(msg_mixed['From'], recipients, msg_mixed.as_string())
    smtp_obj.quit()


def words(*args):
    words = {
        'wrong_date':
            (f": Нельзя назначить дату и время начала испытаний в прошлом.\n"
            f"Текущая дата - {dt.datetime.now().date()}.\n"
            f"Текущее время - {str(dt.datetime.now().time())[:8]}.\n"
            f"Также нельзя назначить дату испытаний на воскресенье!"),
        'wrong_time': " : диапазон времени указан неверно!",
        'new':
            (f"Заявка {args[0].text} создана.\nВыбранный вами интервал "
            f"времени пересекается с интервалом заявки {args[1].text}.\n"
            f"Измените интервал времени, или согласуйте совместное"
            f" проведение работ с автором приоритетной заявки"
            f" {args[1].text}."),
        'edit':
            (f"Заявка {args[0].text} изменена.\nВыбранный вами интервал "
            f"времени пересекается с интервалом заявки {args[1].text}.\n"
            f"Измените интервал времени, или согласуйте совместное"
            f" проведение работ с автором приоритетной заявки"
            f" {args[1].text}."),
        'm_new':
            (f"Заявка {args[0].text} создана - {args[2]}.\n"
            f"Выбранный вами интервал времени пересекается"
            f" с интервалом заявки {args[1].text} - {args[3]}.\n"
            f"Измените интервал времени, или согласуйте "
            f"совместное проведение работ с автором "
            f"приоритетной заявки {args[1].text}."),
        'm_edit':
            (f"Заявка {args[0].text} изменена - {args[2]}.\n"
            f"Выбранный вами интервал времени пересекается"
            f" с интервалом заявки {args[1].text} - {args[3]}.\n"
            f"Измените интервал времени, или согласуйте "
            f"совместное проведение работ с автором "
            f"приоритетной заявки {args[1].text}."),
        'confirm':
            (f"Заявка {args[0].text} на стенд {args[0].group} создана. {args[2]} \n"
            f"После подтверждения администратором она отобразится в календарях.\n"
            f"Заявка подана на дату: {str(args[0].day)[:10]} на временной интервал c {args[0].t_start} по {args[0].t_stop}.\n"
            f"Подразделение-инициатор: {args[0].unit}.\n"
            f"Автор заявки: {args[0].author}.\n"
            f"Статус заявки: {args[0].task_state}.\n"
            f"Состав бригады испытателей: {args[0].testers}.\n"
            f"Объект испытаницй: {args[0].test_object}.\n"
            f"Цель работ: {args[0].purpose}.\n"
            f"Основание для проведения рабрт: {args[0].reason}.\n"
            f"Необходимая конфигурация стенда: {args[0].configuration}.\n"
            f"Требуемые инструменты: {args[0].instruments}.\n"
            f"Прочие требования: {args[0].add_requirements}.\n"
            f"Документ: {args[0].doc}.\n"), }
    return words[args[4]]
##    
def cross(request, post, data_check, day, key):
    '''Вспомогательная функция поиска пересечений временных интервалов'''
    ISIB = post.text[:4]
    bracet_post = str(post.text).find('(')
    for p in data_check[str(day)]:        
        bracet_p = str(p.text).find('(')
        if ((ISIB != 'ISIB' and ISIB != 'NUC-' and ISIB != 'FIB ')
            or post.text[bracet_post:] == p.text[bracet_p:]
            or (bracet_post == -1 and bracet_p == -1)):
                    
            if (post.t_start_id in range(p.t_start_id, p.t_stop_id)
                or (p.t_start_id >= post.t_start_id and
                    post.t_stop_id >= p.t_stop_id)
                or (p.t_start_id >= post.t_start_id and
                    post.t_stop_id in range(p.t_start_id + 1, p.t_stop_id))
                or (p.t_stop_id <= post.t_stop_id and
                    post.t_start_id in range(p.t_start_id, p.t_stop_id - 1))):
                post.save()
                new_url = ('http://virtual2025.oak.cc:8000/' + request.user.username +
                           '/' + str(post.id) + '/')
                url_user = User.objects.filter(id=p.author_id)
                if post.text[:3] == 'FIB':
                    data1 = post.text.split('(')[1][:-1]
                    data2 = p.text.split('(')[1][:-1]
                    if not set(data1.split(',')).isdisjoint(set(data2.split(','))):
                        preor_url = ('http://virtual2025.oak.cc:8000/' + url_user[0].username +
                                 '/' + str(p.id) + '/')            
                        confirm = {'new': words(post, p, new_url, preor_url, 'new'),
                                   'edit': words(post, p, new_url, preor_url, 'edit') }
                        mail_text = {'new': words(post, p, new_url, preor_url, 'm_new'),
                                     'edit': words(post, p, new_url, preor_url, 'm_edit') }
                        return([mail_text[key], confirm[key]])
                else:
                
                    preor_url = ('http://virtual2025.oak.cc:8000/' + url_user[0].username +
                                 '/' + str(p.id) + '/')            
                    confirm = {'new': words(post, p, new_url, preor_url, 'new'),
                               'edit': words(post, p, new_url, preor_url, 'edit') }
                    mail_text = {'new': words(post, p, new_url, preor_url, 'm_new'),
                                 'edit': words(post, p, new_url, preor_url, 'm_edit') }
                    return([mail_text[key], confirm[key]])
    return "no_cross"


#Дмитрий Герасимов, Сергей Чадаев
def next_number(text, bm):
    '''Вспомогательная функция расчета следующего номера заявки'''
    curent_year = dt.datetime.today().strftime('%Y')
    slash = text.find('-')
    last_slash = text.rfind('-')
    text_year = text[(slash+1):last_slash]
    bracet = text.find('(')
    if bracet != -1:
        number = text[(last_slash+1):bracet]
    else:   
        number = text[(last_slash+1):]
    if bm == '_':
        bm = ''
    if int(curent_year) == int(text_year):
        return text[:slash] + '-' + curent_year  + '-' + str(int(number)+1) + bm
    else:
        return text[:slash] + '-' + curent_year + '-1' + bm


#Дмитрий Герасимов
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
            return render(request, 'post.html', {**content, **counts(request.user), **rights})
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
def post_new(request, group_id, bm): # если bm = _, то обычный номер
    '''Функция создания заявки'''
    new = Post()
    new.group_id = group_id
    if group_id in range(3,7):  # isib, fib, nuc, fib bm
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
        post.t_start_html =  post.t_start_id * 2 - 2
        post.t_stop_html = (post.t_stop_id - post.t_start_id) * 2
        #### если выбранная дата некорректна ################################
        if not data_correct(post):
            stend = stend + words(post, post, '', '', 'wrong_date')
            content = {'form': form, 'stend': stend, 'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights})
        #### если выбранный интервал времени некорректен ####################
        if not int(post.t_start_id) < int(post.t_stop_id):
            stend = stend + words(post, post, '', '', 'wrong_time')   
            content = {'form': form, 'stend': stend, 'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights})
        #####################################################################
        if post.group_id == 5:
            post.testers = '-'
            post.test_object = '-'
            post.purpose = '-'
            post.reason = '-'
            post. configuration = '-'
            post. instruments = '-'
            post. add_requirements = '-'
            post. doc = '-'
        #####################################################################
        post.save()
        url = ('http://virtual2025.oak.cc:8000/' + request.user.username +
               '/' + str(post.id) + '/')
        if post.group_id in range(4, 7):
            mail(request.user.email, [], post.text + " создана.", url)
        else:
            mail(request.user.email, settings.RIGHTS, post.text + " создана.", url)
        return redirect('post', post.author, post.id)
    content = {'form': form, 'stend': stend, 'confirm': confirm, }  
    return render(request, 'new_post.html', {**content, **rights})


@login_required
def post_new_one(request, stend_id, start_id, day):
    buttons = {}
    sib = {'SIB': '_',}
    acib = {'ACIB': '_',}
    isib = {'ISIB (Без БМ)': '_',
            'ISIB (+ БМ1)': '(БМ1)',
            'ISIB (+ БМ2)': '(БМ2)',
            'ISIB (+ БМ3)': '(БМ3)',}
    fib = {'FIB CPIOM 1': '(1)',
           'FIB CPIOM 2': '(2)',
           'FIB CPIOM 3': '(3)',
           'FIB CPIOM 4': '(4)',
           'FIB CPIOM 5': '(5)',
           'FIB MDU': '(MDU)',}
    nuc = {'NUC227 (ABSINT)': '(227)',
           'NUC237': '(237)',
           'NUC238': '(238)',
           'NUC239': '(239)',}
    fib_bm = {'FIB BM Linux': '(Linux)',
              'FIB BM Windows': '(Windows)',}
    
    all_buttons = {1: sib, 2: acib, 3: isib, 4: fib, 5: nuc, 6: fib_bm,}
    if stend_id == 1:
        return redirect('post_new_from_table', 1, '_', start_id, day)
    elif stend_id ==2:
        return redirect('post_new_from_table', 2, '_', start_id, day)
    elif stend_id == 3:
        buttons = {'ISIB (Без БМ)': '_',
                   'ISIB (+ БМ1)': '(БМ1)',
                   'ISIB (+ БМ2)': '(БМ2)',
                   'ISIB (+ БМ3)': '(БМ3)',}
    elif stend_id == 4:
        buttons = {'FIB CPIOM 1': '(1)',
                   'FIB CPIOM 2': '(2)',
                   'FIB CPIOM 3': '(3)',
                   'FIB CPIOM 4': '(4)',
                   'FIB CPIOM 5': '(5)',
                   'FIB MDU': '(MDU)',}
    elif stend_id == 5:
        buttons = {'NUC227 (ABSINT)': '(227)',
                   'NUC237': '(237)',
                   'NUC238': '(238)',
                   'NUC239': '(239)',}
    elif stend_id == 6:
        buttons = {'FIB BM Linux': '(Linux)',
                   'FIB BM Windows': '(Windows)', }

    content = {'buttons': buttons,
               'g_id': stend_id,
               'start_id': start_id,
               'day': day,
               'all_buttons': all_buttons, } 
    return render(request, 'new_post_one.html', {**content, **rights})


@login_required
def post_new_from_table(request, group_id, bm, start_id, day): # если bm = _, то обычный номер
    '''Функция создания заявки'''
    new = Post()
    new.group_id = group_id
    new.t_start_id = start_id
    new.t_stop_id = 48
    new.day = day
    if group_id in range(3,7):  # isib, fib, nuc, fib bm
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
        post.t_start_html =  post.t_start_id * 2 - 2
        post.t_stop_html = (post.t_stop_id - post.t_start_id) * 2
        #### если выбранная дата некорректна ################################
        if not data_correct(post):
            stend = stend + words(post, post, '', '', 'wrong_date')
            content = {'form': form, 'stend': stend, 'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights})
        #### если выбранный интервал времени некорректен ####################
        if not int(post.t_start_id) < int(post.t_stop_id):
            stend = stend + words(post, post, '', '', 'wrong_time')   
            content = {'form': form, 'stend': stend, 'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights})
        #####################################################################
        if post.group_id == 5:
            post.testers = '-'
            post.test_object = '-'
            post.purpose = '-'
            post.reason = '-'
            post. configuration = '-'
            post. instruments = '-'
            post. add_requirements = '-'
            post. doc = '-'
        #####################################################################
        post.save()
        url = ('http://virtual2025.oak.cc:8000/' + request.user.username +
               '/' + str(post.id) + '/')
        if post.group_id in range(4, 7):
            mail(request.user.email, [], post.text + " создана.", url)
        else:
            mail(request.user.email, settings.RIGHTS, post.text + " создана.", url)
        return redirect('post', post.author, post.id)
    content = {'form': form, 'stend': stend, 'confirm': confirm, }  
    return render(request, 'new_post.html', {**content, **rights})


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
        #form.save()
        post = form.save(commit=False)
        if post.group_id in range(3,7):  # isib, fib, nuc, fib bm
            post.task_state_id = 2
        else:
            post.task_state_id = 1
        post.t_start_html =  post.t_start_id * 2 - 2
        post.t_stop_html = (post.t_stop_id - post.t_start_id) * 2
        #### если выбранная дата некорректна ################################
        if not data_correct(post):
            stend = stend + words(post, post, '', '', 'wrong_date')
            content = {'form': form, 'post': post, 'edit': True, 'stend': stend,
                       'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights})
        #### если выбранный интервал времени некорректен ####################
        if not int(post.t_start_id) < int(post.t_stop_id):
            stend = stend + words(post, post, '', '', 'wrong_time')
            content = {'form': form, 'post': post, 'edit': True, 'stend': stend,
                       'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights})
        #####################################################################
        post.save()
        url = ('http://virtual2025.oak.cc:8000/' + request.user.username +
               '/' + str(post.id) + '/')
        if post.group_id in range(4, 7):
            mail(request.user.email, [], post.text + " изменена.", url)
        else:
            mail(request.user.email, settings.RIGHTS, post.text + " изменена.", url)
        return redirect('post', post.author, post.id)
    content = {'form': form, 'post': post, 'edit': True, 'stend': stend,
               'month': str(YEAR) + "-" + str(MONTH),'confirm': confirm, }
    return render(request, 'new_post.html', {**content, **rights})


@login_required
def post_copy(request, username, post_id):
    '''Функция создания заявки из шаблона'''
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    post.day = str(post.day)[:-15]
    stend = Group.objects.filter(id=post.group_id).latest('id').title
    new = Post()
    confirm =""
    latest = str(Post.objects.filter(group_id=post.group_id).latest('id'))
    if post.text.find('(') != -1:
        new.text = next_number(latest, post.text[post.text.find('('):])
    else:
        new.text = next_number(latest, "_")
    new.pub_date = post.pub_date
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
    new.all_in = post.all_in
    if new.group_id in range(3,7):  # isib, fib, nuc, fib bm
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
        #form.save()
        post = form.save(commit=False)
        post.author = request.user
        post.pub_date = dt.datetime.now()
        post.t_start_html =  post.t_start_id * 2 - 2
        post.t_stop_html = (post.t_stop_id - post.t_start_id) * 2
        #post = get_object_or_404(Post, author__username=username, pk=new.id)
        #### если выбранная дата некорректна ################################
        if not data_correct(post):
            stend = stend + words(post, post, '', '', 'wrong_date')
            content = {'form': form, 'post': post, 'edit': False, 'stend': stend,
                       'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights})
        #### если выбранный интервал времени некорректен ####################
        if not int(post.t_start_id) < int(post.t_stop_id):
            stend = stend + words(post, post, '', '', 'wrong_time')
            content = {'form': form, 'post': post, 'edit': False, 'stend': stend,
                       'confirm': confirm, }
            return render(request, 'new_post.html', {**content, **rights})
        #####################################################################
        post.save()
        url = ('http://virtual2025.oak.cc:8000/' + request.user.username +
               '/' + str(post.id) + '/')
        if post.group_id in range(4, 7):
            mail(request.user.email, [], post.text + " создана.", url)
        else:
            mail(request.user.email, settings.RIGHTS, post.text + " создана.", url)
        return redirect('post', post.author, post.id)
    content = {'form': form, 'post': post, 'edit': False, 'stend': stend,
               'confirm': confirm, }
    return render(request, 'new_post.html', {**content, **rights})


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
                for i in range(1, len(word)//60 + 2):   
                    new_word += word[60*(i-1):60*i] + " "
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
    return render(request, 'feedback.html', {**content, **rights})

@login_required
def delete_feedback(request, feedback_id):
    """Добавление предложения"""
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if feedback.author == request.user or request.user.username in settings.RIGHTS:
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
        dislike = Dislike.objects.filter(feedback_id=feedback_id, user_id=user_id)
        if dislike.count() > 0:
            for dis in dislike:
                dis.delete()
            feedback.dislikes -= 1
    else:
        for like in likes:
            like.delete()
        feedback.likes = Like.objects.filter(feedback_id=feedback_id).count()
    feedback.save()
    
    feedbacks = Feedback.objects.all()
    content = {'feedbacks': feedbacks, 'form': FeedbackForm(),}
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
    paginator = Paginator(all_posts, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    content = {'author': author, 'page': page, }
    return render(request, 'profile.html', {**content, **counts(author), **rights})


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
                  {**rights,
                   'day': str(dt.date.today()),
                   'wk': str(dt.datetime.now().date().year) + '-' + str(wk),
                   'month': str(dt.datetime.now().date().year) + "-" + str(dt.datetime.now().date().month)})


def rele_isib(request):
    return render(request, 'rele_isib.html', {**rights, })

def rele_isib_cold(request):
    return render(request, 'rele_isib_cold.html', {**rights, })

def rele_on_off(request, IP, rele_number, state):
    '''Вспомогательная функция запроса на вкл/выкл реле'''
    if state == 'on':
        requests.get(
            'http://admin:admin@' + IP + '/protect/rb'+ rele_number + 'n.cgi',
            verify=False,
            timeout=10)
    else:
        requests.get(
            'http://admin:admin@' + IP + '/protect/rb'+ rele_number + 'f.cgi',
            verify=False,
            timeout=10)
    if IP == '10.1.98.249':
        return render(request, 'rele_isib.html', {**rights, })
    elif IP == '10.1.98.248':
        return render(request, 'rele_isib_cold.html', {**rights, })


rele_cold = {'БМ1':'0', 'БМ2':'1', 'БМ3':'2', }
how_many = {'БМ1': 0, 'БМ2': 0, 'БМ3': 0, }
how_many_bm = set()
IP_cold = '10.1.98.248'
rele_no_signal = 0
rele_cold_no_signal = 0


@background(schedule=5)
def hello_world():
    '''Функция работы с управляемым реле'''
    rele = {'БМ1_1':'0', 'БМ1_2':'1',
            'БМ2_1':'2', 'БМ2_2':'3',
            'БМ3_1':'4', 'БМ3_2':'5'}
            #  FIB
    today_recs = {'all':[], 'future':[], 'now':[], 'over':[],
                  'БМ1':[], 'БМ2':[], 'БМ3':[],
                  'FIB_1':[], 'FIB_2':[], 'FIB_3':[],'FIB_4':[], 'FIB_5':[], 'FIB_MDU':[],}
    today = dt.datetime.now()
    groups = [3,4]
    today_post_list = Post.objects.filter(day=today.date(), task_state_id=2, group__in=groups)#  fib group=4
    print('________________________________________________________________________')
    # Если заявки на сегодня есть,
    if len(today_post_list) != 0:
        for rec in today_post_list:
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
            print(rec.text, ': ', rec.t_start,' - ', rec.t_stop, end="")
            
            if 15 >= difference_start_min >= 0:
                print(f". До начала работ менее 15 минут.")
                today_recs['now'].append(rec)
            elif difference_start_min < 0:
                if  difference_stop_min <= -30:
                    print(f". Завершена.")
                    today_recs['over'].append(rec)
                else:
                    print(f". В работе.")
                    today_recs['now'].append(rec)
            else:  # if difference_start_min > 15:
                print(f". До начала работ более 15 минут.")
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
                fib_rec = rec.text.split('(')[1][:-1]# '1,2,3,4,5'
                if fib_rec != '':
                    for r in fib_rec.split(','):
                        today_recs['FIB_'+ r].append(rec)
    print('________________________________________________________________________')
    # Работа с управляемым реле
    rele_now(today_recs['БМ1'], rele['БМ1_1'], rele['БМ1_2'], 'БМ1')
    rele_now(today_recs['БМ2'], rele['БМ2_1'], rele['БМ2_2'], 'БМ2')
    rele_now(today_recs['БМ3'], rele['БМ3_1'], rele['БМ3_2'], 'БМ3')
    #rele_now(today_recs['FIB_1'], rele['TBD'], rele['TBD'], 'FIB_1')
    cold_check(today_recs)
    print(today,': следующий запрос через 10 минут')
    time.sleep(600)
    #python manage.py process_tasks


def rele_now(recs, number1, number2, bm):
    '''Вспомогательная функция включения/отключения реле'''
    if len(recs) == 0:
        try:
            print(f"Заявок в работе на {bm} - {len(recs)} \n"
                  f"Если питание на {bm} не выключено, то необходимо выключить")
            if rele_state(number1, IP) == '1'or rele_state(number2, IP) == '1':
                print('Сейчас питание не выключено')
                res = on_off(IP, number1, 'off')
                res = on_off(IP, number2, 'off')
                if rele_state(number1, IP) == '0'and rele_state(number2, IP) == '0':
                    print('Теперь питание выключено')
            print('________________________________________________________________________')
                
        except Exception as e:
            print("Реле недоступно -", e)
            if rele_no_signal == 0:
                mail('nikolay.emelyanov@ic.irkut.com',
                     settings.RIGHTS,
                     "Реле на ISIB",
                     "Реле на ISIB недоступно")
            rele_no_signal+=1
            if rele_no_signal == 20:
                rele_no_signal = 0
    else:
        try:
            print(f"Заявок в работе на {bm} - {len(recs)} \n"
                  f"Если питание на {bm} не включено, то необходимо включить")
            if rele_state(number1, IP) == '0'or rele_state(number2, IP) == '0':
                print('Сейчас питание не включено')
                res = on_off(IP, number1, 'on')
                res = on_off(IP, number2, 'on')
                if rele_state(number1, IP) == '1'and rele_state(number2, IP) == '1':
                    print('Теперь питание включено')
            print('________________________________________________________________________')
        except Exception as e:
            print("Реле недоступно -", e)
            if rele_no_signal == 0:
                mail('nikolay.emelyanov@ic.irkut.com',
                     settings.RIGHTS,
                     "Реле на ISIB",
                     "Реле на ISIB недоступно")
            rele_no_signal+=1
            if rele_no_signal == 20:
                rele_no_signal = 0


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
            'http://admin:admin@' + IP + '/protect/rb'+ rele_number + 'n.cgi',
            verify=False,
            timeout=10)
    return requests.get(
        'http://admin:admin@' + IP + '/protect/rb'+ rele_number + 'f.cgi',
        verify=False,
        timeout=10)


def rele_state(number, IP):
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
        if rele_no_signal == 0:
            mail('nikolay.emelyanov@ic.irkut.com',
                 settings.RIGHTS,
                 "Реле на ISIB",
                 "Реле на ISIB недоступно")
        rele_no_signal+=1
        if rele_no_signal == 20:
            rele_no_signal = 0
        return '-1'


def cold_check(recs):
    '''Вспомогательная функция опроса статуса вентиляторов'''
    if len(recs['БМ1']) == 0:
        how_many_times('БМ1', '0')
    else:
        if how_many_times('БМ1', '+1') == 6:
            for key in  how_many.keys():
                how_many[key] = 0
            return
    
    if len(recs['БМ2']) == 0:
        how_many_times('БМ2', '0')
    else:
        if how_many_times('БМ2', '+1') == 6:
            for key in  how_many.keys():
                how_many[key] = 0
            return
    
    if len(recs['БМ3']) == 0:
        how_many_times('БМ3', '0')
    else:
        if how_many_times('БМ3', '+1') == 6:
            for key in  how_many.keys():
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
    print('________________________________________________________________________')
    return how_many[bm]


def if_on_then_off(bm, rele_number, IP):
    # если вентилятор ВКЛ, то ВЫКЛ
    try:
        print(f"Если питание вентилятора на {bm} не выключено, то необходимо выключить")
        if rele_state(rele_number, IP) == '1':
            print('Сейчас питание не выключено')
            res = on_off(IP, rele_number, 'off')
            if rele_state(rele_number, IP) == '0':
                print('Теперь питание выключено')
    except Exception as e:
        print("Реле недоступно -", e)
        if rele_cold_no_signal == 0:
            mail('nikolay.emelyanov@ic.irkut.com',
                 settings.RIGHTS,
                 "Реле вентиляторов на ISIB",
                 "Реле вентиляторов на ISIB недоступно")
        rele_cold_no_signal+=1
        if rele_cold_no_signal == 20:
            rele_cold_no_signal = 0


def if_off_then_on(bm, rele_number, IP):
    # если вентилятор ВЫКЛ, то ВКЛ
    try:
        print(f"если питание вентилятора на {bm} не включено, то необходимо включить")
        if rele_state(rele_number, IP) == '0':
            print('Сейчас питание не включено')
            res = on_off(IP, rele_number, 'on')
            if rele_state(rele_number, IP) == '1':
                print('Теперь питание включено')
    except Exception as e:
        print("Реле недоступно -", e)
        if rele_cold_no_signal == 0:
            mail('nikolay.emelyanov@ic.irkut.com',
                 settings.RIGHTS,
                 "Реле вентиляторов на ISIB",
                 "Реле вентиляторов на ISIB недоступно")
        rele_cold_no_signal+=1
        if rele_cold_no_signal == 20:
            rele_cold_no_signal = 0


def statistic(request):    
    month = dt.datetime.now().month
    year = dt.datetime.now().year    
    days = monthrange(year, month)[1]
    day_start_num = date(year, month, 1)
    end_date = date(year, month, days) + timedelta(1)
    post_list = Post.objects.filter(day__range=[day_start_num, end_date],
                                    task_state_id=2)

    sib = []
    acib = []
    isib = []

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
                result += (item.t_stop_id - item.t_start_id)/2
            sib_results[key] = round(result/day_work_time, 2)
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
                result += (item.t_stop_id - item.t_start_id)/2
            acib_results[key] = round(result/day_work_time, 2)
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
                result += (item.t_stop_id - item.t_start_id)/2
            isib_results[key] = round(result/day_work_time, 2)
            result = 0
        isib_month = 0
        for key in isib_results.keys():
            isib_month += isib_results[key]
        isib_month = round(isib_month / len(isib_results.keys()), 2)
    content = {'count': count,
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
    return render(request, 'statistic.html', {**content, **rights})



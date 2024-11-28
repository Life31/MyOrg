
#from asyncio.windows_events import NULL
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
#from django.http import HttpResponse


from .forms import TaskForm, CardForm, BordForm, NoteForm
from .models import Task, Bord, Card, Note
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from posts.models import Feedback
import datetime as dt
from calendar import monthrange
import json
import re
import requests



def some_count(request):
    feedbacks_count = Feedback.objects.filter(
        state_id__in=[5, 6]  # Новое, В работе
    ).count
    users_counts = User.objects.all().count
    content = {
        'feedbacks_count': feedbacks_count,
        'users_counts': users_counts,
    }
    if request.user.username in settings.RIGHTS:
        try:
            ips = {'10.1.98.247', '10.1.98.248', '10.1.98.249', }
            rele_count_of_1 = []
            for ip in ips:
                res = requests.get(
                    'http://admin:admin@' + ip + '/pstat.xml',
                    verify=False,
                    timeout=5,
                )
                rele_count_of_1 += re.findall(r'[>][1][<]', str(res.content))
            content = {
                'feedbacks_count': feedbacks_count,
                'users_counts': users_counts,
                'count_of_1': len(rele_count_of_1),
            }   
        except Exception as ex:
            print(ex)
            content = {
                'feedbacks_count': feedbacks_count,
                'users_counts': users_counts,
                'count_of_1': 0,
            }
    return content


def rights(request):
    rights = {
        'rights': settings.RIGHTS,
        'storage_rights': settings.STORAGE_RIGHTS,
        'sadec_rights': settings.SADEC_RIGHTS,
        'pro_rights': settings.PRO_RIGHTS,
        'passes_rights': settings.PASSES_RIGHTS,
        **some_count(request),
    }
    return rights


urls = {
    'task_urls': {
        'task_all',
        'task_out',
        'task_in',
        'task_new',
    },
}


def lol(request):
    print('lol')


def bord_new(request):
    all_bords = Bord.objects.all()
    user_bords = Bord.objects.filter(user_id=request.user.id)
    bord = Bord()
    bord.user = request.user
    form = BordForm(
        request.POST or None,
        files=request.FILES or None,
        instance=bord,
    )
    if form.is_valid():
        bord = form.save(commit=False)

        bord.save()
        return redirect('task_all', bord.id)
    return render(
        request,
        'task_bord_new.html',
        {
            'form': form,
            'all_bords': all_bords,
            'user_bords': user_bords,
        }
    )


def bord_invite(request, bord_id, user_id):
    bord = Bord.objects.filter(id=bord_id)[0]
    if bord.guests == "":
        bord.guests = bord.guests + str(user_id)
    else:
        bord.guests = bord.guests + '_' + str(user_id)
    bord.save()
    return redirect('task_all', bord_id)


def bord_leave(request, bord_id, user_id):
    bord = Bord.objects.filter(id=bord_id)[0]
    arr_bord = str(bord.guests).split('_')

    arr_bord[arr_bord.index(str(user_id))] = ""
    new_guests = ""
    for b in arr_bord:
        new_guests += b
        new_guests += '_'
    new_guests = new_guests.replace('__', '_')
    if len(new_guests) > 1:
        if new_guests[0] == '_':
            new_guests = new_guests[1:]
        if new_guests[-1] == '_':
            new_guests = new_guests[:-1]
    else:
        new_guests = ''

    bord.guests = new_guests
    bord.save()
    return redirect('task_all', bord_id)


def card_new(request, bord_id):
    form = CardForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        card = form.save(commit=False)
        card.bord_id = bord_id
        card.save()
        return redirect('task_all', bord_id)
    return render(
        request,
        'task_card_new.html',
        {'bord_id': bord_id, 'form': form, }
    )


def bord_delete(request, bord_id):
    bord = get_object_or_404(Bord, id=bord_id)
    cards = Card.objects.filter(bord_id=bord_id)
    for card in cards:
        tasks = Task.objects.filter(card_id=card.id)
        for task in tasks:
            task.delete()
        card.delete()
    bord.delete()
    return redirect('bord_new', )


def bord_rename(request, bord_id):
    all_bords = Bord.objects.all()
    user_bords = Bord.objects.filter(user_id=request.user.id)
    bord = get_object_or_404(Bord, id=bord_id)
    form = BordForm(
        request.POST or None,
        files=request.FILES or None,
        instance=bord,
    )
    if form.is_valid():
        bord = form.save(commit=False)

        bord.save()
        return redirect('task_all', bord.id)

    return render(
        request,
        'task_bord_new.html',
        {'bord_id': bord_id,
        'form': form, 'edit': True,
        'all_bords': all_bords,
        'user_bords': user_bords, }
    )

def card_delete(request, bord_id, card_id):
    card = get_object_or_404(Card, id=card_id)
    tasks = Task.objects.filter(card_id=card_id)
    for task in tasks:
        task.delete()
    card.delete()
    return redirect('task_all', bord_id)


def card_rename(request, bord_id, card_id):
    card = get_object_or_404(Card, id=card_id)
    
    form = CardForm(
        request.POST or None,
        files=request.FILES or None,
        instance=card,
    )
    if form.is_valid():
        form.save()
        return redirect('task_all', bord_id)

    return render(
        request,
        'task_card_new.html',
        {'bord_id': bord_id, 'form': form, 'edit': True, }
    )


def task_delete(request, bord_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_all', bord_id)


def task_all_alter(request, bord_id): # полоски
    cards = Card.objects.filter(bord_id=bord_id)
    cards_ids = [c.id for c in cards]
    cards_tasks = {}
    all_tasks = []
    for id in cards_ids:
        cards_tasks[id] = Task.objects.filter(card_id=id)
        all_tasks += cards_tasks[id]

    month = dt.datetime.now().month
    year = dt.datetime.now().year
    days_in_month = monthrange(year, month)[1]
    month_start = dt.datetime(year, month, 1).date()
    month_end = dt.datetime(year, month, days_in_month).date()
    line_tasks = {}
    i = 1
    for t in all_tasks:
        if t.day_start is not None and t.day_end is not None:
            if t.day_start.date() >= month_start and t.day_end.date() <= month_end:
                line_tasks[i] = {}
                line_tasks[i]['task'] = t
                line_tasks[i]['left'] = str((t.day_start.date().day - 1) / days_in_month * 100).replace(',', '.')
                line_tasks[i]['range'] = str(((t.day_end.date() - t.day_start.date()).days + 1) / days_in_month * 100).replace(',', '.')
                line_tasks[i]['day_end'] = t.day_end.date().day
            elif t.day_start.date() >= month_start and t.day_end.date() > month_end:
                line_tasks[i] = {}
                line_tasks[i]['task'] = t
                line_tasks[i]['left'] =str((t.day_start.date().day - 1) / days_in_month * 100).replace(',', '.')
                line_tasks[i]['range'] = str(((month_end - t.day_start.date()).days + 1) / days_in_month * 100).replace(',', '.')
                line_tasks[i]['day_end'] = month_end
            elif t.day_start.date() < month_start and t.day_end.date() <= month_end:
                line_tasks[i] = {}
                line_tasks[i]['task'] = t
                line_tasks[i]['left'] = 0
                line_tasks[i]['range'] = (t.day_end.date() - t.day_start.date()).days
                line_tasks[i]['day_end'] = t.day_end.date().day
            elif t.day_start.date() < month_start and t.day_end.date() > month_end:
                line_tasks[i] = {}
                line_tasks[i]['task'] = t
                line_tasks[i]['left'] = 0
                line_tasks[i]['range'] = days_in_month
                line_tasks[i]['day_end'] = month_end
            else:
                pass
            i += 1

    days = [d for d in range(1, days_in_month + 1)]
    width = str(1 / days_in_month * 100).replace(',', '.')
    #day = str(dt.datetime.now().day / days_in_month * 100).replace(',', '.')
    day = dt.datetime.now().day
    days_bfr_now = [d for d in range(1, day + 1)]
    print(day)
    return render(request, 'task_all_alter.html', {
        **rights(request), **urls, 'line_tasks': line_tasks,
        'days_in_month': days, 'width': width, 'day': day, 'days_bfr_now': days_bfr_now })


from users.views import (
    get_user_bords_and_ids,
    get_tasks_sorted_by_bords,
    get_new_tasks_sorted_by_bords
)
from users.models import User_info

def check_user_rights(request, access_type):
    rights = User_info.objects.filter(user_id=request.user.id)
    if len(rights) > 0:
        return getattr(rights[0], access_type)
    return False


def task_all(request, bord_id):  # bord_id

    if check_user_rights(request, 'task_access') is False:
        return redirect('bord_new',) #страница "нет прав"
    
    if bord_id == 0:
        return redirect('bord_new',)

    # current
    bord = Bord.objects.filter(id=bord_id)[0]
    bord_owner = User.objects.filter(id=bord.user_id)[0]
    users = str(Bord.objects.filter(id=bord_id)[0].guests).split('_')

    all_users = User.objects.all()
    if users[0] != 'None' and users[0] != "":
        for user in all_users:
            if str(user.id) in users:
                users[users.index(str(user.id))] = user
    else:
        users = []

    all_bords = Bord.objects.all()
    user_bords = Bord.objects.filter(user_id=request.user.id)
    cards = Card.objects.filter(bord_id=bord_id)

    cards_ids = [c.id for c in cards]

    cards_tasks = {}
    all_tasks = []
    for id in cards_ids:
        cards_tasks[id] = Task.objects.filter(card_id=id)
        all_tasks += cards_tasks[id]

    json_data = {}
    for t in all_tasks:

        json_data[t.id] = []
        json_data[t.id].append(t.text)
        json_data[t.id].append(t.state_id)
        json_data[t.id].append(t.persent)
        if t.day_start is not None:
            json_data[t.id].append(str(t.day_start.date()))
        else:
            json_data[t.id].append("")
        if t.day_end is not None:
            json_data[t.id].append(str(t.day_end.date()))
        else:
            json_data[t.id].append("")
        json_data[t.id].append(t.result)
        json_data[t.id].append('file here should be')
        json_data[t.id].append(t.master_id)
        json_data[t.id].append(t.slave_id)

        json_data[t.id].append(t.card_id)
        json_data[t.id].append(t.same_id)
        json_data[t.id].append(t.bord_link_id)
        if t.image:
            json_data[t.id].append(t.image.url)
        else:
            json_data[t.id].append("")
        if t.file:
            json_data[t.id].append(t.file.url)
        else:
            json_data[t.id].append("")

    # Все доски [], где участвует пользователь и их id []
    user_bords, user_bords_ids = get_user_bords_and_ids(all_bords, request.user.id)
    tasks_sorted_by_bords = get_tasks_sorted_by_bords(user_bords_ids)
    new_tasks_sorted_by_bords = get_new_tasks_sorted_by_bords(tasks_sorted_by_bords, request.user)

    if bord_id in new_tasks_sorted_by_bords.keys():
        for t in tasks_sorted_by_bords[bord_id]:
            if t.slave_id == request.user.id:
                t.new = False
                t.save()
    form = TaskForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        task = form.save(commit=False)
        task.bord_id = bord_id
        if task.same_id is not None:
            task.id = int(task.same_id)
        else:
            task.id = Task.objects.all().latest('id').id + 1
            task.same_id = task.id

        time_now = dt.datetime.now()
        if task.day_start is not None:
            task.day_start = dt.datetime.strptime(str(task.day_start)[:-6], '%Y-%m-%d %H:%M:%S')
            task.day_start += dt.timedelta(hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second)
        if task.day_end is not None:
            task.day_end = dt.datetime.strptime(str(task.day_end)[:-6], '%Y-%m-%d %H:%M:%S')
            task.day_end += dt.timedelta(hours=23, minutes=59, seconds=59)

        task.pub_date = dt.datetime.now()
        task.save()
        return redirect('task_all', bord_id)

    return render(request, 'task_all.html', {
        **rights(request), **urls, 'bord_id': bord_id,
        'cards': cards, 'cards_tasks': cards_tasks,
        'bord': bord,  # current
        'bord_owner': bord_owner,
        'user_bords': user_bords,
        'all_bords': all_bords,
        'users_on_bord': users,
        'all_users': all_users,
        #'all_tasks': all_tasks,
        'form': form,
        'json_data': json.dumps(json_data),
        'new_tasks_sorted_by_bords': new_tasks_sorted_by_bords,
        }
    )


def task_slave_change(request, bord_id, task_id, new_slave_id):
    task = get_object_or_404(Task, id=task_id)
    task.slave_id = new_slave_id
    task.save()
    return redirect('task_all', bord_id)


def task_persent_change(request, bord_id, task_id, persent):
    task = get_object_or_404(Task, id=task_id)
    task.persent = persent
    task.save()
    return redirect('task_all', bord_id)


def task_state_change(request, bord_id, task_id, new_state_id):
    task = get_object_or_404(Task, id=task_id)
    if task.state_id == new_state_id:
        return redirect('task_all', bord_id)
    else:
        if new_state_id == 3:
            task.state_id = new_state_id
            task.day_real_end = dt.datetime.now().date()
        elif new_state_id == 2:
            task.state_id = new_state_id
        elif new_state_id == 1:
            task.state_id = new_state_id
            task.day_real_end = None
        task.save()
    return redirect('task_all', bord_id)


def task_out(request):
    tasks = Task.objects.filter(master_id=request.user.id)
    paginator = Paginator(tasks, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'task_all.html',
        {**rights(request), **urls, 'page': page, }
        )

def task_in(request):
    tasks = Task.objects.filter(slave_id=request.user.id)
    paginator = Paginator(tasks, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'task_all.html',
        {**rights(request), **urls, 'page': page, }
        )

def task(request, task_id):
    task = Task.objects.filter(id=task_id)[0]
    include = Task.objects.filter(include_in=task_id)
    return render(
        request,
        'task.html',
        {**rights(request), **urls, 'task': task, 'include': include, }
        )


def task_new(request, card_id):

    task = Task()
    task.master_id = request.user.id
    task.state_id = 1
    task.persent = 0
    task.card_id = card_id
    bord_id = Card.objects.filter(id=card_id)[0].bord_id
    
    form = TaskForm(
        request.POST or None,
        files=request.FILES or None,
        instance=task,
    )
    if form.is_valid():
        task = form.save(commit=False)
        #Task.objects.all().latest('id')
        task.id = Task.objects.all().latest('id').id + 1
        task.bord_id = bord_id
        task.same_id = task.id

        time_now = dt.datetime.now()
        if task.day_start is not None:
            task.day_start =dt.datetime.strptime(str(task.day_start)[:-6], '%Y-%m-%d %H:%M:%S')
            task.day_start += dt.timedelta(hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second)
        if task.day_end is not None:
            task.day_end =dt.datetime.strptime(str(task.day_end)[:-6], '%Y-%m-%d %H:%M:%S')
            task.day_end += dt.timedelta(hours=23, minutes=59, seconds=59)

        task.save()
        return redirect('task_all', bord_id)
    return render(
        request,
        'task_new.html',
        {'form': form, **rights(request), **urls}
    )

def calendar(request, year):
    if year == 0:
        year = dt.datetime.today().year
    today = dt.datetime.today().date()
    month_all = full_year(year)

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
    return render(
        request,
        'task_calendar.html',
        {**rights(request), **urls,
         'today': today,
         'year': year,
         'month_all': month_all,
         'holidays': h_days}
    )

def full_year(year):
    month_all = {
        1:'Январь', 2:'Февраль', 3:'Март',
        4:'Апрель', 5:'Май', 6:'Июнь',
        7:'Июль', 8:'Август', 9:'Сентябрь',
        10:'Октябрь', 11:'Ноябрь', 12:'Декабрь',
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

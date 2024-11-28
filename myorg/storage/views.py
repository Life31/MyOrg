from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404 # reverse, 
#import datetime as dt
from .models import Unit, Th, Tag, Th_tags, Event, User_units  #, User
from .forms import (UnitForm, ThForm, CreatorForm,
                    CtgryForm, PlaceForm, SiForm,
                    StendForm, TagForm, Tag_addForm, EventForm)
from django.conf import settings
from django.db.models import Sum
#import openpyxl
#import shutil
from django.db.models import Q
#from django.utils import timezone
import datetime as dt
import os
from users.models import User_info

rights = {'rights': settings.RIGHTS,
          'storage_rights': settings.STORAGE_RIGHTS,
          'sadec_rights': settings.SADEC_RIGHTS,
          'pro_rights': settings.PRO_RIGHTS,
          'passes_rights': settings.PASSES_RIGHTS,
          'page_name': 'Склад',
          }

urls = {
    'storage_urls':{
        'storage', 'unit_new', 'unit_edit', 'event_new', 'event_edit',
        'unit_ths', 'th_new', 'th_edit', 'main',
        'units_by_ctgry', 'units_by_creator', 'units_by_place',
        'th_all', 'th_all_year', 'th_all_type', 'th_all_tag',
        'place_new', 'creator_new', 'ctgry_new', 'tag_new', 'tag_add',
        'si_new', 'stend_new', 'storage_where', 'units_search', 
        },
    }

def data():
    data = {
        'tags': Tag.objects.all(),
        'th_tags': Th_tags.objects.all(),
        }
    return data


def stor_access_check(request):
    return get_object_or_404(User_info, user_id=request.user.id).stor_access


def storage(request):
    '''Карта склада'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    
    return render(request, 'storage.html', {**rights, **urls})


@login_required
def unit_new(request):
    '''Добавить новую учетную единицу'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    number = Unit.objects.all().latest('id').number + 1
    form = UnitForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        unit = form.save(commit=False)
        unit.number = number
        unit.author = request.user
        unit.save()
        return redirect('main')
    content = {'form': form, }
    return render(request, 'unit_new.html', {**content, **rights, **urls})


@login_required
def unit_edit(request, unit_id):
    '''Редактировать учетную единицу'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    unit = get_object_or_404(Unit, id=unit_id)
    
    form = UnitForm(request.POST or None,
                    files=request.FILES or None,
                    instance=unit)

    if form.is_valid():
        form.save()
        return redirect('unit_ths', unit_id)
    content = {'form': form, 'unit': unit, 'edit': True, }
    return render(request, 'unit_new.html', {**content, **rights, **urls})


@login_required
def unit_delete(request, unit_id):
    '''Удалить учетную единицу'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    unit = get_object_or_404(Unit, id=unit_id)
    
    try:
        if unit.image:
            os.remove(settings.MEDIA_ROOT + unit.image.url)
            print(f'Файл {settings.MEDIA_ROOT + unit.image.url} успешно удален')
    except:
        print(f'Не удалось удалить файл {settings.MEDIA_ROOT + "/" + unit.image.url}')
    unit.delete()
    return redirect('main')


@login_required
def th_new(request):
    '''Добавить новую накладную'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    form = ThForm(
        request.POST or None,
        files=request.FILES or None
    )
          
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        
        try:
            event = Event()
            unit = Unit.objects.filter(number=int(post.unit_number))[0]
            event.th_name_id = post.id
            event.unit_name_id = unit.id
            if post.type_th == 'Входящие':
                event.event_name_id = 1
            else:
                event.event_name_id = 2
            event.num = 1
            event.date = post.day
            event.comment = post.comment
            event.pub_day = post.pub_day
            event.author = post.author
            event.save()
        except:
            print('некорректный post.unit_number')
            post.unit_number = None
        post.save()
        return redirect('th_all')
    
    content = {'form': form, }
    return render(request, 'th_new.html', {**content, **rights, **urls})


@login_required
def event_new(request, unit_id):
    '''Добавить новое событие для уч. единицы'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    event = Event()
    event.unit_name_id = unit_id
    form = EventForm(request.POST or None,
                     files=request.FILES or None,
                     instance=event)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.unit_name_id = unit_id
        post.date += dt.timedelta(hours=12) # из-за timezone
        post.save()
        return redirect('unit_ths', unit_id)
    content = {'form': form, }
    return render(request, 'storage_event_new.html', {**content, **rights, **urls})


@login_required
def event_edit(request, event_id, unit_id):
    '''Редактировать событие для уч. единицы'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    event = Event.objects.filter(id=event_id)[0]
    event.unit_name_id = unit_id
    event.date =str(event.date)[:-15]
    form = EventForm(request.POST or None,
                     files=request.FILES or None,
                     instance=event)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user.username
        post.unit_name_id = unit_id
        post.date += dt.timedelta(hours=12) # из-за timezone
        post.save()
        return redirect('unit_ths', unit_id)
    content = {'form': form, 'edit': True,}
    return render(request, 'storage_event_new.html', {**content, **rights, **urls})


@login_required
def event_delete(request, event_id, unit_id):
    '''Удалить событие для уч. единицы'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('unit_ths', unit_id)


@login_required
def event_copy(request, event_id, unit_id):
    '''Копировать событие для уч. единицы'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    event = get_object_or_404(Event, id=event_id)
    latest_id = Event.objects.all().latest('id').id
    new_event = event
    new_event.id = latest_id + 1
    new_event.save()
    return redirect('unit_ths', unit_id)


def isdigit(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


@login_required
def th_edit(request, th_id):
    '''Редактировать накладную'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    th = get_object_or_404(Th, id=th_id)
    th.day = str(th.day)[:-15]
    
    form = ThForm(request.POST or None,
                    files=request.FILES or None,
                    instance=th)
    if form.is_valid():
        th = form.save(commit=False)
        if not isdigit(th.unit_number):
            th.unit_number = None
        th.save()
        return redirect('th_all')
    content = {'form': form, 'th': th, 'edit': True, }
    return render(request, 'th_new.html', {**content, **rights, **urls})


@login_required
def th_delete(request, th_id):
    '''Удалить накладную'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    th = get_object_or_404(Th, id=th_id)
    try:
        if th.th != "":
            os.remove(settings.MEDIA_ROOT + th.th.url) # нужно менять адрес храрения с кириллицы на латиницу
            print(f'Файл {settings.MEDIA_ROOT + th.th.url} успешно удален')
    except:
        print(f'Не удалось удалить файл {settings.MEDIA_ROOT + "/" + th.th.url}')
    th.delete()
    return redirect('th_all')


def main(request): # необходимо переименовать все связанное с этим и это
    '''перечень учетных единиц'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    unit_list = Unit.objects.all()
    paginator = Paginator(unit_list, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    favorit_units = User_units.objects.filter(user_id=request.user.id)
    favorit_units_ids = [u.unit_id for u in favorit_units ]
    content = {'page': page, 'favorit_units_ids': favorit_units_ids, 'page_name': 'Корреспонденция',}
    return render(request, 'main.html', {**content, **rights, **urls})


def main_likes(request): # необходимо переименовать все связанное с этим и это
    '''перечень учетных единиц'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    unit_list = Unit.objects.all()
    favorit_units = User_units.objects.filter(user_id=request.user.id)
    favorit_units_ids = [u.unit_id for u in favorit_units]
    units = []
    for unit in unit_list:
        if unit.id in favorit_units_ids:
            units.append(unit)

    paginator = Paginator(units, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    content = {'page': page, 'favorit_units_ids': favorit_units_ids, }
    return render(request, 'main.html', {**content, **rights, **urls})


def unit_like(request, unit_id):
    user_unit = User_units.objects.filter(user_id=request.user.id, unit_id=unit_id)
    if len(user_unit) == 0:
        new_user_unit = User_units()
        new_user_unit.user_id=request.user.id
        new_user_unit.unit_id=unit_id
        new_user_unit.save()
    elif len(user_unit) == 1:
        user_unit[0].delete()
    return redirect(request.META.get('HTTP_REFERER'))


def units_search(request):
    q = request.GET.get("q")
    if q != "":
        units = Unit.objects.filter(Q(name__icontains=q) | Q(code__icontains=q) | Q(number__icontains=q))  # не работает с Foreign key
    else:
        units = []
    #passes = Pass.objects.filter(sec_name__icontains=q)
    #paginator = Paginator(units, 10)
    #page_number = request.GET.get('page')
    #page = paginator.get_page(page_number)
    content = {'page': units, }
    return render(request, 'main.html', {**content, **rights, **urls})


def units_by_ctgry(request, ctgry_id):
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    units_by_ctgry = Unit.objects.filter(ctgry_id=ctgry_id)
    paginator = Paginator(units_by_ctgry, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    content = {'page': page, }
    return render(request, 'main.html', {**content, **rights, **urls})


def units_by_creator(request, creator_id):
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    units_by_creator = Unit.objects.filter(creator_id=creator_id)
    paginator = Paginator(units_by_creator, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    content = {'page': page, }
    return render(request, 'main.html', {**content, **rights, **urls})


def units_by_place(request, place_id):
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    units_by_place = Unit.objects.filter(place_id=place_id)
    paginator = Paginator(units_by_place, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    content = {'page': page, }
    return render(request, 'main.html', {**content, **rights, **urls})

def unit_ths(request, id):
    '''Перечень событий учетной еденицы'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    
    unit = get_object_or_404(Unit, id=id)
    events = Event.objects.filter(unit_name_id=id)
    ''' Добавить после актализации всех количеств
    plus, minus = 0, 0
    for event in events:
        if event.event_name_id in [1, 4]:
            plus += event.num
        elif event.event_name_id in [2, 3]:
            minus += event.num
    result = plus - minus
    '''
    ths_ids = []
    for event in events:
        ths_ids.append(event.th_name_id)
    ths = Th.objects.filter(id__in=ths_ids)
    #num_all = unit.units.all().aggregate(total_sum=Sum('num'))
    #unit.num = num_all['total_sum']
    #unit.save()
    # returns {'total_sum': 1000} for example

    
    paginator = Paginator(events, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    favorit_units = User_units.objects.filter(user_id=request.user.id)
    favorit_units_ids = [u.unit_id for u in favorit_units ]   

    content = {
        'unit': unit,
        'page': page,
        'ths_ids': ths_ids,
        'ths': ths,
        'favorit_units_ids': favorit_units_ids,
    } #'num_all': num_all, }
    return render(request, 'unit.html', {**content, **rights, **urls})


def th_all(request):
    '''Перечень накладных'''
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    th_list = Th.objects.all()
    paginator = Paginator(th_list, 24)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    content = {'page': page, **data()}
    
    return render(request, 'th_all.html', {**content, **rights, **urls})


def th_all_year(request, year):
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    th_list = Th.objects.filter(year=year)
    paginator = Paginator(th_list, 24)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    content = {'page': page, **data(),}
    return render(request, 'th_all.html', {**content, **rights, **urls})


def th_all_type(request, type_th):
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
 
    th_list = Th.objects.filter(type_th=type_th)
    paginator = Paginator(th_list, 24)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    content = {'page': page, **data(),}
    return render(request, 'th_all.html', {**content, **rights, **urls})


def th_all_tag(request, tag_id):
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    th_by_tag_id = Th_tags.objects.filter(tag_id=tag_id)
    ths = []
    for el in th_by_tag_id:
        ths.append(el.th_id)
        
    th_list = Th.objects.filter(id__in=ths)
    paginator = Paginator(th_list, 24)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    content = {'page': page, **data(),}
    return render(request, 'th_all.html', {**content, **rights, **urls})


@login_required
def place_new(request):
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    form = PlaceForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        place = form.save(commit=False)
        place.save()

        return redirect('storage')
    content = {'form': form, 'var': 'Место хранения', **data(), }
    return render(request, 'some_new.html', {**content, **rights, **urls})


@login_required
def creator_new(request):
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    form = CreatorForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        creator = form.save(commit=False)
        creator.save()

        return redirect('storage')
    content = {'form': form, 'var': 'Производителя', **data(), }
    return render(request, 'some_new.html', {**content, **rights, **urls})


@login_required
def ctgry_new(request):
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    form = CtgryForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        ctgry = form.save(commit=False)
        ctgry.save()
        return redirect('storage')
    content = {'form': form, 'var': 'Категорию', **data(), }
    return render(request, 'some_new.html', {**content, **rights, **urls})



@login_required
def si_new(request):
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    form = SiForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        si = form.save(commit=False)
        si.save()
        return redirect('storage')
    content = {'form': form, 'var': 'Еденицу измерения', **data(), }
    return render(request, 'some_new.html', {**content, **rights, **urls})


@login_required
def stend_new(request):
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    form = StendForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        stend = form.save(commit=False)
        stend.save()
        return redirect('storage')
    content = {'form': form, 'var': 'Стенд', **data(), }
    return render(request, 'some_new.html', {**content, **rights, **urls})


def storage_where(request, place):
    
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    place = str(place)[0]
    content = {place: 'red', **data(), 'page_name': 'Склад',}
    return render(request, 'storage.html', {**content, **rights, **urls})


@login_required
def tag_new(request):
    if not stor_access_check(request):
        return render(request, 'no_rights.html',)
    form = TagForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('th_all')
    content = {'form': form, 'var': 'Тег', }
    return render(request, 'some_new.html', {**content, **rights, **urls})


@login_required
def tag_add(request, th_id):

    if not stor_access_check(request):
        return render(request, 'no_rights.html',)

    new = Th_tags()
    new.th_id = th_id
    form = Tag_addForm(request.POST or None,
                   files=request.FILES or None,
                   instance=new)
    if form.is_valid():
        form.save()
        return redirect('th_all')

    content = {'form': form, 'var': 'Запись', }

    return render(request, 'some_new.html', {**content, **rights, **urls})

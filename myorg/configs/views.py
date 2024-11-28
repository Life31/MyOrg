#from asyncio.windows_events import NULL
import datetime as dt
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .forms import (
    UnitForm, IncludeForm, ConfigForm, ChangeForm,
    ConfigurationForm, Changes_confirmForm
)
from .models import (
    Unit, Include, Config, Number, Query, Change,
    Configuration, Changes, Changes_confirm
)


def some_data():
    content = {
        'cur_conf_num': Number.objects.all().latest('id'),
        'config_numbers': Number.objects.all(),
    }
    return content


def rights():
    content = {'rights': settings.RIGHTS,
            'storage_rights': settings.STORAGE_RIGHTS,
            'sadec_rights': settings.SADEC_RIGHTS,
            'pro_rights': settings.PRO_RIGHTS,
            'passes_rights': settings.PASSES_RIGHTS,
            **some_data(), # не работает тут, отрабатывает только при старте
            }
    return content

urls = {'urls':{
    'config_units_all', 'config_current_config',
    'config_new_changes', 'config_changes_cur',
    'config_new_unit', 'config_units',
    },
}

#---------------------------------------------------------new
@login_required
def config_new_unit(request):
    '''Функция добавления блока'''
    unit =  Unit()
    form = UnitForm(request.POST or None,
                    files=request.FILES or None,
                    instance=unit, )
    content = {'form': form, }
    if form.is_valid():
        unit = form.save(commit=False)
        unit.author = request.user
        unit.pub_date = dt.datetime.now()
        unit.save()
        number = Number.objects.all().latest('id')
        #
        change_conf = Changes_confirm()
        change_conf.unit_id = unit.id
        change_conf.parametr = "Монтаж"
        change_conf.part_n = unit.part_n
        change_conf.other_info = "Монтаж" 
        change_conf.descr = str(dt.datetime.now().date())
        change_conf.number = number
        change_conf.save()

        return redirect('config_current_config')
    return render(request, 'config_new_unit.html', {**content, **rights(), **urls})


@login_required
def config_new_parametr(request, unit_id):
    '''Функция добавления параметра'''
    param = Configuration()
    param.unit_id = unit_id
    
    form = ConfigurationForm(request.POST or None,
                    files=request.FILES or None,
                    instance=param, )
    content = {'form': form, }
    if form.is_valid():
        param = form.save(commit=False)
        #param.number_id = Number.objects.all().latest('id').id
        param.save()

        change =  Changes_confirm()
        config = Configuration.objects.all().latest('id')
        change.parametr = config.parametr
        change.part_n = config.part_n
        change.other_info = config.other_info
        change.descr = config.descr
        change.doc = config.doc
        change.number_id = Number.objects.all().latest('id').id
        change.unit = config.unit
        change.save()

        return redirect('config_current_config')
    else:
        print(form.errors.as_data())
    return render(request, 'config_new_param.html', {**content, **rights(), **urls})


@login_required
def config_new_changes(request, config_id):
    '''Функция создания изменения'''
    change =  Changes()
    config = get_object_or_404(Configuration, id=config_id)
    change.parametr = config.parametr
    change.part_n = config.part_n
    change.other_info = config.other_info
    change.descr = config.descr
    change.doc = config.doc
    change.number = config.number
    change.unit = config.unit
    change.save()
    return redirect('config_current_config')


@login_required
def config_new_changes_confirm(request, changes_id):
    '''Функция внесения изменения'''
    param = Changes_confirm()
    change = get_object_or_404(Changes, id=changes_id)
    param.unit = change.unit
    param.number = change.number
    param.parametr = change.parametr
    param.part_n = change.part_n
    param.other_info = change.other_info
    param.descr = change.descr
    param.doc = change.doc
    
    form = Changes_confirmForm(
        request.POST or None,
        files=request.FILES or None,
        instance=param,
    )
    content = {'form': form, }
    if form.is_valid():
        param = form.save(commit=False)
        param.save()
        return redirect('config_current_config')
    else:
        print(form.errors.as_data())
    return render(request, 'config_new_param.html', {**content, **rights(), **urls})


@login_required
def config_new_config(request):
    '''Функция создания новой конфигурации'''
    try:
        number = Number.objects.all().latest('id')
    except:
        number = 1
    #
    new_number = Number()
    new_number.number = str(int(number.number) + 1)
    new_number.save()
    #
    current = Configuration.objects.filter(number=number)
    changes_confirm = Changes_confirm.objects.filter(number=number)
    changes_confirm_ids =[]
    for c in current:
        for cc in changes_confirm:
            if c.unit == cc.unit and c.parametr == cc.parametr:
                changes_confirm_ids.append(c.id)
    #
    for cc in changes_confirm:
        new_c = Configuration()
        new_c.parametr = cc.parametr
        new_c.part_n = cc.part_n
        new_c.other_info = cc.other_info
        new_c.descr = cc.descr
        new_c.doc = cc.doc
        new_c.parametr = cc.parametr
        new_c.unit = cc.unit
        new_c.number_id = new_number.id
        new_c.save()
        
    #
    for c in current:
        if c.id not in changes_confirm_ids:
            new_c = Configuration()
            new_c.parametr = c.parametr
            new_c.part_n = c.part_n
            new_c.other_info = c.other_info
            new_c.descr = c.descr
            new_c.doc = c.doc
            new_c.parametr = c.parametr
            new_c.unit = c.unit
            new_c.number_id = new_number.id
            new_c.save()
    #
    return redirect('config_current_config')


def config_units_all(request):
    '''Перечень блоков'''
    number = Number.objects.all().latest('id')

    content = {
        'units': Unit.objects.all(),
        'config': Configuration.objects.filter(number=number),
    }
    return render(
        request,
        'config_units_all.html',
        {**content, **rights(), **urls}
    )


def config_current_config(request):
    '''Текущая конфигурация'''
    try:
        number = Number.objects.all().latest('id')
    except:
        number = 1
    cc_ids = []
    for c in Changes.objects.filter(number=number):
        for cc in Changes_confirm.objects.filter(number=number):
            if c.unit == cc.unit and c.parametr == cc.parametr:
                cc_ids.append(c.id)
    conf_ids = []
    for c in Configuration.objects.filter(number=number):
        for cc in Changes.objects.filter(number=number):
            if c.unit == cc.unit and c.parametr == cc.parametr:
                conf_ids.append(c.id)
    units_with_conf = []
    for c in Configuration.objects.filter(number=number):
        units_with_conf.append(c.unit_id)
    content = {
        'number': number,
        'units': Unit.objects.all(),
        'units_with_conf': units_with_conf,
        'changes': Changes.objects.filter(number=number),
        'already_confirm': cc_ids,
        'already_change': conf_ids,
        'changes_confirm': Changes_confirm.objects.filter(number=number),
        'current': Configuration.objects.filter(number=number),
    }
    return render(request, 'config_current_config.html', {**content, **rights(), **urls})


def config_changes_cur(request, number):
    '''Изменения текущей конфигурации'''
    try:
        number = Number.objects.filter(number=str(int(number) - 1))[0]
    except:
        number = number
    content = {
        'number': number,
        'changes': Changes.objects.filter(number=number),
        'changes_confirm': Changes_confirm.objects.filter(number=number),
    }
    return render(request, 'config_current_changes.html', {**content, **rights(), **urls})


def config_re_unit(request, unit_id):
    '''Удалить блок'''
    unit = get_object_or_404(Unit, id=unit_id)

    number = Number.objects.all().latest('id')
        #
    change_conf = Changes_confirm()
    change_conf.parametr = unit.unit_type
    change_conf.part_n = unit.part_n
    change_conf.other_info = unit.unit_type + "Удален"
    change_conf.descr = str(dt.datetime.now().date())
    change_conf.number = number
    change_conf.save()

    unit.delete()
    return redirect('config_current_config')

def config_re_confirm(request, confirm_id):
    '''Отмена подтвержденного изменения'''
    confirm = get_object_or_404(Changes_confirm, id=confirm_id)
    confirm.delete()
    return redirect('config_current_config')

def config_re_change(request, change_id):
    '''Отмена запроса изменения'''
    change = get_object_or_404(Changes, id=change_id)
    change.delete()
    return redirect('config_current_config')


def config_units(request, number): # аккордеон
    '''Все блоки + Текущая конфигурация'''
    try:
        number = Number.objects.filter(number=number)[0]
    except:
        number = 1
    changes = []
    if Number.objects.filter(number=int(number.number)-1).count() > 0:
        before_conf = Number.objects.filter(number=int(number.number)-1)[0]
        if Query.objects.filter(state="Принят", number_id=before_conf.id).count() > 0:
            query = Query.objects.filter(state="Принят", number_id=before_conf.id)[0].id
            print(query)
            ch = Change.objects.filter(number_id=query)

            for i in range(ch.count()):
                changes.append(ch[i].include_name_id)
            print(changes)
    content = {
        'units': Unit.objects.all(),
        'current': Configuration.objects.filter(number=number),
        'number': number,
        'changes': changes,
        }
    return render(request, 'config_units.html', {**content, **rights(), **urls})


@login_required
def config_sib(request):
    number = Number.objects.all().latest('id')
    print('number: ', number)
    units_in_current_config = Configuration.objects.filter(number=number)
    
    data = {}
    for u in units_in_current_config:
        if u.parametr == "Монтаж":
            print('unit: ', str(u.unit).replace(' ', '_').replace('#', '_'))
            data[str(u.unit).replace(' ', '_').replace('#', '_')] = u.other_info
    
    units = Unit.objects.all()
    data_u = {}
    for u in units:
        data_u[str(u.unit_type).replace(' ', '_').replace('#', '_')] = {
            'unit_type': u.unit_type,
            'serial_n': u.serial_n,
            'part_n': u.part_n,
            'descr': u.descr,
            'pos_on_stor': u.pos_on_storage,

            }
        if u.doc is not None and  u.doc != "":
            data_u[str(u.unit_type).replace(' ', '_').replace('#', '_')]['doc'] = u.doc.url
        else:
            data_u[str(u.unit_type).replace(' ', '_').replace('#', '_')]['doc'] = '-'

    #for k, v in data_u.items():
    #    print(k, v)
    return render(request, 'config_sib.html', {**data, 'json_data': json.dumps([data, data_u]), **rights(), **urls})
#---------------------------------------------------------new

@login_required
def config_new_include(request, unit_id):
    '''Функция добавления блока'''
    include =  Include()
    include.unit_id = unit_id
    form = IncludeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=include, 
    )
    content = {'form': form, }
    if form.is_valid():
        form.save()
        return redirect('current')
    return render(request, 'config_new_include.html', {**content, **rights(), **urls})


def current(request):
    '''Текущая конфигурация'''
    try:
        number = Number.objects.all().latest('id')
    except:
        number = 1
    content = {'current': Config.objects.filter(number=number),}
    return render(request, 'config_current.html', {**content, **rights(), **urls})


def config_querys(request):
    '''Запросы на изменение конфигурации'''
    querys = Query.objects.all().exclude(state="Принят")
    content = {'querys': querys,}
    return render(request, 'config_querys.html', {**content, **rights(), **urls})


@login_required
def config_query_creat(request):
    '''Создать запрос на изменение конфигурации'''
    querys = Query.objects.filter(author=request.user).exclude(state="Принят")
    if len(querys) == 0:
        query = Query()
        try:
            query.number = Number.objects.all().latest('id')
        except:
            return redirect('current')
            #query.number = 1
        query.state = "Создан"
        query.author = request.user
        query.save()
    return redirect('config_querys', )


def config_changes(request, query_id):
    '''Создать запрос на изменение конфигурации'''
    changes = Change.objects.filter(number_id=query_id)
    #changes = Change.objects.all()
    content = {'changes': changes, 'query_id': query_id, }
    return render(request, 'config_changes.html', {**content, **rights(), **urls})    


@login_required
def config_changes_confirm(request, query_id):
    current_number = Number.objects.all().latest('id').id
    current_config = Config.objects.filter(number_id=current_number)
    new_number= Number()
    new_n = str(int(Number.objects.all().latest('id').number) + 1)
    new_number.number = new_n
    new_number.save()
    
    changes = Change.objects.filter(number_id=query_id)
    check ={}
    for ch in changes:
        if ch.state == "Изменить":
            new_config = Config()
            new_config.unit = ch.unit
            new_config.include_name = ch.include_name
            new_config.part_n = ch.part_n
            new_config.other_info = ch.other_info
            new_config.descr = ch.descr
            new_config.doc = ch.doc
            new_config.number_id = Number.objects.filter(number=new_n)[0].id

            new_config.pub_date = ch.pub_date
            new_config.author = ch.author
            new_config.save()
            if ch.unit not in check.keys():
                check[ch.unit] = []
            check[ch.unit].append(ch.include_name)

    for cur_con in current_config:
        if not (cur_con.unit in check.keys() and
                cur_con.include_name in check[cur_con.unit]):
            new_config = Config()
            new_config.unit = cur_con.unit
            new_config.include_name = cur_con.include_name
            new_config.part_n = cur_con.part_n
            new_config.other_info = cur_con.other_info
            new_config.descr = cur_con.descr
            new_config.doc = cur_con.doc
            new_config.number_id = Number.objects.filter(number=new_n)[0].id
            new_config.pub_date = cur_con.pub_date
            new_config.author = cur_con.author
            new_config.save()
            
    query = Query.objects.filter(id=changes[0].number_id)[0]
    query.state = "Принят"
    query.save()
    return redirect('config_querys', )


@login_required
def config_new_change(request):
    '''Функция создания изменения'''
    change =  Change()
    form = ChangeForm(request.POST or None,
                    files=request.FILES or None,
                    instance=change, )
    content = {'form': form, }
    if form.is_valid():
        change = form.save(commit=False)
        change.author = request.user
        change.pub_date = dt.datetime.now()
        change.save()
        return redirect('current')
    return render(request, 'config_new_change.html', {**content, **rights(), **urls})


@login_required
def config_from_conf_to_change(request, conf_id):
    if len(Query.objects.filter(author_id=request.user.id, state="Создан")) > 0:
        config = Config.objects.filter(id=conf_id)[0]
        change =  Change()
        change.number_id = Query.objects.filter(author_id=request.user.id, state="Создан")[0].id
        change.unit = config.unit
        change.include_name = config.include_name
        change.part_n = config.part_n
        change.other_info = config.other_info
        change.descr = config.descr
        change.doc = config.doc
        change.pub_date = dt.datetime.now()
        change.author = request.user
        change.state = "Изменить"
        change.save()
        return redirect('current')

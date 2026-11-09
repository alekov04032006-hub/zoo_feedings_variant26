import logging
import sqlite3
from functools import wraps
from django.http import Http404
from django.shortcuts import render
from . import db
logger = logging.getLogger(__name__)

def database_errors(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        try:
            return view(request, *args, **kwargs)
        except (sqlite3.Error, ValueError, OSError):
            logger.exception('Ошибка чтения базы кормлений')
            return render(request, 'database_error.html', status=503)
    return wrapped

def number(request, name, default, minimum, maximum):
    raw = request.GET.get(name, '').strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        raise ValueError(f'Поле «{name}»: введите целое число.')
    if not minimum <= value <= maximum:
        raise ValueError(f'Поле «{name}»: допустимо от {minimum} до {maximum}.')
    return value

@database_errors
def feeding_list(request):
    context = {'sorts': [(key, value[1]) for key, value in db.SORTS.items()],
               'visitors': request.GET.get('visitors', ''),
               'limit': request.GET.get('limit', ''), 'sort': request.GET.get('sort', 'date')}
    try:
        visitors = number(request, 'visitors', 0, 0, 1000000)
        limit = number(request, 'limit', -1, 1, 1000)
        if context['sort'] not in db.SORTS:
            raise ValueError('Выберите сортировку из списка.')
    except ValueError as error:
        context.update(error=str(error), feedings=[])
        return render(request, 'feedings/feeding_list.html', context, status=400)
    context['feedings'] = db.get_feedings(visitors, context['sort'], limit)
    return render(request, 'feedings/feeding_list.html', context)

@database_errors
def feeding_detail(request, slug):
    feeding = db.get_feeding(slug)
    if feeding is None:
        raise Http404('Кормление не найдено')
    return render(request, 'feedings/feeding_detail.html', {'feeding': feeding})

@database_errors
def statistics(request):
    try:
        minimum = number(request, 'min_count', 2, 1, 1000000)
    except ValueError as error:
        return render(request, 'feedings/statistics.html', {'error': str(error)}, status=400)
    return render(request, 'feedings/statistics.html',
                  {'groups': db.get_statistics(minimum), 'min_count': minimum,
                   'total': db.count_feedings()})

def page_not_found(request, exception):
    return render(request, '404.html', status=404)

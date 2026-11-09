"""SQLite → SQL → словари Python. Каждый вызов открывает и закрывает соединение."""
from contextlib import closing
from datetime import datetime
from pathlib import Path
import re
import sqlite3
from django.conf import settings

# Этот же файл запросов используется работающим приложением.
SQL_TEXT = (Path(__file__).resolve().parent.parent / 'sql/queries.sql').read_text(encoding='utf-8')
QUERIES = {name: sql.strip() for name, sql in re.findall(
    r'-- name: (\w+)\n(.*?)(?=-- name:|\Z)', SQL_TEXT, re.S)}
SORTS = {
    'date': ('f.feed_date ASC, f.id ASC', 'По дате: сначала ранние'),
    'date_desc': ('f.feed_date DESC, f.id ASC', 'По дате: сначала поздние'),
    'visitors': ('f.visitors DESC, f.id ASC', 'По посетителям: по убыванию'),
    'visitors_asc': ('f.visitors ASC, f.id ASC', 'По посетителям: по возрастанию'),
    'title': ('f.title ASC, f.id ASC', 'По названию'),
}

def query(sql, parameters=()):
    # mode=rw не создаёт пустую БД, если исходный файл пропал.
    uri = Path(settings.FEEDINGS_DB).resolve().as_uri() + '?mode=rw'
    with closing(sqlite3.connect(uri, uri=True, timeout=5)) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA foreign_keys = ON')
        rows = [dict(row) for row in connection.execute(sql, parameters).fetchall()]
    for row in rows:
        if 'feed_date' in row:
            row['feed_date'] = datetime.fromisoformat(row['feed_date'])
    return rows

def get_aviaries():
    return query(QUERIES['aviaries'])

def count_feedings():
    return query(QUERIES['count'])[0]['total']

def get_feedings(visitors=0, sort='date', limit=-1):
    # Пользовательский ввод не становится именем SQL-поля.
    order_by = SORTS.get(sort, SORTS['date'])[0]
    return query(QUERIES['list'].format(order_by=order_by), (visitors, limit))

def get_feeding(slug):
    rows = query(QUERIES['detail'], (slug,))
    return rows[0] if rows else None

def get_statistics(min_count=2):
    return query(QUERIES['statistics'], (min_count,))

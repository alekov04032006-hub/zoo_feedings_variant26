# Контрольная работа № 2 — вариант 26 «Кормления в зоопарке»

Автор: Ковалишин Александр Александрович.

Готовый Django-проект: 4 связанных вольера, 8 кормлений, SQLite без ORM.
Даты и статусы — учебные данные; статус хранится в БД, а не вычисляется по часам.

## Запуск в Windows

Нужен Python 3.10 или новее. Распакуйте архив полностью.
Самый быстрый запуск: откройте `start_windows.bat`, затем http://127.0.0.1:8000/.
Для первого запуска нужен интернет, чтобы установить Django.

Или вручную **в Windows PowerShell, в папке zoo_feedings, где лежит manage.py**:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe init_db.py
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test feedings
.\.venv\Scripts\python.exe manage.py runserver --insecure
```

Активация окружения не требуется. Остановка: Ctrl+C.
База уже в архиве; init_db.py при её наличии сохраняет данные.
Миграции и суперпользователь не требуются. DEBUG=False нужен для собственной 404;
`--insecure` обслуживает CSS, PNG и JS локальным сервером при DEBUG=False.
Это режим локальной демонстрации контрольной.

**В терминале Ubuntu/VirtualBox**, если запускаете проект там:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python init_db.py
.venv/bin/python manage.py check
.venv/bin/python manage.py test feedings
.venv/bin/python manage.py runserver --insecure
```

Браузер открывайте внутри Ubuntu; при запуске на Windows используйте браузер Windows.

## Страницы и проверка

| Действие | Адрес / результат на исходной базе |
|---|---|
| Главная | `/` — всего 8 кормлений |
| Вольеры | `/aviaries/` — 4 записи |
| Список | `/feedings/` — 8 карточек, сведения о вольерах |
| Минимум 25 | `/feedings/?visitors=25` — 6 карточек |
| Минимум 50 | `/feedings/?visitors=50` — 2 карточки |
| Нет результатов | `/feedings/?visitors=9999` — понятное сообщение |
| Сортировка и LIMIT | `/feedings/?sort=visitors&limit=3` — 70, 60, 45 посетителей |
| Обратная сортировка | `/feedings/?sort=visitors_asc&limit=3` — 12, 18, 25 |
| Детальная страница | `/feedings/penguin-feeding/` |
| Неизвестный slug | `/feedings/absent/` — HTTP 404 |
| Статистика | `/feedings/statistics/` — 3, 3 и 2 кормления по типам |
| HAVING | `/feedings/statistics/?min_count=3` — два типа; `min_count=4` — пусто |
| Некорректный ввод | `/feedings/?visitors=abc` — сообщение, HTTP 400 |
| JavaScript | Нажмите «О вольере», затем «Скрыть сведения» |

## SQL → Python → Django → HTML

`sql/queries.sql` загружается модулем `feedings/db.py`. `get_feedings()` подставляет
в ORDER BY только фрагмент из словаря SORTS, а числа передаёт отдельно:
`connection.execute(sql, (visitors, limit))`. `query()` возвращает словари;
`feeding_list()` передаёт их в context; цикл шаблона включает `feeding_card.html`.
Дата превращается в datetime для фильтра date. Используются date, default, upper,
truncatechars и length. Каждый запрос закрывает соединение через closing.
Данные при следующем HTTP-запросе читаются заново, без кеширования.

Полная демонстрация и соответствие критериям — в `DEMONSTRATION.md`.
SQL-консоль работает через стандартный Python sqlite3; отдельный SQLite не нужен.

Официальная справка по static:
https://docs.djangoproject.com/en/5.2/howto/static-files/

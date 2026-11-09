# Порядок защиты по контрольной

Используйте исходную базу. Все адреса ниже дописываются к http://127.0.0.1:8000.
Скриншоты не названы обязательными в контрольной; требуется живая демонстрация результата и кода.

1. **Windows PowerShell, папка проекта:** ` .\.venv\Scripts\python.exe manage.py check`.
   Запустите ` .\.venv\Scripts\python.exe manage.py runserver --insecure`.
   Покажите главную, навигацию и 4 вольера.
2. Откройте список кормлений, названия, виды, дату, продолжительность, посетителей,
   статусы и связанный вольер. В коде: `feedings/db.py`, `sql/queries.sql`,
   `feedings/views.py`, `feeding_list.html`, `includes/feeding_card.html`.
3. Покажите `?visitors=25`, затем `?visitors=50`, затем `?visitors=9999`.
   В коде: request.GET, number(), execute(sql, parameters), for/empty.
4. Покажите `?sort=visitors&limit=3`, затем `?sort=visitors_asc&limit=3`.
   В коде: белый список SORTS, ORDER BY и LIMIT.
5. Перейдите по ссылке карточки на `/feedings/penguin-feeding/`, вернитесь к списку.
   В коде: `<slug:slug>`, именованный URL и `{% url %}`, поиск по `WHERE f.slug = ?`.
6. Откройте `/feedings/absent/`. Получите страницу 404.
7. Для ошибки БД **во втором Windows PowerShell в папке проекта**, когда сервер работает:
   `Rename-Item data\feedings.db feedings.db.bak`.
   Обновите список: понятная страница с HTTP 503 без traceback.
   Затем обязательно восстановите: `Rename-Item data\feedings.db.bak feedings.db`.
   В коде: database_errors, обработка исключения и database_error.html.
8. Покажите base.html, extends, include и статус через if/elif, а также фильтры
   date, default, upper, truncatechars, length. В списке есть все три статуса.
9. Покажите статистику `?min_count=3` и `?min_count=4`.
   Откройте SQL COUNT / GROUP BY / HAVING в queries.sql и вызов из statistics().
10. **Во втором Windows PowerShell, папка проекта:** запустите
    ` .\.venv\Scripts\python.exe sql_console.py`.
    Это прямой доступ к SQLite через sqlite3, отдельно от Django.
    Выполните следующие запросы по одному (каждый завершается `;`):

```sql
SELECT id, name, capacity, aviary_kind FROM aviaries ORDER BY name;
SELECT f.title, f.visitors, a.name FROM feedings f JOIN aviaries a ON a.id=f.aviary_id WHERE f.visitors>=50 ORDER BY f.visitors DESC LIMIT 3;
SELECT COUNT(*) FROM feedings;
SELECT feed_kind, COUNT(*) AS total FROM feedings GROUP BY feed_kind HAVING COUNT(*)>=3 ORDER BY total DESC, feed_kind;
```

Сравните результат с вольерами, списком `?visitors=50&sort=visitors&limit=3`,
главной и статистикой `?min_count=3` соответственно. Значения `?` в queries.sql —
параметры Python sqlite3; в ручных SQL-примерах указаны конкретные значения.

11. В той же SQL-консоли выполните по одной строке из `sql/demo_changes.sql`.
    Консоль фиксирует каждое изменение (commit). Обновите вольеры и кормление
    пингвинов: новое название и 77 посетителей. На главной станет 10 записей.
    Статистика `?min_count=4` теперь покажет вечернее кормление — 4 записи.
    Так подтверждается изменение результата HAVING при добавлении записей.
12. Для возврата исходных демонстрационных данных выполните по одной строке
    `sql/demo_restore.sql`, затем `.quit`. Не запускайте demo_changes.sql повторно
    без восстановления: уникальные slug защищают от дублирования.
13. Покажите CSS, логотип и работающую кнопку «О вольере».
    В коде: `{% load static %}`, style.css, logo.png, main.js и aria-expanded.
14. Закончите полным сценарием: главная → вольеры → кормления → фильтрация → карточка → назад.

## Соответствие 27 критериям

| Критерии | Реализация |
|---|---|
| 1–2 | manage.py, settings.py, data/feedings.db, schema.sql, init_db.py |
| 3–5 | homepage/views.py, home.html, base.html, urls.py |
| 6–10 | db.get_feedings, JOIN, feeding_list.html, feeding_card.html, empty |
| 11–14 | request.GET, number(), параметризованный execute, SORTS, ORDER BY, LIMIT |
| 15–17 | slug-маршрут, feeding_detail, get_feeding, именованные url |
| 18–19 | Http404, handler404, database_errors, шаблоны ошибок |
| 20–22 | base.html, extends, if/elif, фильтры шаблонов |
| 23–25 | get_statistics, COUNT/GROUP BY/HAVING, context; изменение SQLite |
| 26–27 | style.css, logo.png, main.js, интерактивная кнопка |

## Автоматическая проверка

**Windows PowerShell, папка проекта:**
` .\.venv\Scripts\python.exe manage.py test feedings --verbosity 2`.
12 тестов используют отдельную временную БД и не изменяют data/feedings.db.
Проверяются маршруты, JOIN, два фильтра, пустой результат, сортировка, LIMIT,
неверный ввод, SQL-инъекция, 404, 503, HAVING после INSERT, обновление записей,
пустые таблицы, шаблоны и ограничение внешнего ключа.

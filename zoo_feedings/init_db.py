"""Первичное создание БД. Существующую базу скрипт никогда не перезаписывает."""
from contextlib import closing
from pathlib import Path
import sqlite3
BASE = Path(__file__).resolve().parent

def create_database(path):
    path = Path(path)
    if path.exists():
        raise FileExistsError('База уже существует: ' + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as connection:
        connection.executescript((BASE / 'sql/schema.sql').read_text(encoding='utf-8'))
        connection.executemany('INSERT INTO aviaries VALUES (?, ?, ?, ?)', [
            (1, 'Вольер тигров', 60, 'открытый'), (2, 'Павильон пингвинов', 80, 'крытый'),
            (3, 'Террариум рептилий', 30, 'террариум'), (4, 'Вольер жирафов', 100, 'открытый')])
        connection.executemany('INSERT INTO feedings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', [
            (1, 'Кормление пингвинов', 'penguin-feeding', 'демонстрационное', '2026-10-24 12:00:00', 30, 70, 'идёт', 2),
            (2, 'Дневное кормление тигров', 'tiger-lunch', 'дневное', '2026-10-24 13:00:00', 20, 45, 'запланировано', 1),
            (3, 'Вечернее кормление жирафов', 'giraffe-evening', 'вечернее', '2026-10-24 18:00:00', 25, 35, 'запланировано', 4),
            (4, 'Кормление змей в террариуме', 'snake-feeding', 'дневное', '2026-10-23 11:00:00', 15, 12, 'завершено', 3),
            (5, 'Демонстрационное кормление тигров', 'tiger-show', 'демонстрационное', '2026-10-25 14:00:00', 35, 60, 'запланировано', 1),
            (6, 'Дневное кормление жирафов', 'giraffe-lunch', 'дневное', '2026-10-23 12:30:00', 20, 25, 'завершено', 4),
            (7, 'Вечерняя встреча с пингвинами', 'penguin-evening', 'вечернее', '2026-10-23 17:00:00', 25, 18, 'завершено', 2),
            (8, 'Показательное кормление черепах и знакомство с рептилиями', 'turtle-show', 'демонстрационное', '2026-10-25 10:00:00', 40, 28, 'запланировано', 3)])
        connection.commit()

if __name__ == '__main__':
    path = BASE / 'data/feedings.db'
    if path.exists():
        print('База уже существует; данные сохранены.')
    else:
        create_database(path)
        print('Создано: 4 вольера и 8 кормлений.')

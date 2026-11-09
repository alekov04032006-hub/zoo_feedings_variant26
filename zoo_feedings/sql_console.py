"""Консоль SQLite на стандартном Python, в том числе для Windows без sqlite3.exe."""
from contextlib import closing
from pathlib import Path
import sqlite3
BASE = Path(__file__).resolve().parent
print('SQLite: вводите SQL с ; в конце. Выход: .quit. После записи выполняется commit.')
with closing(sqlite3.connect((BASE / 'data/feedings.db').as_uri()+'?mode=rw', uri=True)) as connection:
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys=ON')
    buffer = ''
    while True:
        try:
            line = input('sql> ' if not buffer else '...> ')
        except (EOFError, KeyboardInterrupt):
            break
        if line.strip() == '.quit':
            break
        buffer += line + '\n'
        if not sqlite3.complete_statement(buffer):
            continue
        try:
            cursor = connection.execute(buffer)
            if cursor.description:
                print(' | '.join(c[0] for c in cursor.description))
                for row in cursor.fetchall():
                    print(' | '.join(str(value) for value in row))
            else:
                connection.commit()
                print('Изменено строк:', cursor.rowcount)
        except sqlite3.Error as error:
            connection.rollback()
            print('Ошибка SQL:', error)
        buffer = ''

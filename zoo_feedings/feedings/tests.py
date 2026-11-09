from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
import sqlite3
from django.test import SimpleTestCase, override_settings
from django.urls import reverse
from init_db import create_database
from . import db

class FeedingTests(SimpleTestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'feedings.db'
        create_database(self.path)
        self.settings_override = override_settings(FEEDINGS_DB=self.path, DEBUG=False)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)

    def change(self, sql, params=()):
        with closing(sqlite3.connect(self.path)) as connection:
            connection.execute('PRAGMA foreign_keys=ON')
            connection.execute(sql, params)
            connection.commit()

    def test_pages(self):
        for url in ['/', '/aviaries/', '/feedings/', '/feedings/statistics/', '/feedings/penguin-feeding/']:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_counts_and_join(self):
        self.assertEqual(db.count_feedings(), 8)
        self.assertEqual(len(db.get_aviaries()), 4)
        self.assertEqual(db.get_feeding('penguin-feeding')['aviary_name'], 'Павильон пингвинов')

    def test_filters(self):
        for value, count in [(25, 6), (50, 2), (9999, 0)]:
            response = self.client.get('/feedings/', {'visitors': value})
            self.assertEqual(len(response.context['feedings']), count)
            self.assertTrue(all(f['visitors'] >= value for f in response.context['feedings']))
        self.assertContains(response, 'Кормления не найдены')

    def test_sort_and_limit(self):
        response = self.client.get('/feedings/?sort=visitors&limit=3')
        self.assertEqual([f['visitors'] for f in response.context['feedings']], [70,60,45])
        self.assertEqual(db.get_feedings(sort='visitors_asc')[0]['visitors'], 12)

    def test_invalid_input(self):
        for query in ['visitors=abc','visitors=-1','limit=0','limit=1001',
                      'sort=title%3BDROP+TABLE+feedings','visitors=1+OR+1=1']:
            self.assertEqual(self.client.get('/feedings/?'+query).status_code,400)
        self.assertEqual(db.count_feedings(),8)

    def test_404_and_named_routes(self):
        self.assertEqual(reverse('feedings:detail',args=['penguin-feeding']),'/feedings/penguin-feeding/')
        response = self.client.get('/feedings/absent/')
        self.assertContains(response, 'Кормление не найдено', status_code=404)
        self.assertNotContains(response, 'Traceback', status_code=404)

    def test_database_error(self):
        with override_settings(FEEDINGS_DB=self.path.parent/'missing.db'):
            for url in ['/', '/aviaries/', '/feedings/', '/feedings/statistics/', '/feedings/penguin-feeding/']:
                with self.subTest(url=url), self.assertLogs('feedings.views', level='ERROR'):
                    response=self.client.get(url)
                    self.assertContains(response,'Расписание временно недоступно',status_code=503)
                    self.assertNotContains(response,'Traceback',status_code=503)
            self.assertFalse((self.path.parent/'missing.db').exists())

    def test_statistics_having(self):
        self.assertEqual({g['feed_kind']:g['total'] for g in db.get_statistics(3)},
                         {'дневное':3,'демонстрационное':3})
        self.assertEqual(db.get_statistics(4),[])
        for n in [9,10]:
            self.change("INSERT INTO feedings VALUES (?, ?, ?, 'вечернее', '2026-10-26 18:00:00', 20, 10, 'запланировано', 4)",
                        (n,'Новое кормление',f'extra-{n}'))
        response=self.client.get('/feedings/statistics/?min_count=4')
        self.assertEqual(response.context['groups'],[{'feed_kind':'вечернее','total':4}])
        self.assertContains(response,'Вечернее')
        self.assertEqual(self.client.get('/').context['total'],10)

    def test_updates_visible(self):
        self.change('UPDATE aviaries SET name=? WHERE id=2',('Новый павильон',))
        self.assertContains(self.client.get('/aviaries/'),'Новый павильон')
        self.assertContains(self.client.get('/feedings/penguin-feeding/'),'Новый павильон')
        self.change('UPDATE feedings SET visitors=77 WHERE id=1')
        self.assertContains(self.client.get('/feedings/penguin-feeding/'),'77 чел.')

    def test_empty_tables(self):
        self.change('DELETE FROM feedings')
        self.change('DELETE FROM aviaries')
        self.assertContains(self.client.get('/feedings/'),'Кормления не найдены')
        self.assertContains(self.client.get('/aviaries/'),'Вольеры пока не добавлены')
        self.assertEqual(self.client.get('/').context['total'],0)

    def test_templates_and_filters(self):
        response=self.client.get('/feedings/')
        for template in ['base.html','feedings/feeding_list.html','feedings/includes/feeding_card.html']:
            self.assertTemplateUsed(response,template)
        for text in ['24.10.2026','ДЕМОНСТРАЦИОННОЕ','Скоро начало','Идёт кормление','Кормление прошло']:
            self.assertContains(response,text)

    def test_foreign_key(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.change('UPDATE feedings SET aviary_id=999 WHERE id=1')

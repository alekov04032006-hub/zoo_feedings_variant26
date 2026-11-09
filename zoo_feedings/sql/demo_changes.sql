-- Выполнить в SQLite (например DB Browser for SQLite) и сохранить изменения.
UPDATE aviaries SET name = 'Обновлённый павильон пингвинов' WHERE id = 2;
UPDATE feedings SET visitors = 77 WHERE slug = 'penguin-feeding';
INSERT INTO feedings (title, slug, feed_kind, feed_date, duration, visitors, status, aviary_id)
VALUES ('Вечернее кормление тигров', 'extra-tiger-evening', 'вечернее', '2026-10-26 18:00:00', 20, 32, 'запланировано', 1);
INSERT INTO feedings (title, slug, feed_kind, feed_date, duration, visitors, status, aviary_id)
VALUES ('Вечернее кормление черепах', 'extra-turtle-evening', 'вечернее', '2026-10-26 19:00:00', 15, 16, 'запланировано', 3);

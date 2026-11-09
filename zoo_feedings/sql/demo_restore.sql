-- Удаляются только две записи демонстрации; остальная база сохраняется.
DELETE FROM feedings WHERE slug IN ('extra-tiger-evening', 'extra-turtle-evening');
UPDATE aviaries SET name = 'Павильон пингвинов' WHERE id = 2;
UPDATE feedings SET visitors = 70 WHERE slug = 'penguin-feeding';

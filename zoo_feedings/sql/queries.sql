-- name: aviaries
SELECT id, name, capacity, aviary_kind FROM aviaries ORDER BY name;
-- name: count
SELECT COUNT(*) AS total FROM feedings;
-- name: list
SELECT f.*, a.name AS aviary_name, a.capacity, a.aviary_kind
FROM feedings AS f JOIN aviaries AS a ON a.id = f.aviary_id
WHERE f.visitors >= ?
ORDER BY {order_by}
LIMIT ?;
-- name: detail
SELECT f.*, a.name AS aviary_name, a.capacity, a.aviary_kind
FROM feedings AS f JOIN aviaries AS a ON a.id = f.aviary_id
WHERE f.slug = ?;
-- name: statistics
SELECT feed_kind, COUNT(*) AS total FROM feedings
GROUP BY feed_kind HAVING COUNT(*) >= ? ORDER BY total DESC, feed_kind;

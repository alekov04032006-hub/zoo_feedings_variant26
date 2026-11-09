PRAGMA foreign_keys = ON;
CREATE TABLE aviaries (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL,
 capacity INTEGER NOT NULL CHECK(capacity > 0),
 aviary_kind TEXT NOT NULL CHECK(aviary_kind IN ('открытый','крытый','террариум'))
);
CREATE TABLE feedings (
 id INTEGER PRIMARY KEY, title TEXT NOT NULL, slug TEXT NOT NULL UNIQUE,
 feed_kind TEXT NOT NULL CHECK(feed_kind IN ('дневное','демонстрационное','вечернее')),
 feed_date TEXT NOT NULL, duration INTEGER NOT NULL CHECK(duration > 0),
 visitors INTEGER NOT NULL CHECK(visitors >= 0),
 status TEXT NOT NULL CHECK(status IN ('запланировано','идёт','завершено')),
 aviary_id INTEGER NOT NULL REFERENCES aviaries(id)
);
CREATE INDEX idx_feeding_visitors ON feedings(visitors);

-- SQLITE3 VERSION --
--
--
-- Same schema, just sqlite3 can't read all SQL

CREATE TABLE `emails` (
  `id` INTEGER PRIMARY KEY,
  `from_user_id` INTEGER,
  `to_user_id` INTEGER,
  `subject` VARCHAR(200) DEFAULT 'No Subject',
  `datetime` DATETIME);

CREATE TABLE `users` (
  `id` INTEGER PRIMARY KEY,
  `name` VARCHAR(100),
  `email` VARCHAR(100));
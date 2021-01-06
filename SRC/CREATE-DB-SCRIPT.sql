CREATE TABLE IF NOT EXISTS movie_names (
	id INT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
    genre VARCHAR(100),
    duration INT,
    language VARCHAR(100),
    budget INT,
    year INT
	)

--- create fulltext index
--- create index
--- define primary keys and foreign keys
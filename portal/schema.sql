DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS courses;

CREATE TABLE users (
    id bigserial PRIMARY KEY,
    first_name varchar(50),
    last_name varchar(50),
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);

CREATE TABLE courses (
    id bigserial PRIMARY KEY,
    name text NOT NULL,
    number text UNIQUE NOT NULL,
    description text NOT NULL
);


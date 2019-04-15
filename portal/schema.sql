DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id bigserial PRIMARY KEY,
    first_name varchar(50),
    last_name varchar(50),
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);
<<<<<<< HEAD

CREATE TABLE courses (
    id bigserial PRIMARY KEY,
    course text NOT NULL,
    course_id text UNIQUE NOT NULL,
    course_description text NOT NULL
);
=======
>>>>>>> 64f8f4aca2ca2af280831deee90b65b893a3e9ec

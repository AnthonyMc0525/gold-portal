DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS roster;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id bigserial PRIMARY KEY,
    first_name varchar(50),
    last_name varchar(50),
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);

CREATE TABLE courses (
    course_id bigserial PRIMARY KEY,
    name text NOT NULL,
    number text UNIQUE NOT NULL,
    description text NOT NULL,
    teacher_id bigint NOT NULL REFERENCES users(id)
);

CREATE TABLE sessions (
    id bigserial PRIMARY KEY,
    course_id bigint NOT NULL REFERENCES courses(course_id),
    name text NOT NULL,
    description text NOT NULL,
    start_time time NOT NULL,
    end_time time NOT NULL
);

CREATE TABLE assignments (
    id bigserial PRIMARY KEY,
    name text NOT NULL,
    due_date date NOT NULL,
    description text NOT NULL,
    points numeric NOT NULL,
    course_id bigint NOT NULL REFERENCES courses(course_id)
);

  CREATE TABLE roster (
    session_id bigint REFERENCES sessions(session_id),
    user_id bigint REFERENCES users(id)
  );

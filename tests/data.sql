-- Mock Data For Tests

INSERT INTO users (first_name, last_name, email, password, role)
VALUES ('teacher', 'teacher', 'teacher@stevenscollege.edu', 'qwerty', 'teacher'),
       ('student', 'student', 'student@stevenscollege.edu', 'asdfgh', 'student');

INSERT INTO courses (course, course_id, course_description)
VALUES ('security and profesional ethics', 'CSET 170', 'lml'),
       ('public speaking', 'ENG 221', 'kldnkn');

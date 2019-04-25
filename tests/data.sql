-- Mock Data For Tests

INSERT INTO users (first_name, last_name, email, password, role)
VALUES ('teacher', 'teacher', 'teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$0dsQUPzz$e064b66273cba283847cb5df61ae5160a5bfa573e066c20d476ef45c479d2c53', 'teacher'),
       ('student', 'student', 'student@stevenscollege.edu', 'pbkdf2:sha256:150000$0dsQUPzz$e064b66273cba283847cb5df61ae5160a5bfa573e066c20d476ef45c479d2c53', 'student'),
      ('user1', 'teacher', 'user3@test.com', '
pbkdf2:sha256:150000$E82PvcbL$8b6e318366700f77a993eaff991782bb22686af366a79dd810a5cfc737b49284
', 'student'),
      ('user2', 'teacher', 'user4@test.com', 'pbkdf2:sha256:150000$E82PvcbL$8b6e318366700f77a993eaff991782bb22686af366a79dd810a5cfc737b49284', 'teacher');

INSERT INTO courses (name, number, description, teacher_id)
VALUES ('Web development 2', 'CSET 170', 'lml', 1),
       ('public speaking', 'ENG 221', 'kldnkn', 4);

INSERT INTO sessions (course_id, name, description, start_time, end_time)
VALUES (1, 'A', 'First session', '09:00', '09:50'),
       (2, 'B', 'Second session', '10:00', '10:50');

INSERT INTO assignments (name, due_date, description, student_id, session_id)
VALUES ('Thing to get done', '2018-01-01', 'thing', 1, 1),
       ('other thing', '2018-02-02', 'yes', 2, 2);

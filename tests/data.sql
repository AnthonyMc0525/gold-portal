-- Mock Data For Tests

INSERT INTO users (first_name, last_name, email, password, role)
VALUES ('teacher', 'teacher', 'teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$0dsQUPzz$e064b66273cba283847cb5df61ae5160a5bfa573e066c20d476ef45c479d2c53', 'teacher'), 
       ('student', 'student', 'student@stevenscollege.edu', 'pbkdf2:sha256:150000$CJ1Gz9Xg$33381bb35fb80a5cdd090735159153b1fde323ae60bb106fe5a16a8549a48615', 'student');

INSERT INTO courses (name, number, description)
VALUES ('security and profesional ethics', 'CSET 170', 'lml'),
       ('public speaking', 'ENG 221', 'kldnkn');

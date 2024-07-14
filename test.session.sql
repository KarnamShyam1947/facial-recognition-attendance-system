-- pbkdf2:sha256:600000$mL7DE683PEAp4NLo$e90814cf57597bb10a21c76962ba9acd713f32bdb9ec9403a81f487996b43476

-- CREATE TABLE users (
--     id INT auto_increment,
--     name varchar(100),
--     email varchar(100),
--     password varchar(255),
--     role varchar(10),
--     unique_id varchar(50),
--     primary key(id),
--     unique(email)
-- );

INSERT INTO users(name, email, password, role)
VALUES('Admin', "admin@gmail.com", "pbkdf2:sha256:600000$mL7DE683PEAp4NLo$e90814cf57597bb10a21c76962ba9acd713f32bdb9ec9403a81f487996b43476", "ADMIN");

select * FROM users;

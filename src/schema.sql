DROP table if EXISTS users CASCADE;
DROP table if EXISTS catalogs CASCADE;
DROp PROCEDURE if EXISTS addUser CASCADE;

CREATE TABLE users(
user_id serial primary key not null,
username varchar(50) unique not null,
password varchar(50) not null,
email varchar(70) unique not null,
first_name varchar(50),
last_name varchar(50),
date_created date not null,
last_accessed date not null
);

CREATE TABLE catalogs(
  catalog_id serial primary key not null,
  user_id serial,
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE PROCEDURE addUser(In username varchar, In password varchar, In email varchar, In first_name varchar, In last_name varchar, In date_created date,In last_accessed date)
LANGUAGE sql
AS $$
INSERT INTO users(username, password, email, first_name, last_name, date_created,last_accessed)
VALUES (username, password, email, first_name, last_name, date_created,last_accessed);
$$;


INSERT INTO users(username, password, email, first_name, last_name, date_created,last_accessed) VALUES
 ('as_123','password','as@rit.edu','amelia', 'smith', date('2022-01-02'), date('2022-01-10')),
 ('bj_94','pass_word','bj@gmail.com','bret', 'johnson', date('2022-01-02'), date('2022-01-10')),
 ('user21_21','my_password','cj@yahoo.com','carly', 'jr', date('2022-01-02'), date('2022-01-10')),
 ('d.da','donna_password','donna@gmail.com','donna', 'ng', date('2022-01-02'), date('2022-01-10'));




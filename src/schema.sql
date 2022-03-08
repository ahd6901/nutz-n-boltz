DROP table if EXISTS users CASCADE;
DROP table if EXISTS catalog_tools CASCADE;
DROP table if EXISTS tools CASCADE;
DROP PROCEDURE if EXISTS addUser CASCADE;

CREATE TABLE users(
user_id serial primary key not null,
username varchar(50) unique not null,
password varchar(50) not null,
email varchar(70) unique not null,
first_name varchar(50),
last_name varchar(50),
date_created timestamp not null,
last_accessed timestamp not null
);

create table tools
(
    tool_id serial primary key,
    times_lent     integer not null,
    barcode        char(12) not null,
    name           varchar(128) not null,
    description    varchar(250),
    shareable      boolean default true not null,
    purchase_price float not null,
    purchase_date  date not null,
    available      boolean not null
);

CREATE TABLE catalog_tools (
    owner_id int NOT NULL,
    tool_id int NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(user_id),
    FOREIGN KEY (tool_id) REFERENCES tools(tool_id)
);



CREATE PROCEDURE addUser(In username varchar, In password varchar, In email varchar, In first_name varchar, In last_name varchar, In date_created date,In last_accessed date)
LANGUAGE sql
AS $$
INSERT INTO users(username, password, email, first_name, last_name, date_created,last_accessed)
VALUES (username, password, email, first_name, last_name, date_created,last_accessed);
$$;


INSERT INTO users(username, password, email, first_name, last_name, date_created,last_accessed) VALUES
 ('as_123','password','as@rit.edu','amelia', 'smith', '2020-01-02 20:19:09','2022-01-01 03:10:12'),
 ('bj_94','pass_word','bj@gmail.com','bret', 'johnson', '2021-03-02 14:10:12', '2022-01-02 12:10:12'),
 ('user21_21','my_password','cj@yahoo.com','carly', 'jr', '2022-01-02 12:10:12', '2022-01-03 02:10:12'),
 ('d.da','donna_password','donna@gmail.com','donna', 'ng', '2022-01-02 21:10:12', '2022-02-03 02:10:12');




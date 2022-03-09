DROP table if EXISTS users CASCADE;
DROP table if EXISTS catalog_tools CASCADE;
DROP table if EXISTS tools CASCADE;
DROP table if EXISTS categories CASCADE;
DROP table if EXISTS user_tool_requests CASCADE;
DROP table if EXISTS catalog_tools CASCADE;
DROP table if EXISTS categorized_tools CASCADE;
DROP table if EXISTS recommended_tools CASCADE;
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
create table categories(
	category_id SERIAL PRIMARY KEY,
	owner_id int NOT NULL,
	name varchar(64) NOT NULL,
	constraint owner_category
		Foreign key(owner_id)
			References users(user_id)
);
create table user_tool_requests(
	requesting_user_id INT NOT NULL,
	tool_id INT NOT NULL,
	date_borrowed DATE,
	date_returned DATE,
	date_required DATE NOT NULL,
	status varchar(32) check(status ='accepted' OR status = 'declined' OR status = 'pending') NOT NULL,
	overdue boolean NOT NULL,
	date_status_changed DATE,
	duration INT,
	expected_return_date DATE,
	constraint owner_tool_req
		Foreign key(requesting_user_id)
			References users(user_id),
	constraint tool_id_req
		Foreign key(tool_id)
			References tools(tool_id)
);

CREATE TABLE catalog_tools (
    owner_id int NOT NULL,
    tool_id int NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(user_id),
    FOREIGN KEY (tool_id) REFERENCES tools(tool_id)
);

create table categorized_tools(
	category_id INT NOT NULL,
	tool_id INT NOT NULL,
	constraint tool_categories
		Foreign key(tool_id)
			References tools(tool_id),
	constraint category_ids
		Foreign key(category_id)
			References categories(category_id)
);

create table recommended_tools(
	Recommended_tool_id INT NOT NULL,
	Tool_id INT NOT NULL,

	constraint recommend_tool_id
		Foreign key(tool_id)
			References tools(tool_id)
);


grant delete, insert, references, select, trigger, truncate, update on users, categories, user_tool_requests, catalog_tools, recommended_tools, tools, categorized_tools to nag6917, wam2134, ahd6901;

INSERT INTO users(username, password, email, first_name, last_name, date_created,last_accessed) VALUES
 ('as_123','password','as@rit.edu','amelia', 'smith', '2020-01-02 20:19:09','2022-01-01 03:10:12'),
 ('bj_94','pass_word','bj@gmail.com','bret', 'johnson', '2021-03-02 14:10:12', '2022-01-02 12:10:12'),
 ('user21_21','my_password','cj@yahoo.com','carly', 'jr', '2022-01-02 12:10:12', '2022-01-03 02:10:12'),
 ('d.da','donna_password','donna@gmail.com','donna', 'ng', '2022-01-02 21:10:12', '2022-02-03 02:10:12');




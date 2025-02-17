-- CREATE DATABASE gestionlibros;

USE gestionlibros;

CREATE TABLE admins (
id int unsigned auto_increment primary key,
email varchar(30) NOT NULL,
password varchar(255) NOT NULL,
phone varchar(9) NOT NULL
);


CREATE TABLE books (
id int unsigned auto_increment primary key,
name varchar(30) NOT NULL,
category varchar(30) NOT NULL,
autor varchar(30) NOT NULL,
admin_id int unsigned NOT NULL,

FOREIGN KEY (admin_id) REFERENCES admins(id)
)
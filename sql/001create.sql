drop table if exists link_tags;
drop table if exists link_users;
drop table if exists users; 
drop table if exists tags;  
drop table if exists notes;


create table users(
    id serial primary key,
    user_name text unique not null,
    passwords text not null  
);

create table tags(
    id serial primary key,
    tag_name text
);

create table notes(
    id serial primary key,
    title text,
    note text,
    created_on date
);

create table link_users(
    user_id serial references users(id),
    note serial references notes(id)
);

create table link_tags(
    note serial references notes(id),
    tag serial references tags(id)
);
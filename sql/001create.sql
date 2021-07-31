drop table if exists link_tags;
drop table if exists link_users;
drop table if exists users; 
drop table if exists tags;  
drop table if exists notes;


create table users(
    id serial primary key unique,
    user_name text unique not null,
    passwords text not null  
);

create table notes(
    id serial primary key,
    title text,
    note text,
    tags text,
    created_on date
);

create table link_users(
    u_id  int references users(id) NOT NULL,
    n_id  int references notes(id) NOT NULL
);

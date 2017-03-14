drop table if exists library;
create table library (
    id integer primary key autoincrement,
    name text not null,
    type text not null,
    prep_time integer not null,
    like_it boolean default true
);

drop table if exists pantry;
create table pantry (
    id integer primary key autoincrement,
    quantity integer default 0,
    units text not null,
    alternative text
);

drop table if exists techniques;
create table techniques (
    id integer primary key autoincrement,
    name text not null,
    description text not null,
    link text
);

drop table if exists ingredients;
create table ingredients (
    recipe_id integer not null,
    ingredient text not null,
    quantity integer not null,
    foreign key(recipe_id) references library(id)
);

drop table if exists procedures;
create table procedures (
    recipe_id integer not null,
    step integer not null,
    procedure text not null,
    tech_id integer,
    foreign key(tech_id) references techniques(id),
    foreign key(recipe_id) references library(id)
);

drop table if exists entries;
create table entries (
id integer primary key autoincrement,
name text not null,
emailid text not null,
password text not null,
Designation text not null,
phone_no text not null

);
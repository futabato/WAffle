drop database if exists docker;
create database docker;
use docker;
drop table if exists docker;
create table docker (
    name char(50),
    pass char(50)
);
insert into docker values ("admin", "P@ssw0rd"); 
insert into docker values ("yoden", "Svp3rS3crt3P4sswr0d!!!"); 
insert into docker values ("flag", "flag{7h1s_1s_f4k3_fl4g}"); 

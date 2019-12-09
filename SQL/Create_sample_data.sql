use ats;

delete from department;
delete from applicant;
delete from resume;
delete from employee;
delete from users;
delete from job;
delete from application;
delete from interview;
delete from offer;

insert into department values ('1', 'Engineering');
insert into department values ('2', 'Finance');
insert into department values ('3', 'HR');
insert into department values ('4', 'Marketing');

insert into applicant values ('1', 'encrypted1', 'marianne@gmail.com', 'Marianne Paulson', 'Female', '1984-03-03', 'Active');
insert into applicant values ('2', 'encrypted2', 'mikey@gmail.com', 'Mikey Paulson', 'Male', '2001-12-21', 'Active');
insert into applicant values ('3', 'encrypted3', 'nicholas@gmail.com', 'Nicholas Paulson', 'Male', '1996-06-01', 'Active');
insert into applicant values ('4', 'encrypted4', 'thomas@gmail.com', 'Thomas Paulson', 'Male', '1997-04-07', 'Active');
insert into applicant values ('5', 'encrypted5', 'jim@gmail.com', 'Jim Paulson', 'Male', '1966-10-31', 'Active');

insert into resume values ('1', 'resume1', '1');
insert into resume values ('2', 'resume2', '1');
insert into resume values ('3', 'resume1', '2');

insert into employee values ('1', 'John Kennedy', '2019-03-13', 'Active', '100000', 'Kennedy@gmail.com', '1');
insert into employee values ('2', 'Mary Jones', '2018-03-01', 'Active', '85000', 'Mary@gmail.com', '2');
insert into employee values ('3', 'Hans Iverson', '2017-04-15', 'Active', '100000', 'Hans@gmail.com', '3');

insert into users values ('1', 'Encrypted1', 'Hiring Manager', '1', '1');
insert into users values ('2', 'Encrypted2', 'Recruiter', '2', '2');
insert into users values ('3', 'Encrypted3', 'Administrator', '3', '3');

insert into job values ('1', '2019-09-15', 'Open', 'Software Engineer', '50000', '95000', 'Design and write code', 'San Francisco', 'Yes', '1');
insert into job values ('2', '2019-09-18', 'Open', 'Java Programmer', '40000', '90000', 'Write Java Code', 'San Francisco', 'Yes', '1');

insert into application values ('1', '2019-09-22', 'Interview', '1', '1');
insert into application values ('2', '2019-09-23', 'Applied', '2', '1');
insert into application values ('3', '2019-09-24', 'Applied', '3', '1');
insert into application values ('4', '2019-09-22', 'Applied', '4', '2');
insert into application values ('5', '2019-09-23', 'Offer', '5', '2');

insert into interview values ('1', '2019-09-24', 'Pending', null, '1');
insert into interview values ('2', '2019-09-25', 'Recommend for offer', 'Exceeds all requirements', '5');

insert into offer values ('1', '2019-09-25', 'Accepted', '90000', '2019-10-07', '2', null);


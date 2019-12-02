drop database if exists ats;
 
create database ats;
 
use ats;
 

create table department
	(deptid				INT AUTO_INCREMENT,
	 name				varchar(1000),
	 primary key (deptid)
	);
	
create table applicant
	(app_id			INT AUTO_INCREMENT, 
	psw				varchar(256) not null,
	emailid			varchar(1000) not null,
	name			varchar(1000) not null,
	gender			varchar(64)
		check (gender in ('Female', 'Male', 'Unknown')),
	birth_dt		date,
	status			varchar(64)
		check (status in ('Active', 'Inactive')),      
	 primary key (app_id)
	);

create table resume
	(res_id			INT AUTO_INCREMENT, 
	 resume			varchar(1000), 
	 app_id		    INT not null,
	 primary key (res_id),
	 foreign key (app_id) references applicant(app_id)
	);
	
create table employee
	(emplid			INT AUTO_INCREMENT, 
	 name			varchar(1000) not null, 
	 hire_dt		date,
	 status			varchar(64) not null
	 	check (status in ('Active', 'Inactive')),
	 salary			numeric(8,2) check (salary > 29000),
	 email			varchar(1000),
	 deptid			INT, 	 
	 primary key (emplid),
	 foreign key (deptid) references department(deptid)
		on delete set null
	);

create table users
	(userid			INT AUTO_INCREMENT, 
	 psw			varchar(1000) not null, 
	 type			varchar(64)
	 	check (type in ('Hiring Manager', 'Recruiter', 'Administrator')),
	 emplid			INT,
	 deptid			INT,
	 primary key (userid),
	 foreign key (deptid) references department(deptid)
		on delete set null,
	 foreign key (emplid) references employee(emplid)
		on delete set null
	);

create table job
	(jobid			INT AUTO_INCREMENT, 
	 open_dt		date,
	 status			varchar(64)
	 	check (status in ('Open', 'Closed', 'Cancelled')), 
	 title			varchar(1000),
	 salary_min		numeric(8,2) check (salary_min > 29000),
	 salary_max		numeric(8,2) check (salary_max < 1000000),
	 descr			varchar(1000),
	 location		varchar(1000),
	 visibility		varchar(64)
	 	check (visibility in ('Y', 'N')),
	 deptid			INT,
	 primary key (jobid),
	 foreign key (deptid) references department(deptid)
		on delete set null
	);

create table application
	(appl_id		INT AUTO_INCREMENT, 
	 appl_dt		date,
	 status			varchar(64)
	 	check (status in ('Applied', 'Reviewed', 'Reject', 'Interview', 'Offer', 'Hired')),
	 app_id			INT,
	 jobid			INT,
	 primary key (appl_id),
	 foreign key (app_id) references applicant(app_id)
		on delete set null,
	 foreign key (jobid) references job(jobid)
		on delete set null
	);

create table interview
	(int_id			INT AUTO_INCREMENT, 
	 int_dt			date,
	 status			varchar(64)
	 	check (status in ('Pending', 'Recommend for offer', 'Reject')),
	 comments		varchar(64),
	 appl_id		INT,
	 primary key (int_id),
	 foreign key (appl_id) references application(appl_id)
		on delete set null
	);
	
	create table offer
	(ofr_id			INT AUTO_INCREMENT,
	 ofr_dt			date,
	 status			varchar(64)
	 	check (status in ('Submitted', 'Accepted', 'Rejected')), 
	 salary			numeric(8,2) check (salary > 29000),
	 start_dt		date,
	 int_id			INT,
	 emplid			INT,
	 primary key (ofr_id),
	 foreign key (int_id) references interview(int_id)
		on delete set null,
	 foreign key (emplid) references employee(emplid)
		on delete set null
	);

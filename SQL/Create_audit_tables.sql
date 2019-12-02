use ats

create table aud_department
	(
	auditID integer Auto_increment	primary key,
	deptid				INT,
	name				varchar(20),
	action				varchar(10),
 	whochanged 			nvarchar(128),
	whenchanged 			datetime(3)
	);
	

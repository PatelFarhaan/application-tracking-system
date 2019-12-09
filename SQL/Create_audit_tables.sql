use ats;
drop table if exists aud_department;
create table aud_department
	(
	auditID integer Auto_increment	primary key,
	deptid				INT,
	name_old			varchar(20),
    	name_new			varchar(20),
	action				varchar(10),
 	whochanged 			nvarchar(128),
	whenchanged 			datetime(3)
	);
	

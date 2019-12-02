use ats;

DROP TRIGGER  department_audit


CREATE TRIGGER department_audit on department for INSERT, UPDATE, DELETE
AS insert into aud_department(deptid, name, action, WhoChanged, WhenChanged)
select 
				deptid,
				name,
				CASE WHEN EXISTS (SELECT * FROM Deleted)
					THEN 'UPDATED'
					ELSE 'INSERTED' END,
				SUSER_SNAME(),
				now()
			FROM
			   Inserted I
		UNION ALL
		select 
				deptid,
				name,
				'DELETED',
				SUSER_SNAME(),
				now()
			FROM Deleted D
			WHERE NOT EXISTS (SELECT * FROM Inserted);

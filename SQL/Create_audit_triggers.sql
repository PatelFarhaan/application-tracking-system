use ats;
DROP TRIGGER if exists department_uTrg;
DELIMITER $$;
CREATE TRIGGER department_uTrg 
AFTER UPDATE ON department 
FOR EACH ROW
BEGIN
	DECLARE `username` varchar(60);
	SELECT SUBSTRING_INDEX(USER(),'@',1) INTO `username`;
	INSERT INTO aud_department (deptid, name_old, name_new, action, whochanged, whenchanged) 
    VALUES (OLD.deptid, OLD.name, NEW.name, 'UPDATE', `username`, now());
END 
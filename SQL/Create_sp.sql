use ats;
DELIMITER $$;
CREATE  PROCEDURE Audit ()
BEGIN
	select * from aud_department;
END

-- CALL Audit()
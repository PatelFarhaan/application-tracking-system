use ats;
DELIMITER $$;
CREATE  PROCEDURE RejectOthers (IN in_app_id varchar(8),  IN in_jobid varchar(8))
BEGIN
	update application set status = 'Reject' where app_id != in_app_id and jobid = in_jobid ;
END

CALL RejectOthers(4,2)


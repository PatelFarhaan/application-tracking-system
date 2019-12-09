
use ats;


create or replace view  hm_appl_vw
as select a.name,
       a.emailid,
       a.gender,
       b.appl_dt,
	   b.status,
	   b.app_id, b.jobid
from applicant a, application b, job c, users d where 
a.app_id = b.app_id and 
b.jobid = c.jobid and 
c.deptid = d.deptid
;

create or replace view job_vw
as select a.title, a.open_dt, a.descr, a.location 
from job a
where a.visibility = 'Y'
;
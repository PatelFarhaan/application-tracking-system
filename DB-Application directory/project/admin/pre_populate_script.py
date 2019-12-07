import sys
sys.path.append('../../')


import datetime
from project import db, app
from project.models import Job, Employee, Users
from werkzeug.security import generate_password_hash



########################################################################################################################
new_emp_obj = Employee(name='Hiring Manager 1',
                       email='hiringmanager1@gmail.com',
                       salary=60000,
                       status='Active',
                       deptid=1,
                       hire_dt=datetime.date.today())
db.session.add(new_emp_obj)
db.session.commit()
app.logger.info('Hiring Manager 1 Created')


emp_obj = Employee.query.filter_by(email='hiringmanager1@gmail.com').first()
emp_user_obj = Users(emplid=emp_obj.emplid,
                     deptid=1,
                     type='Hiring Manager',
                     psw=generate_password_hash('hr1'))
db.session.add(emp_user_obj)
db.session.commit()

new_emp_obj = Employee(name='Recruiter',
                       email='recruiter1@gmail.com',
                       salary=50000,
                       status='Active',
                       deptid=2,
                       hire_dt=datetime.date.today())
db.session.add(new_emp_obj)
db.session.commit()
app.logger.info('Recruiter Created')


emp_obj = Employee.query.filter_by(email='recruiter1@gmail.com').first()
emp_user_obj = Users(emplid=emp_obj.emplid,
                     deptid=2,
                     type='Recruiter',
                     psw=generate_password_hash('r1'))
db.session.add(emp_user_obj)
db.session.commit()
########################################################################################################################
jobs_obj = Job(title='Job Title 1',
               salary_min=30000,
               salary_max=60000,
               open_dt=datetime.date.today(),
               location='New York',
               descr='Job Description 1',
               status='Open',
               visibility='Yes',
               deptid=2)
db.session.add(jobs_obj)
db.session.commit()
app.logger.info('Job 1 Created')


jobs_obj = Job(title='Job Title 2',
               salary_min=35000,
               salary_max=70000,
               open_dt=datetime.date.today(),
               location='California',
               descr='Job Description 2',
               status='Open',
               visibility='Yes',
               deptid=1)
db.session.add(jobs_obj)
db.session.commit()
app.logger.info('Job 2 Created')


jobs_obj = Job(title='Job Title 3',
               salary_min=50000,
               salary_max=90000,
               open_dt=datetime.date.today(),
               location='Boston',
               descr='Job Description 3',
               status='Open',
               visibility='Yes',
               deptid=2)
db.session.add(jobs_obj)
db.session.commit()
app.logger.info('Job 3 Created')
########################################################################################################################

print("Hiring Manager Created Successfully!!!")
print("Recruiter Created Successfully!!!")
print("3 Jobs Created Successfully!!!")

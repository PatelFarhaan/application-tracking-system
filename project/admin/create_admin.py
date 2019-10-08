import sys
sys.path.append('../../')


import datetime
from project import db
from werkzeug.security import generate_password_hash
from project.models import Users, Department, Employee

########################################################################################################################
dept_obj = Department(name='Engineering')
db.session.add(dept_obj)
db.session.commit()

########################################################################################################################
emp_obj = Employee(salary=100000,
                   hire_date=datetime.datetime.strptime('2019-03-13', '%Y-%m-%d'),
                   name='Farhaan Patel',
                   email='patel.farhaaan@gmail.com',
                   status='Active',
                   dept_id=1)
db.session.add(emp_obj)
db.session.commit()

emp_obj2 = Employee(salary=150000,
                    hire_date=datetime.datetime.strptime('2019-03-13', '%Y-%m-%d'),
                    name='Marianne Paulson',
                    email='marianne.paulson@sjsu.edu',
                    status='Active',
                    dept_id=1)
db.session.add(emp_obj2)
db.session.commit()

########################################################################################################################
admin_obj = Users(type='admin',
                  hashed_password=generate_password_hash('***REMOVED***'),
                  emp_id=1,
                  dept_id=1)
db.session.add(admin_obj)
db.session.commit()


admin_obj2 = Users(type='admin',
                   hashed_password=generate_password_hash('marianne'),
                   emp_id=2,
                   dept_id=1)
db.session.add(admin_obj2)
db.session.commit()
########################################################################################################################

print("Admin Created Successfully!!!")

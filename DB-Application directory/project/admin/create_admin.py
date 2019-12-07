import sys
sys.path.append('../../')

import datetime
from project import db, app
from werkzeug.security import generate_password_hash
from project.models import Users, Department, Employee


########################################################################################################################
import logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                        filename='/media/farhaan/New Volume/Masters/CMPE226_TEAM1_SOURCES/LOG/app.log',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG,
                        filemode='a')
########################################################################################################################

########################################################################################################################
dept_obj = Department(name='Engineering')
dept_obj1 = Department(name='Finance')
db.session.add(dept_obj)
db.session.add(dept_obj1)
db.session.commit()
logging.info('Engineering Department Created')
logging.info('Finance Department Created')

########################################################################################################################
emp_obj = Employee(salary=100000,
                   hire_dt=datetime.datetime.strptime('2019-03-13', '%Y-%m-%d'),
                   name='Farhaan Patel',
                   email='patel.farhaaan@gmail.com',
                   status='Active',
                   deptid=1)
db.session.add(emp_obj)
db.session.commit()
logging.info('First Admin User Created')


emp_obj2 = Employee(salary=150000,
                    hire_dt=datetime.datetime.strptime('2019-03-13', '%Y-%m-%d'),
                    name='Marianne Paulson',
                    email='marianne.paulson@sjsu.edu',
                    status='Active',
                    deptid=1)
db.session.add(emp_obj2)
db.session.commit()
logging.info('Second Admin User Created')


########################################################################################################################
admin_obj = Users(type='Administrator',
                  psw=generate_password_hash('***REMOVED***'),
                  emplid=1,
                  deptid=1)
db.session.add(admin_obj)
db.session.commit()


admin_obj2 = Users(type='Administrator',
                   psw=generate_password_hash('marianne'),
                   emplid=2,
                   deptid=1)
db.session.add(admin_obj2)
db.session.commit()
########################################################################################################################

print("Admin Created Successfully!!!")

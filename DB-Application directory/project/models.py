from flask_login import UserMixin
from project import db, login_manager


########################################################################################################################
###############################################* LOGIN MANAGER *########################################################
########################################################################################################################
@login_manager.user_loader
def user_load(user_id):
    return Applicant.query.get(user_id)
########################################################################################################################


########################################################################################################################
###############################################* LOGIN MANAGER *########################################################
########################################################################################################################
@login_manager.user_loader
def user_load(user_id):
    return Employee.query.get(user_id)
########################################################################################################################


########################################################################################################################
#################################################* DEPARTMENT *#########################################################
########################################################################################################################
class Department(db.Model):
    __tablename__ = 'department'

    deptid = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64))
########################################################################################################################


########################################################################################################################
#################################################* APPLICANT *##########################################################
########################################################################################################################
class Applicant(db.Model, UserMixin):
    __tablename__ = 'applicant'

    app_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    status = db.Column(db.String(64), default="Active")
    birth_dt = db.Column(db.DateTime)
    psw = db.Column(db.String(256))
    emailid = db.Column(db.String(64), unique=True, index=True)

    def get_id(self):
        return self.app_id
########################################################################################################################


########################################################################################################################
#################################################* RESUME *#############################################################
########################################################################################################################
class Resume(db.Model):
    __tablename__ = 'resume'

    res_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    resume = db.Column(db.String(256))
    app_id = db.Column(db.Integer, db.ForeignKey('applicant.app_id'), nullable=False)
########################################################################################################################


########################################################################################################################
#################################################* EMPLOYEE *###########################################################
########################################################################################################################
class Employee(db.Model, UserMixin):
    __tablename__ = 'employee'

    emplid = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    salary = db.Column(db.Float)
    hire_dt = db.Column(db.DateTime)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(64), nullable=False)
    deptid = db.Column(db.Integer, db.ForeignKey('department.deptid'), nullable=False)

    def get_id(self):
        return self.emplid
########################################################################################################################


########################################################################################################################
#################################################* USERS *##############################################################
########################################################################################################################
class Users(db.Model):
    __tablename__ = 'users'

    userid = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type = db.Column(db.String(64), nullable=False)
    psw = db.Column(db.String(256), nullable=False)
    emplid = db.Column(db.Integer, db.ForeignKey('employee.emplid'), nullable=False)
    deptid = db.Column(db.Integer, db.ForeignKey('department.deptid'), nullable=False)
########################################################################################################################


########################################################################################################################
###################################################* JOB *##############################################################
########################################################################################################################
class Job(db.Model):
    __tablename__ = 'job'

    jobid = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(64))
    salary_min = db.Column(db.Float)
    salary_max = db.Column(db.Float)
    open_dt = db.Column(db.DateTime)
    location = db.Column(db.String(64))
    descr = db.Column(db.Text)
    status = db.Column(db.String(64), nullable=False)
    visibility = db.Column(db.String, nullable=False)
    deptid = db.Column(db.Integer, db.ForeignKey('department.deptid'), nullable=False)
########################################################################################################################


########################################################################################################################
#################################################* APPLICATION *########################################################
########################################################################################################################
class Application(db.Model):
    __tablename__ = 'application'

    appl_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    appl_dt = db.Column(db.DateTime)
    status = db.Column(db.String(64), nullable=False, default='Applied')
    jobid = db.Column(db.Integer, db.ForeignKey('job.jobid'), nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('applicant.app_id'), nullable=False)
########################################################################################################################


########################################################################################################################
#################################################* INTERVIEW *##########################################################
########################################################################################################################
class Interview(db.Model):
    __tablename__ = 'interview'

    int_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    int_dt = db.Column(db.DateTime)
    comments = db.Column(db.Text)
    status = db.Column(db.String(64), nullable=False)
    appl_id = db.Column(db.Integer, db.ForeignKey('application.appl_id'), nullable=False)
########################################################################################################################


########################################################################################################################
####################################################* OFFER *###########################################################
########################################################################################################################
class Offer(db.Model):
    __tablename__ = 'offer'

    ofr_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    salary = db.Column(db.Float)
    ofr_dt = db.Column(db.DateTime)
    start_dt = db.Column(db.DateTime)
    status = db.Column(db.String(64), nullable=False)
    emplid = db.Column(db.Integer, db.ForeignKey('employee.emplid'), nullable=False)
    int_id = db.Column(db.Integer, db.ForeignKey('interview.int_id'), nullable=False)
########################################################################################################################
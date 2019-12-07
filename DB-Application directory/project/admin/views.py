import datetime
from project import db, app
from project.models import Users, Employee, Department
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template, request, Blueprint, redirect, url_for, session


########################################################################################################################
import logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                        filename=app.config['LOG_PATH'],
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG,
                        filemode='a')
########################################################################################################################


admin_blueprint = Blueprint('admin', __name__, template_folder='templates')



@admin_blueprint.route('/admin-view', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        admin_email = request.form.get('admin_email', None)
        admin_password = request.form.get('admin_password', None)

        if admin_email == None:
            return render_template('admin.html', warning='Email cannot be empty')

        if admin_password == None:
            return render_template('admin.html', warning='Password cannot be empty')

        admin_obj = Employee.query.filter_by(email=admin_email).first()

        if admin_obj == None:
            logging.debug('{admin} does not exist'.format(admin=admin_email))
            return render_template('admin.html', warning='Email address does not exist!!!')

        admin_users_obj = Users.query.filter_by(emplid=admin_obj.emplid).first()
        if admin_obj is not None and check_password_hash(admin_users_obj.psw, admin_password):
            login_user(admin_obj)
            logging.debug('{admin} Logged In'.format(admin=admin_email))
            return redirect(url_for('admin.create_rc_hr_accounts'))
    return render_template ('admin.html')


@admin_blueprint.route('/create-rc-hr-accounts', methods=['GET', 'POST'])
@login_required
def create_rc_hr_accounts():
    dept_names = Department.query.all()
    department_list = [x.name for x in dept_names]

    if request.method == 'POST':
        email = request.form.get('email', None)
        name = request.form.get('username', None)
        password = request.form.get('password', None)
        type = request.form.get('gridRadios', None)
        department = request.form.get('department', None)
        repeat_password = request.form.get('repeat_password', None)

        dept_obj = Department.query.filter_by(name=department).first()

        if name == None:
            return render_template('hr_recruiter_account_create.html', warning='Username cannot be None')

        if email == None:
            return render_template('hr_recruiter_account_create.html', warning='Email cannot be None')

        if type == None:
            return render_template('hr_recruiter_account_create.html', warning='Type cannot be None')

        if password == None:
            return render_template('hr_recruiter_account_create.html', warning='Password cannot be None')

        if repeat_password == None:
            return render_template('hr_recruiter_account_create.html', warning='Repeat Password cannot be None')

        if password != repeat_password:
            return render_template('hr_recruiter_account_create.html', warning='Both passwords should be same')

        new_emp_obj = Employee(name=name,
                               email=email,
                               salary=10000,
                               status='Active',
                               deptid=dept_obj.deptid,
                               hire_dt=datetime.date.today())
        db.session.add(new_emp_obj)
        db.session.commit()
        logging.debug('New employee {name} created'.format(name=name))

        emp_obj = Employee.query.filter_by(email=email).first()
        emp_user_obj = Users(emplid=emp_obj.emplid,
                             deptid=dept_obj.deptid,
                             type=type,
                             psw=generate_password_hash(password))
        db.session.add(emp_user_obj)
        db.session.commit()
        return redirect(url_for('admin.create_rc_hr_accounts'))
    return render_template('hr_recruiter_account_create.html',department_list=department_list)


@admin_blueprint.route('/admin-logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('users.login'))

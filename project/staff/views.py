import datetime
from project import db
from project.models import Users, Employee
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template, request, Blueprint, redirect, url_for, session


staff_blueprint = Blueprint('staff', __name__, template_folder='templates')


@staff_blueprint.route('/staff-login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        staff_email = request.form.get('staff_email', None)
        staff_password = request.form.get('staff_password', None)

        if staff_email == None:
            return render_template('staff_login.html', warning='Email cannot be empty')

        if staff_password == None:
            return render_template('staff_login.html', warning='Password cannot be empty')

        staff_obj = Employee.query.filter_by(email=staff_email).first()
        if staff_obj == None:
            return render_template('staff_login.html', warning='Email address does not exist!!!. Please contact Admin.')

        staff_users_obj = Users.query.filter_by(emp_id=staff_obj.id).first()
        if staff_obj is not None and check_password_hash(staff_users_obj.hashed_password, staff_password):
            login_user(staff_obj)
            return redirect(url_for('staff.staff_jobs_view_create'))
    return render_template('staff_login.html')


@staff_blueprint.route('/staff-jobs-view-create', methods=['GET', 'POST'])
@login_required
def staff_jobs_view_create():
    if request.method == 'POST':
        pass
    return render_template('staff_jobs_view_create.html')


@staff_blueprint.route('/admin-logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('users.login'))

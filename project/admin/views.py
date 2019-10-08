from project.models import Users, Employee
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user, logout_user
from flask import render_template, request, Blueprint, redirect, url_for, session


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
            return render_template('admin.html', warning='Email address does not exist!!!')

        admin_users_obj = Users.query.filter_by(emp_id=admin_obj.id).first()
        if admin_obj is not None and check_password_hash(admin_users_obj.hashed_password, admin_password):
            login_user(admin_obj)
            return redirect(url_for('admin.create_rc_hr_accounts'))
    return render_template ('admin.html')


@admin_blueprint.route('/create-rc-hr-accounts', methods=['GET', 'POST'])
def create_rc_hr_accounts():
    if request.method == 'POST':
        pass
    return render_template('hr_recruiter_account_create.html')
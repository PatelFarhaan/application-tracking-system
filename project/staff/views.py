import datetime
from project import db
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user, logout_user
from flask import render_template, request, Blueprint, redirect, url_for, session
from project.models import Users, Employee, Job, Department, Application,Applicant, Resume


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
    dept_names = Department.query.all()
    department_list = [x.name for x in dept_names]

    final_display_list = []
    all_application_obj = Application.query.all()

    if all_application_obj != []:
        for application in all_application_obj:
            application = application.__dict__
            job_id = application['job_id']
            applicant_id = application['app_id']
            job_obj = Job.query.filter_by(id=job_id).first()
            user_obj = Applicant.query.filter_by(id=applicant_id).first()
            resume_obj = Resume.query.filter_by(app_id=applicant_id).first()
            temp_dict = {}
            temp_dict['job_id'] = job_id
            temp_dict['job_title'] = job_obj.title
            temp_dict['user_name'] = user_obj.name
            temp_dict['applicant_id'] = applicant_id
            temp_dict['user_resume'] = resume_obj.resume
            temp_dict['applied_date'] = application['appl_date']
            final_display_list.append(temp_dict)

    if request.method == 'POST':
        form = request.form.get('action', None)
        print("action is", form)
        if form == 'create_job':
            status = request.form.get('status', None)
            desc = request.form.get('job_desc', None)
            title = request.form.get('job_title', None)
            location = request.form.get('location', None)
            min_sal = request.form.get('min_salary', None)
            max_sal = request.form.get('max_salary', None)
            visibility = request.form.get('gridRadios', None)
            department = request.form.get('department', None)

            if visibility == 'visible':
                visibility = True
            else:
                visibility = False

            dept_obj = Department.query.filter_by(name=department).first()

            if title == None or title == '':
                return render_template('staff_jobs_view_create.html', warning='Job Title cannot be empty')
            if desc == None or desc == '':
                return render_template('staff_jobs_view_create.html', warning='Job Description cannot be empty')
            if visibility == None or visibility == '':
                return render_template('staff_jobs_view_create.html', warning='Job Visibility cannot be empty')
            if location == None or location == '':
                return render_template('staff_jobs_view_create.html', warning='Job Location cannot be empty')

            new_job_obj = Job(title=title,
                              status=status,
                              description=desc,
                              location=location,
                              min_salary=min_sal,
                              max_salary=max_sal,
                              dept_id=dept_obj.id,
                              visibility=visibility,
                              open_date=datetime.datetime.utcnow())
            db.session.add(new_job_obj)
            db.session.commit()
            return redirect(url_for('staff.staff_jobs_view_create'))
        else:
            result = request.form.get('action')
            print(type(result))
            application_obj = Application.query.filter_by().all()

    return render_template('staff_jobs_view_create.html',
                           department_list=department_list,
                           final_display_list=final_display_list)


@staff_blueprint.route('/admin-logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('users.login'))

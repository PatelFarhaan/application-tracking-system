import json
import datetime
import threading
from project import db, app
from werkzeug.security import check_password_hash
from project.staff.emails import email_sending_logic
from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template, request, Blueprint, redirect, url_for, session
from project.models import Users, Employee, Job, Department, Application, Applicant, Resume


########################################################################################################################
import logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                        filename=app.config['LOG_PATH'],
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG,
                        filemode='a')
########################################################################################################################

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

        staff_users_obj = Users.query.filter_by(emplid=staff_obj.emplid).first()
        if staff_obj is not None and check_password_hash(staff_users_obj.psw, staff_password):
            logging.debug('{name} User Logged In'.format(name=staff_obj.name))
            login_user(staff_obj)
            return redirect(url_for('staff.staff_jobs_view_create'))
    return render_template('staff_login.html')


@staff_blueprint.route('/staff-jobs-view-create', methods=['GET', 'POST'])
@login_required
def staff_jobs_view_create():

    current_emp_obj = Employee.query.filter_by(email=current_user.__dict__['email']).first()
    current_user_obj = Users.query.filter_by(emplid=current_emp_obj.emplid).first()
    isRecruiter = current_user_obj.type

    dept_names = Department.query.all()
    department_list = [x.name for x in dept_names]

    if isRecruiter == 'Recruiter':
        final_display_list = []
        all_application_obj = Application.query.all()

        if all_application_obj != []:
            for application in all_application_obj:
                print(application.__dict__)
                application = application.__dict__
                job_id = application['jobid']
                applicant_id = application['app_id']
                job_obj = Job.query.filter_by(jobid=job_id).first()
                user_obj = Applicant.query.filter_by(app_id=applicant_id).first()
                resume_obj = Resume.query.filter_by(app_id=applicant_id).first()
                temp_dict = {}
                temp_dict["job_id"] = job_id
                temp_dict["job_title"] = job_obj.title
                temp_dict["user_name"] = user_obj.name
                temp_dict["applicant_id"] = applicant_id
                temp_dict["user_resume"] = resume_obj.resume
                temp_dict["status"] = application["status"]
                temp_dict["applied_date"] = datetime.datetime.strftime(application["appl_dt"], '%d %b %Y')
                final_display_list.append(temp_dict)


    elif isRecruiter == 'Hiring Manager':
        final_display_list = []

        all_application_obj = Application.query.all()
        list_of_jobs = Job.query.filter_by(deptid=1).all()

        if all_application_obj != []:
            for application in all_application_obj:
                application = application.__dict__
                job_id = application['jobid']
                applicant_id = application['app_id']

                for jobs in list_of_jobs:
                    if jobs.jobid == job_id:
                        user_obj = Applicant.query.filter_by(app_id=applicant_id).first()
                        resume_obj = Resume.query.filter_by(app_id=applicant_id).first()
                        temp_dict = {}
                        temp_dict["job_id"] = job_id
                        temp_dict["job_title"] = jobs.title
                        temp_dict["user_name"] = user_obj.name
                        temp_dict["applicant_id"] = applicant_id
                        temp_dict["user_resume"] = resume_obj.resume
                        temp_dict["status"] = application["status"]
                        temp_dict["applied_date"] = datetime.datetime.strftime(application["appl_dt"], '%d %b %Y')
                        final_display_list.append(temp_dict)


    if request.method == 'POST':
        form = request.form.get('action', None)
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
                              descr=desc,
                              location=location,
                              salary_min=min_sal,
                              salary_max=max_sal,
                              deptid=dept_obj.deptid,
                              visibility=visibility,
                              open_dt=datetime.date.today())
            db.session.add(new_job_obj)
            db.session.commit()
            logging.debug('New Job {title} Created'.format(title=title))
            return redirect(url_for('staff.staff_jobs_view_create'))
        else:
            if request.method == 'POST':
                res = request.form.to_dict()
                res = res["action"].replace("'", '"')
                ap = res[1:-8]
                action = res[-6:-1]
                res = json.loads(ap)

                if action == '"rev"':
                    app_name = Applicant.query.filter_by(app_id=res['applicant_id']).first().name
                    job_name = Job.query.filter_by(jobid=res['job_id']).first().title
                    logging.debug('{aname} Reviewed for Job {jname}'.format(aname=app_name, jname=job_name))
                    department_list, final_display_list = commonSaveLogic("Reviewed", res)

                if action == '"rej"':
                    app_name = Applicant.query.filter_by(app_id=res['applicant_id']).first().name
                    job_name = Job.query.filter_by(jobid=res['job_id']).first().title
                    logging.debug('{aname} Rejected for Job {jname}'.format(aname=app_name, jname=job_name))
                    department_list, final_display_list = commonSaveLogic("Rejected", res)

                if action == '"int"':
                    app_name = Applicant.query.filter_by(app_id=res['applicant_id']).first().name
                    job_name = Job.query.filter_by(jobid=res['job_id']).first().title
                    logging.debug('{aname} Interviewed for Job {jname}'.format(aname=app_name, jname=job_name))
                    department_list, final_display_list = commonSaveLogic("Interviewed", res)

                if action == '"off"':
                    app_name = Applicant.query.filter_by(app_id=res['applicant_id']).first().name
                    job_name = Job.query.filter_by(jobid=res['job_id']).first().title
                    logging.debug('{aname} Offered for Job {jname}'.format(aname=app_name, jname=job_name))
                    department_list, final_display_list = commonSaveLogic("Offer", res)

                if action == '"hir"':
                    app_name = Applicant.query.filter_by(app_id=res['applicant_id']).first().name
                    job_name = Job.query.filter_by(jobid=res['job_id']).first().title
                    logging.debug('{aname} Hired for Job {jname}'.format(aname=app_name, jname=job_name))
                    rejectOtherCandidates(res['job_id'], res['applicant_id'])
                    department_list, final_display_list = commonSaveLogic("Hired", res)
                    email_thread = threading.Thread(target=email_send, args=(res['job_id'], res['applicant_id']))
                    email_thread.start()

    return render_template('staff_jobs_view_create.html',
                           department_list=department_list,
                           final_display_list=final_display_list)


@staff_blueprint.route('/admin-logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('staff.login'))

########################################################################################################################
########################################################################################################################
########################################################################################################################
def commonSaveLogic(new, res):
    status_change_obj = Application.query.filter_by(jobid=res['job_id'], app_id=res['applicant_id']).first()
    status_change_obj.status = new
    db.session.commit()
    dept_names = Department.query.all()
    department_list = [x.name for x in dept_names]

    final_display_list = []
    all_application_obj = Application.query.all()

    if all_application_obj != []:
        for application in all_application_obj:
            application = application.__dict__
            job_id = application['jobid']
            applicant_id = application['app_id']
            job_obj = Job.query.filter_by(jobid=job_id).first()
            user_obj = Applicant.query.filter_by(app_id=applicant_id).first()
            resume_obj = Resume.query.filter_by(app_id=applicant_id).first()
            temp_dict = {}
            temp_dict["job_id"] = job_id
            temp_dict["job_title"] = job_obj.title
            temp_dict["user_name"] = user_obj.name
            temp_dict["applicant_id"] = applicant_id
            temp_dict["user_resume"] = resume_obj.resume
            temp_dict["status"] = application["status"]
            temp_dict["applied_date"] = datetime.datetime.strftime(application["appl_dt"], '%d %b %Y')
            final_display_list.append(temp_dict)
    return department_list, final_display_list


def rejectOtherCandidates(job_id, applicant_id):
    try:
        filter_list = Application.query.filter_by(jobid=job_id).all()
        filter_list = list(i.__dict__ for i in filter_list if i.__dict__['app_id'] != applicant_id)
        for j in filter_list:
            app_id = j['app_id']
            job_id = j['job_id']
            app_status_obj = Application.query.filter_by(app_id=app_id, jobid=job_id).first()
            app_status_obj.status = 'Rejected'
            db.session.commit()
    except:
        db.session.rollback()


def email_send(job_id, applicant_id):
    applicant_obj = Applicant.query.filter_by(app_id=applicant_id).first()
    job_obj = Job.query.filter_by(jobid=job_id).first()
    resp = email_sending_logic(applicant_obj.name,job_obj.title, applicant_obj.emailid)
    print(resp)

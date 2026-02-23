import sys
sys.path.append('../../')

import boto3
import datetime
from project import db, app
from project.models import Applicant, Resume, Job, Application
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, redirect, request, Blueprint, session


users_blueprint = Blueprint('users', __name__, template_folder='templates')


########################################################################################################################
import logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                        filename=app.config['LOG_PATH'],
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG,
                        filemode='a')
########################################################################################################################

@users_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('users.login'))


@users_blueprint.route('/register', methods=['GET','POST'])
def register():
    session.clear()
    if request.method == 'POST':
        email = request.form.get('email', None)
        name = request.form.get('name', None)
        password = request.form.get('password', None)
        gender = request.form.get('gridRadios', None)
        repeat_password = request.form.get('repeat_password', None)
        dob = request.form.get('date_of_birth', None)
        resume = request.files.get('resume', None)
        resume_name = resume.filename.replace(' ', '')

        if email is None or email == '':
            return render_template('register.html', warning='Email cannot be Empty')

        if password is None or password == '':
            return render_template('register.html', warning='Password cannot be Empty')

        if repeat_password is None or repeat_password == '':
            return render_template('register.html', warning='Confirm Password cannot be Empty')

        if name is None or name == '':
            return render_template('register.html', warning='Name cannot be Empty')

        if gender is None:
            return render_template('register.html', warning='Gender cannot be Empty')

        if dob is None or dob == '':
            return render_template('register.html', warning='Date of Birth cannot be Empty')

        if resume is None or resume.filename == '':
            return render_template('register.html', warning='Resume cannot be Empty')

        if not (password == repeat_password):
            return render_template('register.html', warning='Both passwords should be same.')

        user = Applicant.query.filter_by(emailid=email).first()

        if user == None:
            try:
                new_user_obj = Applicant(name=name,
                                         emailid=email,
                                         gender=gender,
                                         birth_dt=datetime.datetime.strptime(dob, '%m/%d/%Y'),
                                         psw=generate_password_hash(password))
                db.session.add(new_user_obj)
                db.session.commit()
                logging.debug('New Applicant {name} Registered'.format(name=name))

                user = Applicant.query.filter_by(emailid=email).first()
                public_resume_link = file_upload_to_s3(resume, resume_name)
                new_resume_obj = Resume(app_id=user.app_id,
                                        resume=public_resume_link)

                db.session.add(new_resume_obj)
                db.session.commit()
                return redirect(url_for('users.login'))
            except:
                db.session.rollback()
            db.session.remove()
        else:
            return render_template('register.html', warning='Email already exists. Please Login')
    return render_template('register.html')


@users_blueprint.route('/login', methods=['GET','POST'])
def login():
    session.clear()
    if request.method == 'POST':
        email = request.form.get('email', 'None')
        password = request.form.get('password', 'None')
        user = Applicant.query.filter_by(emailid=email).first()

        if user == None:
            logging.debug('Applicant {email} Does Not Exist'.format(email=email))
            return render_template('login.html', warning='Email Does not exist!!!')
        elif check_password_hash(user.psw, password) and user is not None:
            logging.debug('Applicant {name} Logged In'.format(name=user.name))
            login_user(user)
            session['user_email'] = user.emailid
            return redirect(url_for('users.applicant_view'))
        else:
            return render_template('login.html', warning='Password is incorrect')
    return render_template('login.html')


@users_blueprint.route('/applicant-view', methods=['GET', 'POST'])
@login_required
def applicant_view():
    user_email = session['user_email']
    page = request.args.get('page', 1, type=int)
    total_jobs = Job.query.paginate(page=page, per_page=5)
    total_job_count = (total_jobs.__dict__)['total']

    user_obj = Applicant.query.filter_by(emailid=user_email).first()
    applicant_obj = Application.query.filter_by(app_id=user_obj.app_id).all()

    job_id_list = [x.jobid for x in applicant_obj]
    applied_list = [x.status for x in applicant_obj]
    job_id_list = dict(zip(job_id_list, applied_list))

    if request.method == 'POST':
        apply_job_id = request.form.get('apply_job', None)
        new_application_obj = Application(appl_dt=datetime.date.today(),
                                          app_id=user_obj.app_id,
                                          jobid=apply_job_id)


        db.session.add(new_application_obj)
        db.session.commit()
        return redirect(url_for('users.applicant_view'))


    return render_template('applicant-view.html',
                           is_applicant=True,
                           total_jobs=total_jobs,
                           user_name=user_obj.name,
                           job_id_list=job_id_list,
                           total_job_count=total_job_count)


@users_blueprint.route('/applicant-attachments', methods=['GET','POST'])
def applicant_attachments():
    user_email = session['user_email']
    user_obj = Applicant.query.filter_by(emailid=user_email).first()
    username = user_obj.name
    if request.method == 'POST':
        lor = request.files.get('lor', None)
        lor_name = lor.filename.replace(' ', '')
        transcripts = request.files.get('transcripts', None)
        transcripts_name = transcripts.filename.replace(' ', '')
        cover_letter = request.files.get('cover_letter', None)
        cover_letter_name = cover_letter.filename.replace(' ', '')

        if not lor is None and lor.filename != '':
            public_lor_link = file_upload_to_dynamo_s3(lor, lor_name)
            user_dynamo_obj = {
                'pk': user_obj.app_id
            }
            read_response = read_from_dynamo(user_dynamo_obj)
            if 'Item' in read_response:
                lor_obj = {
                                'type': 'LOR',
                                'link': public_lor_link
                            }
                dt_obj = f'{datetime.datetime.utcnow()}'
                read_response['Item']['attachments'][dt_obj] = lor_obj
                write_resp = write_to_dynamo(read_response['Item'])
            else:
                dt_obj = f'{datetime.datetime.utcnow()}'
                dynamo_obj = {
                    'pk': user_obj.app_id,
                    'attachments':
                        {
                            dt_obj: {
                                'type': 'LOR',
                                'link': public_lor_link
                            }
                        }
                    }
                write_to_dynamo(dynamo_obj)

        if not transcripts is None and transcripts.filename != '':
            public_transcript_link = file_upload_to_dynamo_s3(transcripts, transcripts_name)
            user_dynamo_obj = {
                'pk': user_obj.app_id
            }
            read_response = read_from_dynamo(user_dynamo_obj)
            if 'Item' in read_response:
                trns_obj = {
                    'type': 'TRANSCRIPTS',
                    'link': public_transcript_link
                }
                dt_obj = f'{datetime.datetime.utcnow()}'
                read_response['Item']['attachments'][dt_obj] = trns_obj
                write_resp = write_to_dynamo(read_response['Item'])
            else:
                dt_obj = f'{datetime.datetime.utcnow()}'
                dynamo_obj = {
                    'pk': user_obj.app_id,
                    'attachments':
                        {
                            dt_obj: {
                                'type': 'TRANSCRIPTS',
                                'link': public_transcript_link
                            }
                        }
                }
                write_to_dynamo(dynamo_obj)

        if not cover_letter is None and cover_letter.filename != '':
            public_cv_link = file_upload_to_dynamo_s3(cover_letter, cover_letter_name)
            user_dynamo_obj = {
                'pk': user_obj.app_id
            }
            read_response = read_from_dynamo(user_dynamo_obj)
            if 'Item' in read_response:
                cv_obj = {
                    'type': 'COVER-LETTER',
                    'link': public_cv_link
                }
                dt_obj = f'{datetime.datetime.utcnow()}'
                read_response['Item']['attachments'][dt_obj] = cv_obj
                write_resp = write_to_dynamo(read_response['Item'])
            else:
                dt_obj = f'{datetime.datetime.utcnow()}'
                dynamo_obj = {
                    'pk': user_obj.app_id,
                    'attachments':
                        {
                            dt_obj: {
                                'type': 'COVER-LETTER',
                                'link': public_cv_link
                            }
                        }
                }
                write_to_dynamo(dynamo_obj)

        return redirect(url_for('users.applicant_view'))
    return render_template('applicant_attachments.html', user_name=username)

########################################################################################################################
########################################################################################################################
########################################################################################################################
def file_upload_to_s3(file, object_name):
    bucket = 'cmpe226-ats2'
    s3 = boto3.client(
        's3',
        aws_access_key_id='***REMOVED***',
        aws_secret_access_key='***REMOVED***'
    )
    s3.upload_fileobj(file, bucket, object_name, ExtraArgs={"ACL": "public-read"})
    public_url = f"https://cmpe226-ats2.s3-us-west-1.amazonaws.com/{object_name}"
    return public_url


def file_upload_to_dynamo_s3(file, object_name):
    bucket = 'cmpe226-ats-dynamodb'
    s3 = boto3.client(
        's3',
        aws_access_key_id='***REMOVED***',
        aws_secret_access_key='***REMOVED***'
    )
    s3.upload_fileobj(file, bucket, object_name, ExtraArgs={"ACL": "public-read"})
    public_url = f"https://cmpe226-ats-dynamodb.s3-us-west-1.amazonaws.com/{object_name}"
    return public_url


def write_to_dynamo(item_obj: dict):
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-west-1',
        aws_access_key_id='***REMOVED***',
        aws_secret_access_key='***REMOVED***'
        )
    table = dynamodb.Table('cmpeats')
    response = table.put_item(
        Item=item_obj
    )
    print(response)


def read_from_dynamo(item_obj: dict):
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-west-1',
        aws_access_key_id='***REMOVED***',
        aws_secret_access_key='***REMOVED***'
    )
    table = dynamodb.Table('cmpeats')
    response = table.get_item(
        Key=item_obj
    )
    return response

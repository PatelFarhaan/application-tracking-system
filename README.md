# Application Tracking System

A full-stack web application for managing the end-to-end hiring pipeline. The system supports three user roles -- Applicants, HR Staff (Hiring Managers and Recruiters), and Administrators -- with features including job posting, application submission with resume upload to AWS S3, interview scheduling, offer management, and automated email notifications.

## Tech Stack

- **Language:** Python 3.x
- **Web Framework:** Flask
- **Database:** MySQL (SQLAlchemy ORM, Flask-Migrate)
- **NoSQL:** AWS DynamoDB (for applicant attachments)
- **Storage:** AWS S3 (resume and document storage)
- **Authentication:** Flask-Login with password hashing (Werkzeug)
- **Email:** SMTP (Gmail) for automated notifications
- **Frontend:** HTML, Bootstrap 4, Jinja2 templates

## Features

- **Applicant Portal:**
  - Account registration with resume upload to S3
  - Browse and apply for jobs with pagination
  - Upload additional attachments (LOR, transcripts, cover letters) stored in DynamoDB/S3

- **Staff Portal (Hiring Manager / Recruiter):**
  - Create job postings with department, salary range, location, and visibility
  - Review, reject, interview, offer, and hire candidates
  - Automatic rejection of other candidates when one is hired
  - Automated email notifications for interviews, offers, and hiring decisions

- **Admin Portal:**
  - Create HR and Recruiter accounts
  - Department management

- **Database:**
  - Full SQL schema with stored procedures, views, audit triggers, and sample data
  - DynamoDB integration for flexible document storage

## Prerequisites

- Python 3.7+
- pip
- MySQL server
- AWS account (S3, DynamoDB)
- Gmail account for SMTP notifications (with App Password)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<username>/Application-Tracking-System.git
   cd Application-Tracking-System
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   cd "DB-Application directory"
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cd ..
   cp .env.example .env
   # Edit .env with your database, AWS, and email credentials
   ```

5. **Set up MySQL database:**
   ```bash
   mysql -u root -p < SQL/Create_db_and_tables.sql
   mysql -u root -p ats < SQL/Create_sample_data.sql
   mysql -u root -p ats < SQL/Create_sp.sql
   mysql -u root -p ats < SQL/Create_views.sql
   mysql -u root -p ats < SQL/Create_audit_tables.sql
   mysql -u root -p ats < SQL/Create_audit_triggers.sql
   ```

6. **Create admin user:**
   ```bash
   cd "DB-Application directory"
   python project/admin/create_admin.py
   ```

7. **Optionally populate sample data:**
   ```bash
   python project/admin/pre_populate_script.py
   ```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `FLASK_SECRET_KEY` | Flask application secret key | `change-me-in-production` |
| `DATABASE_URI` | MySQL connection string | `mysql+pymysql://root:password@localhost/ats` |
| `LOG_PATH` | Path for application log file | `./LOG/app.log` |
| `AWS_ACCESS_KEY_ID` | AWS access key for S3/DynamoDB | _(required)_ |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key | _(required)_ |
| `AWS_REGION` | AWS region | `us-west-1` |
| `S3_RESUME_BUCKET` | S3 bucket for resume uploads | `cmpe226-ats2` |
| `S3_DYNAMO_BUCKET` | S3 bucket for DynamoDB attachments | `cmpe226-ats-dynamodb` |
| `DYNAMO_TABLE_NAME` | DynamoDB table name | `cmpeats` |
| `EMAIL_SENDER_ADDRESS` | Gmail address for sending notifications | _(required)_ |
| `EMAIL_SENDER_PASSWORD` | Gmail app password for SMTP | _(required)_ |

## How to Run

```bash
cd "DB-Application directory"
python app.py
```

The application starts on `http://localhost:5000`.

### Access Points

| URL | Role |
|---|---|
| `/` | Homepage |
| `/login` | Applicant login |
| `/register` | Applicant registration |
| `/staff-login` | Staff (Hiring Manager / Recruiter) login |
| `/admin-view` | Administrator login |

## Database Schema

The SQL schema includes the following tables:
- `department` - Company departments
- `applicant` - Job applicants
- `resume` - Applicant resumes (S3 links)
- `employee` - Company employees
- `users` - System users with role-based access
- `job` - Job postings
- `application` - Job applications
- `interview` - Interview records
- `offer` - Job offers

Additional SQL features: stored procedures, views, audit tables, and audit triggers.

## Project Structure

```
Application-Tracking-System/
├── DB-Application directory/
│   ├── app.py                          # Application entry point
│   ├── requirements.txt
│   └── project/
│       ├── __init__.py                 # Flask app factory and config
│       ├── models.py                   # SQLAlchemy ORM models
│       ├── core/
│       │   └── views.py               # Homepage routes
│       ├── users/
│       │   └── views.py               # Applicant routes and AWS integration
│       ├── staff/
│       │   ├── views.py               # Staff routes (jobs, applications)
│       │   └── emails.py              # Email notification logic
│       ├── admin/
│       │   ├── views.py               # Admin routes
│       │   ├── create_admin.py        # Admin user setup script
│       │   └── pre_populate_script.py # Sample data population
│       ├── error_pages/
│       │   └── handler.py             # Custom error pages
│       └── templates/                  # Jinja2 HTML templates
├── SQL/
│   ├── Create_db_and_tables.sql
│   ├── Create_sample_data.sql
│   ├── Create_sp.sql
│   ├── Create_views.sql
│   ├── Create_audit_tables.sql
│   ├── Create_audit_triggers.sql
│   └── RejectOthers_sp.sql
├── LOG/                                # Application logs
├── .env.example
├── .gitignore
├── Dockerfile
├── Makefile
└── README.md
```

## License

This project is licensed under the MIT License.

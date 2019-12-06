import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def email_sending_logic(name, job_name, email):
    try:
        mail_content_html = '''
                          <!DOCTYPE html>
                        <html lang="en" dir="ltr">

                        <head>
                          <meta charset="utf-8">
                          <title>Farhaan</title>
                          <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
                            integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
                          <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
                            integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
                            crossorigin="anonymous"></script>
                          <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"
                            integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49"
                            crossorigin="anonymous"></script>
                          <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"
                            integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy"
                            crossorigin="anonymous"></script>
                        </head>

                        <body>

                            <br>
                            <br>


                          <div class="container">
                            <div class="jumbotron">
                              <h1 align="center">APPLICATION TRACKING SYSTEM</h1>
                            </div>
                                <div class="jumbotron">
                                    <h2>Hello {name},</h2>
                                    <h3>You have been selected for the job "{job_name}."</h3>
                                    <br>
                                    <br>

                                    <h4>By Team,</h4>
                                    <h4>Application Tracking System</h4>
                                </div>
                                <br>
                                <br>
                                <br>
                          </div>
                        </body>

                        </html>
            '''.format(name=name, job_name=job_name)

        text = 'Please do not reply to this email. This is a system auto-generated email.'
        part1 = MIMEText(mail_content_html, 'html')
        part2 = MIMEText(text, 'plain')

        sender_address = '***REMOVED***'
        sender_pass = '***REMOVED***'
        receiver_address = email
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'UPDATE TO YOUR APPLICATION AT APPLICATION TRACKING SYSTEM'
        message.attach(part1)
        message.attach(part2)
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        return True
    except:
        return False
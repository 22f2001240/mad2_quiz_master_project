from flask import current_app as app
from .worker import celery
from .model import User,UserActivity,Scores
from celery.schedules import crontab
from jinja2 import Template
from datetime import datetime,timezone, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv
import os

def send_mail(email,subject,email_content,attachment=None):
    smtp_server_host = "localhost"
    smtp_port = 1025
    sender_email = "admin@gmail.com"
    sender_password = ""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(email_content, "html"))

    if attachment:
        with open(attachment,"rb") as attachment_content:
            part = MIMEBase('application','octet-stream')
            part.set_payload(attachment_content.read())
            encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % {os.path.basename(attachment)})
        part.add_header('Content-Disposition', f'attachment; filename= "{os.path.basename(attachment)}"')
            
        msg.attach(part)

    server = smtplib.SMTP(host=smtp_server_host, port=smtp_port)
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
    print("Mail Sent")

def get_html_report(username,data):
    with open("monthly_report.html", "r") as file:
        jinja_template = Template(file.read())
        html_report=jinja_template.render(username=username,data=data)
        return html_report


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*", hour="*"),  # Runs every minute
        daily_reminder.s(),
        name="Check for reminders every minute"
    )

    #execute on the first day of every month
    sender.add_periodic_task(
        crontab(day_of_month='1',month_of_year='*'),
        monthly_report.s(),
        name='montly_report at list of every month'
    )

@celery.task
def daily_reminder():
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)

    inactive_users = User.query.join(UserActivity).filter(UserActivity.last_visited < datetime.now().date()).all()

    with app.app_context():
        for user in inactive_users:
            if user.reminder_time and user.reminder_time.hour == ist_now.hour and user.reminder_time.minute == ist_now.minute:
                with open('daily_task.html','r') as f:
                    template = Template(f.read())
                    msg = template.render(username=user.name)
                    send_mail(email=user.email, email_content=msg, subject="Daily Reminder")
    print(f"✅ Sent reminders at {ist_now.strftime('%H:%M')} for users with matching preferred time")

@celery.task
def notify_new_quiz(quiz):
    users = User.query.filter_by(role = 'user').all()
    for user in users:
        msg = f"🚀 New Quiz Alert!\n\nA new quiz '{quiz}' has been added. Check it now!"
        send_mail(email=user.email,email_content=msg,subject="Reminder for Newly Created Quiz")

@celery.task
def monthly_report():
    students = User.query.filter_by(role = 'user').all()
    for student in students:
        scores = Scores.query.filter_by(user_id=student.id).all()
        score_details=[]
        for score in scores:
            temp_dict={}
            temp_dict["subject_name"] = score.quiz.chapter.subject.name
            temp_dict["chapter_name"] = score.quiz.chapter.name
            temp_dict["quiz_name"] = score.quiz.name
            temp_dict["total_score"] = score.total_score
            temp_dict["total_attempted_questions"] = score.total_attempted_questions,
            temp_dict["total_correct_answers"] = score.total_correct_answers
            temp_dict["total_wrong_answers"] = score.total_wrong_answers
            score_details.append(temp_dict)

        html_report=get_html_report(username=student.name,data=score_details)
        send_mail(email=student.email,email_content=html_report,subject="Monthly Report")
    print("✅ Monthly Report Sent!")


@celery.task
def data_export(quiz_details):
    with open('data_export.csv','w',newline='') as csvfile:
        fieldnames = ['quiz_id', 'chapter_name', 'level', 'date_of_quiz', 'time_of_quiz', 'time_duration', 'reamrks']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(quiz_details)
    send_mail(email="admin@gmail.com",email_content="Please find the exported data.",subject="Product Data Export",attachment="data_export.csv")
    return "Data Exported!!"

        

    

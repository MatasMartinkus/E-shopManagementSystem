from flask import Flask, request, jsonify
from itsdangerous import URLSafeTimedSerializer
from src.utils.dbengine import get_db
from src.models.user import User
import smtplib
from email.mime.text import MIMEText
import os

class EmailController:
    def __init__(self, app, smtp_server, smtp_port, smtp_user, smtp_password):
        self.app = app
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        self.serializer = URLSafeTimedSerializer(self.app.config['SECRET_KEY'])
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.setup_routes()

    def generate_verification_token(self, email):
        return self.serializer.dumps(email, salt=self.app.config['SECRET_KEY'])

    def confirm_verification_token(self, token, expiration=3600):
        try:
            email = self.serializer.loads(token, salt=self.app.config['SECRET_KEY'], max_age=expiration)
        except:
            return False
        return email

    def send_verification_email(self, email, token):
        verification_link = f"http://localhost:5000/verify/{token}"
        msg = MIMEText(f"Please click the link to verify your email: {verification_link}")
        msg['Subject'] = 'Email Verification'
        msg['From'] = self.smtp_user
        msg['To'] = email

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.set_debuglevel(1)  # Enable debug output
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(msg['From'], [msg['To']], msg.as_string())
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def setup_routes(self):
        @self.app.route('/verify/<token>', methods=['GET'])
        def verify_email(token):
            email = self.confirm_verification_token(token)
            if email:
                with get_db() as db:
                    user = db.query(User).filter(User.email == email).first()
                    if user:
                        user.is_verified = True
                        db.commit()
                        return jsonify({"message": "Email verified successfully!"}), 200
            return jsonify({"message": "Invalid or expired token!"}), 400
    
    def send_email(self, recipient, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.smtp_user
        msg['To'] = recipient

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.set_debuglevel(1)  # Enable debug output
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(msg['From'], [msg['To']], msg.as_string())
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")


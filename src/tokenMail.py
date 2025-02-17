import jwt
# # import smtplib
#from email.mime.text import MIMEText
#from flask import current_app
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
secret = "pepito"

load_dotenv()

def generate_reset_token(email):
    expiration_time = datetime.now() + timedelta(minutes=30)
    payload = {"email" : email, "exp": expiration_time}
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

email = "david@gmail.com"
print("Este es el token: ")
print(generate_reset_token(email))
print("---------------------------------------")




# def reset_email(email):
#     with current_app.app_context():
#         token = generate_reset_token(email)
#         reset_url = url_for("reset_password", token=token, _external=True)
#     subject = "Recuperacion de contraseña"
#     body = f"Haz click en el siguiente enlace para restablecer contraseña, tienes 30 minutos: {reset_url}"
#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = "pruebasjr341@gmail.com"
#     msg["To"] = email
    
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#         server.login("pruebasjr341@gmail.com", "")
#         server.sendmail(msg["From"], msg["To"], msg.as_string())
        
#     return "Correo enviado"

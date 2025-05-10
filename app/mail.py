import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()
sender_em = os.getenv("sender")
app_key = os.getenv("app_key")

def verify_code_mail(reciver,code):
    print(reciver,code)
    sender_email = sender_em
    app_password = app_key  # Wygenerowane hasło aplikacji
    receiver_email = str(reciver) # email do kogo chcemy wysłać

    html_content = """
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #007BFF;">Twój kod weryfikacyjny</h2>
        <p><b>Twój kod:</b> <span style="font-size: 20px; color: red;">{}</span></p>
        <p>Użyj go, aby potwierdzić swoją tożsamość.</p>
        <hr>
        <p style="font-size: 12px; color: gray;">Jeśli to nie Ty prosiłeś o kod, zignoruj tę wiadomość.</p>
      </body>
    </html>
    """.format(code)

    text_content = "To jest twój kod weryfikacyjny: {}. ".format(code)

    msg = MIMEMultipart("alternative")

    # Dodanie wersji tekstowej i HTML
    msg.attach(MIMEText(text_content, "plain"))  # Zwykły tekst
    msg.attach(MIMEText(html_content, "html"))  # HTML

    msg["Subject"] = "Kod Weryfikacyjny"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)  # Używamy hasła aplikacji
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    print("E-mail wysłany!")

def custom_mail(sender,sender_name,reciver, message, raport):
    print(reciver)
    sender_email = sender_em
    app_password = app_key  # Wygenerowane hasło aplikacji
    receiver_email = str(reciver)  # email do kogo chcemy wysłać

    html_content = f"""
<html>
  <body style="font-family: Arial, sans-serif; color: #333;">
    <h2 style="color: #007BFF;">Nowa wiadomość dotycząca zgłoszenia nr. {raport}</h2>
    <p><b>Od:</b> {sender_name} ({sender})</p>
    <p><b>Do:</b> {reciver}</p>
    <hr>
    <p>{message}</p>
    <br>
    <p style="font-size: 12px; color: gray;">Wiadomość wysłana ze strony <a href=" http://127.0.0.1:3000/login">Lost and Found Pets</a>. </p>
  </body>
</html>
"""

    text_content = f"Wiadomość od {sender_name} ({sender_email}):\n\n{message}"

    msg = MIMEMultipart("alternative")

    # Dodanie wersji tekstowej i HTML
    msg.attach(MIMEText(text_content, "plain"))  # Zwykły tekst
    msg.attach(MIMEText(html_content, "html"))  # HTML

    msg["Subject"] = "Nowa wiadomość dotycząca zgłoszenia"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)  # Używamy hasła aplikacji
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    print("E-mail wysłany!")
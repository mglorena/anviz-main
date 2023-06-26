import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class Correo(object):
    _smtp = "170.210.200.2"
    _smtpport = 25

    def __init__(self):
        pass

    def sendMail(self):
        # Configura la información del correo electrónico
        fecha = datetime.now().date().strftime("%d-%m-%Y")
        subject = f'{self.title} - {fecha}'
        # Crea el objeto del mensaje de correo electrónico
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.body, 'html'))

        try:
            # Enviar el correo utilizando smtplib
            with smtplib.SMTP(self._smtp, self._smtpport) as smtp:
                smtp.send_message(msg)
            print('Correo electrónico enviado.')
        except Exception as ex2:
            print('Correo NO enviado')

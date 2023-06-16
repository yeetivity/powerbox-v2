"""
Module responsible for creating an email and sending it out to a receiver
It attaches the report from /tmp in a pdf format
and analysed data and rawdata in a csv format

Author: Jitse van Esch
Date: 24-03-23
"""

import email, ssl, smtplib, os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from settings import Paths

class EmailGenerator():
    def __init__(self):
        pass
    
    def send_email(self, receiver_adress, username, date, resultID):
        
        # Initialise email details
        em = MIMEMultipart()
        sender_adress = os.environ.get("EM_SENDER_ADRESS")
        em['From'] = sender_adress
        em['To'] = receiver_adress
        em['Subject'] = """ Your PowerBox Result """
        em_password = os.environ.get("EM_PASSWORD")
        
        # Date for filename
        special_characters = ['/', '-', ':', ' ']
        file_date = date
        file_name = username.lower()
        for i in special_characters:
            file_date = file_date.replace(i, "")
            file_name = file_name.replace(i, "")
        
        # Create body
        body = f"""
        Hi {username},

        Thank you for using our PowerBox system, 
        Hereby we send you the report from your measurement,
        and your raw and analysed data.

        We hope to see you back again soon!

        Best regards,
        PowerBox
        """
        try:
            em.attach(MIMEText(body, "plain"))

            # Create pdf payload
            with open(Paths.PATH_REPORT, "rb") as attachment:
                # Add file as application/octet-stream, email client can usually download this automatically as attachment
                payload = MIMEBase("application", "octet-stream", Name=f"PowerBox-{file_name}-{file_date}.pdf")
                payload.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(payload)

            # Add header as key/value pair to attachment part
            payload.add_header("Content-Decomposition", "attachment", filename=Paths.PATH_REPORT)
            em.attach(payload)

            # Create csv payloads
            rawdata_path = Paths.PATH_RAWDATA + str(resultID) + ".csv"
            with open(rawdata_path, "rb") as attachment2:
                em.attach(MIMEApplication(attachment2.read(), Name=f"Rawdata-{file_name}-{file_date}.csv"))
            
            analyseddata_path = Paths.PATH_ANALYSEDDATA + str(resultID) + ".csv"
            with open(analyseddata_path, "rb") as attachment3:
                em.attach(MIMEApplication(attachment3.read(), Name=f"Analyseddata-{file_name}-{file_date}.csv"))

            # Login to server using secure context and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(sender_adress, password=em_password)
                server.sendmail(sender_adress, receiver_adress, em.as_string())
            print('results exported')
            return True
        except Exception as e:
            print(e)
            return False

        



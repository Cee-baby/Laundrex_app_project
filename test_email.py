import smtplib, ssl
from email.message import EmailMessage
port = 465
smtp_server = "smtp.zeptomail.com"
username="emailapikey"
password = "wSsVR613/EL3Dql7njL8Iu44y1lQVFnzEE180FOiv3P7Fv/FpcdtkkfNBFLxG/RNR2ZtQjIXoegokBwF1GZYh98lmwwHACiF9mqRe1U4J3x17qnvhDzNWW5bkRWLLYIAww1pnGRiEsgl+g=="
message = "our project is now global,yeeee!."
msg = EmailMessage()
msg['Subject'] = "Test Email"
msg['From'] = "noreply@laundrex.com.ng"
msg['To'] = "jideoforkosisochukwu20480agr@gmail.com"
msg.set_content(message)
try:
    if port == 465:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(username, password)
            server.send_message(msg)
    elif port == 587:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
    else:
        print ("use 465 / 587 as port value")
        exit()
    print ("successfully sent")
except Exception as e:
    print (e)
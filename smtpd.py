import smtplib

def send_email(to, subject, body):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("your@gmail.com", "APP_PASSWORD")
    server.sendmail(
        "your@gmail.com",
        to,
        f"Subject:{subject}\n\n{body}"
    )
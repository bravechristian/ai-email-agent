
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os

# Email credentials and server settings
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
IMAP_SERVER = 'mail.camuh.com.ng'
IMAP_PORT = 993
SMTP_SERVER = 'mail.camuh.com.ng'
SMTP_PORT = 465

# Keywords to identify quotation-related emails
QUOTATION_KEYWORDS = ['quotation', 'quote', 'pricing', 'invoice']

# Connect to the IMAP server and fetch unread emails
def fetch_unread_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    mail.select('inbox')

    status, response = mail.search(None, '(UNSEEN)')
    email_ids = response[0].split()
    emails = []

    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                emails.append(msg)

    mail.logout()
    return emails

# Check if the email is related to quotations
def is_quotation_email(msg):
    subject = msg['subject'].lower()
    body = msg.get_payload(decode=True).decode().lower()
    return any(keyword in subject or keyword in body for keyword in QUOTATION_KEYWORDS)

# Send an email
def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_address, msg.as_string())

# Generate a daily report
def send_daily_report(report):
    subject = 'Daily Business Activity Report'
    send_email(EMAIL_ADDRESS, subject, report)

# Main function to process emails and send replies
def main():
    emails = fetch_unread_emails()
    report = []

    for msg in emails:
        from_address = msg['from']
        subject = msg['subject']
        body = msg.get_payload(decode=True).decode()

        if is_quotation_email(msg):
            report.append(f'Skipped quotation email from {from_address} with subject: {subject}')
        else:
            reply_subject = f'Re: {subject}'
            reply_body = 'Thank you for your email. We will get back to you shortly.'
            send_email(from_address, reply_subject, reply_body)
            report.append(f'Replied to email from {from_address} with subject: {subject}')

    # Send daily report
    report_body = '\n'.join(report)
    send_daily_report(report_body)

if __name__ == '__main__':
    main()

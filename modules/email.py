import smtplib
import email.message

from utils.file import useFile
import re

def get_template(path, context):
    template = useFile(path)

    def convert(html, prop, key):
        return re.sub(r"\{\{\s*("+key+")\s*\}\}", str(prop), html)

    def formated(html, ctx):
        for key in context.keys():
            html = convert(html, ctx[key], key)
        return html

    return formated(template, context)

class Transport:
    def __init__(self, config):
        self.view = config['view']
        self.ext = config['ext']
        self.user = config['auth']['user']
        self.password = config['auth']['pass']
        self.s = smtplib.SMTP(config['smtp'])
        self.s.starttls()
        # Login Credentials for sending the mail
        self.s.login(self.user, self.password)

    def send_mail(self, options):
        html = get_template(self.view+options['template']+self.ext, options.get('context', {}))

        print(html)
        msg = email.message.Message()
        msg['Subject'] = options['subject']
        msg['From'] = options['from']
        msg['To'] = options['to']
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(html)

        self.s.sendmail(msg['From'], [msg['To']], msg.as_string().encode())
        print('Email enviado')


import os

email_user = os.getenv('EMAIL_USER')
email_pass = os.getenv('EMAIL_PASS')

if email_user == None: 
    raise Exception('Not Provider Email User')

if email_pass == None: 
    raise Exception('Not Provider Email Password')

transporter = Transport({
    'smtp': 'smtp.gmail.com: 587',
    'auth': {
        'user': email_user,
        'pass': email_pass
    },
    'view': '../resources/mail/',
    'ext': '.html'
})

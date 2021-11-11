from Dmail  import Email
with Email(mail_server='smtp.website.org',
           sender_email='sender@email',
           mail_port=25,
           mail_use_ssl=False,
           mail_use_tls=False) as email:
    email.send('body', 'recipient', subject='suject',
               attachments='path to attachment',
               subtype='html')
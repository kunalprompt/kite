import os
from logging.handlers import BufferingHandler
from smtplib import SMTP, SMTP_PORT

import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class KiteErrorsBufferEmailHandler(BufferingHandler):
    """
    This class handles the messages as per buffer capacity wrt handler definition.
    """

    def __init__(self, capacity, **kwargs):
        super().__init__(capacity=capacity)
        self.email_configs = {
            'mailhost': kwargs.get('mailhost', 'smtp.gmail.com'),
            'mailport': kwargs.get('mailport', 587),
            'from': os.environ['MONITOR_EMAIL_ADDR'],
            'to': kwargs['toaddrs'],
            'subject': kwargs['subject'],
            'credentials': (os.environ['MONITOR_EMAIL_ADDR'], os.environ['MONITOR_EMAIL_PASS'])
        }

    def emit(self, record):
        """
        Emit a record.

        Append the record. If shouldFlush() tells us to, call flush() to process
        the buffer.
        """
        self.buffer.append(record)

        if self.shouldFlush(record):
            for record in self.buffer:
                self.handler(record)
            self.flush()

    def flush(self):
        """
        This version not just zaps the buffer to empty, but emits all the pending messages.
        """
        for record in self.buffer:
            self.handler(record)
        super().flush()

    def handler(self, record):
        """
        customized handler to send emails from GMAIL SMTP
        :param record: the log item
        :return: None
        """
        try:
            port = self.email_configs['mailport']
            if not port:
                port = SMTP_PORT
            if isinstance(self.email_configs['to'], (tuple, list)):
                self.email_configs['to'] = ','.join(self.email_configs['to'])

            server = SMTP(self.email_configs['mailhost'], port)
            server.ehlo()
            server.starttls()
            server.login(self.email_configs['credentials'][0],
                         self.email_configs['credentials'][1])

            msg = self.draft_message(record)

            server.sendmail(self.email_configs['from'],
                            self.email_configs['to'],
                            msg.as_string())
            server.quit()
        except BaseException as ex:
            self.handleError(None)
            self.buffer = []

    def draft_message(self, record):
        """
        Override this to make magical messages
        :param record: the log
        :return: message
        """
        return self.draft_html_message(record, msg_type='html')

    def draft_text_message(self, record, msg_type='plain'):
        msg = MIMEMultipart()
        msg["From"] = self.email_configs['from']
        msg["To"] = self.email_configs['to']
        msg["Subject"] = self.email_configs['subject']
        msg['Date'] = str(email.utils.localtime())
        if msg_type == 'plain':
            msg.attach(MIMEText(self.format(record), _subtype='plain'))
        return msg

    def draft_html_message(self, record, msg_type='html'):
        _email_template = "templates/basic_template.html"
        template_path = "{}/{}".format(
            os.path.dirname(os.path.realpath(__file__))
            , _email_template
        )
        with open(template_path, "r") as fp:
            html = fp.read()

        html = html.format(self.format(record))
        msg = self.draft_text_message(record, msg_type=msg_type)
        msg.attach(MIMEText(html, 'html'))
        return msg

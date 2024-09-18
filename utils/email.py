import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.core.mail import (
    BadHeaderError,
    EmailMultiAlternatives,
    get_connection
)
from django.template.loader import render_to_string

from utils.debug import Debug


class _EmailHelper(object):
    def _recipient_list(self, recipients):
        if not recipients:
            return []

        if isinstance(recipients, list):
            return recipients

        data = []
        for recipient in recipients.split(','):
            data.append(recipient.strip())
        return data

    def _send(
        self, subject, body, from_email=None, to=None, bcc=None, cc=None,
        html_subject=None, html_body=None, filename=None, content=None,
        mimetype=None, context=None
    ):
        if settings.DO_NOT_SEND_EMAIL:
            return
        if settings.SEND_TEST_EMAIL:
            to = [settings.TEST_EMAIL_ADDRESS]
        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        if html_subject:
            subject = render_to_string(html_subject, context)
        subject = ''.join(subject.splitlines())

        email = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to,
            bcc=bcc,
            cc=cc
        )
        if html_body:
            html_email = render_to_string(html_body, context)
            email.attach_alternative(html_email, 'text/html')
        if filename and content and mimetype:
            email.attach(filename, content, mimetype)
        elif filename:
            email.attach_file(filename)

        try:
            email.send(fail_silently=False)
        except BadHeaderError:
            Debug.error("BadHeaderError")
        except smtplib.SMTPException:
            Debug.error("SMTPException")

    def send_to(
        self, subject, body, from_email=None, user=None, email=None,
        html_subject=None, html_body=None, filename=None, content=None,
        mimetype=None, context=None
    ):
        """
        Send a single email to a single user or email

        to send html subject, pass return of render_to_string
        """
        if not user and not email:
            raise AssertionError("Either user or email should be presented.")
        elif not email:
            email = user.email
        Debug.trace(" Sending mail to %s" % email)

        self._send(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[email],
            html_subject=html_subject,
            html_body=html_body,
            filename=filename,
            content=content,
            mimetype=mimetype,
            context=context
        )

    def send_direct(
        self, subject, body, from_email=None, user=None, email=None,
        html_subject=None, html_body=None, filename=None, content=None,
        mimetype=None, context=None
    ):
        """
        Send a single email to a single user or email

        using smtplib send directly
        """
        if not user and not email:
            raise AssertionError("Either user or email should be presented.")
        elif not email:
            email = user.email
        Debug.trace(" Sending smtp mail to %s" % email)

        if settings.DO_NOT_SEND_EMAIL:
            return
        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        if html_subject:
            subject = render_to_string(html_subject, context)
        subject = ''.join(subject.splitlines())

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = email

        if html_body:
            html_email = render_to_string(html_body, context)
            msg.attach(MIMEText(html_email, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))

        mail = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mail.ehlo()
        mail.starttls()
        mail.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        mail.sendmail(from_email, email, msg.as_string())
        mail.quit()

    def send_bcc(
        self, subject, body, from_email=None, to=None, recipients=None,
        html_subject=None, html_body=None, filename=None, content=None,
        mimetype=None, context=None
    ):
        """
        Send a single email to single or multiple recipient as cc

        to send html subject, pass return of render_to_string
        """
        bcc = self._recipient_list(recipients)
        Debug.trace(" Sending mail to %d bcc" % len(bcc))

        self._send(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to],
            bcc=bcc,
            html_subject=html_subject,
            html_body=html_body,
            filename=filename,
            content=content,
            mimetype=mimetype,
            context=context
        )

    def send(
        self, subject, body, from_email=None, to=None, cc=None, bcc=None,
        html_subject=None, html_body=None, filename=None, content=None,
        mimetype=None, context=None
    ):
        """
        Send a single email to single or multiple recipient as to or cc

        This is the best fucntion you choose for sending common emails
        """
        to = self._recipient_list(to)
        cc = self._recipient_list(cc)
        bcc = self._recipient_list(bcc)
        Debug.trace(" Sending mail to %s, cc %s, bcc %s." % (
            to, cc, bcc
        ))

        self._send(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to,
            cc=cc,
            bcc=bcc,
            html_subject=html_subject,
            html_body=html_body,
            filename=filename,
            content=content,
            mimetype=mimetype,
            context=context
        )

    def send_mass(self, messages):
        """
        Send multiple emails at once

        messages are list of EmailMultiAlternatives
        """
        if settings.DO_NOT_SEND_EMAIL:
            return
        connection = get_connection(fail_silently=False)
        Debug.trace(" Sending %d mass messages" % len(messages))
        connection.send_messages(messages)
        Debug.trace(" Sending mass messages completed.")


EmailHelper = _EmailHelper()

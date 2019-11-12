import os
import requests
from pyfcm import FCMNotification
from flask import Flask, request, jsonify, url_for, redirect, render_template

push_service = None
FIREBASE_KEY = os.environ.get('FIREBASE_KEY')
if(FIREBASE_KEY and FIREBASE_KEY!=''):
    push_service = FCMNotification(api_key=FIREBASE_KEY)
EMAIL_NOTIFICATIONS_ENABLED = os.environ.get('EMAIL_NOTIFICATIONS_ENABLED')

def send_email_message(slug, to, data={}):
    if EMAIL_NOTIFICATIONS_ENABLED == 'TRUE':
        template = get_template_content(slug, data, ["email"])
        # print('Email notification '+slug+' sent')
        return requests.post(
            "https://api.mailgun.net/v3/mailgun.jobcore.co/messages",
            auth=(
                "api",
                os.environ.get('MAILGUN_API_KEY')),
            data={
                "from": os.environ.get('MAILGUN_FROM') +
                " <mailgun@mailgun.jobcore.co>",
                "to": to,
                "subject": template['subject'],
                "text": template['text'],
                "html": template['html']}).status_code == 200
    else:
        # print('Email not sent because notifications are not enabled')
        return True

def send_sms(slug, phone_number, data={}):

    template = get_template_content(slug, data, ["email", "fms"])
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    TWILLIO_SID = os.environ.get('TWILLIO_SID')
    TWILLIO_SECRET = os.environ.get('TWILLIO_SECRET')
    client = Client(TWILLIO_SID, TWILLIO_SECRET)

    message = client.messages \
                    .create(
                        body=template['fms'],
                        from_='+15017122661',
                        to='+15558675310'
                    )


def send_fcm(slug, registration_ids, data={}):
    if(len(registration_ids) > 0 and push_service):
        template = get_template_content(slug, data, ["email", "fms"])

        if 'fms' not in template:
            raise APIException(
                "The template " +
                slug +
                " does not seem to have a valid FMS version")

        message_title = template['subject']
        message_body = template['fms']
        if 'DATA' not in data:
            raise Exception("There is no data for the notification")
        message_data = data['DATA']

        result = push_service.notify_multiple_devices(
            registration_ids=registration_ids,
            message_title=message_title,
            message_body=message_body,
            data_message=message_data)

        # if(result["failure"] or not result["success"]):
        #     raise APIException("Problem sending the notification")

        return result
    else:
        return False


def send_fcm_notification(slug, user_id, data={}):
    device_set = FCMDevice.objects.filter(user=user_id)
    registration_ids = [device.registration_id for device in device_set]
    send_fcm(slug, registration_ids, data)


def get_template_content(slug, data={}, formats=None):
    info = get_template_info(slug)

    #d = Context({ 'username': username })
    con = {
        'API_URL': os.environ.get('API_URL'),
        'COMPANY_NAME': 'Swap App',
        'COMPANY_LEGAL_NAME': 'Swap App LLC',
        'COMPANY_ADDRESS': '2323 Hello, Coral Gables, 33134'
    }
    z = con.copy()   # start with x's keys and values
    z.update(data)

    templates = {
        "subject": info['subject']
    }

    if formats is None or "email" in formats:
        plaintext = get_template(info['type'] + '/' + slug + '.txt')
        html = get_template(info['type'] + '/' + slug + '.html')
        templates["text"] = plaintext.render(z)
        templates["html"] = html.render(z)

    if formats is not None and "fms" in formats:
        fms = get_template(info['type'] + '/' + slug + '.fms')
        templates["fms"] = fms.render(z)

    return templates


def get_template_info(slug):
    subjects = {
        "general": {"type": "utils", "subject": "Important message from JobCore"},
        "email_validated": {"type": "views", "subject": "Your email has been validated"},
        "reset_password_form": {"type": "views", "subject": "Reset your password"},
        "registration": {"type": "registration", "subject": "Welcome to JobCore"},
        "password_reset_link": {"type": "registration", "subject": "About your password reset"},
        "password_reset": {"type": "registration", "subject": "You password has been reset"},

        "update_chips": {
            "type": "tournament",
            "subject": "Remember to update your chipts"
        },
    }
    if slug in subjects:
        return subjects[slug]
    else:
        raise ValueError(
            'Invalid template slug: "' +
            slug +
            "' no subject found")
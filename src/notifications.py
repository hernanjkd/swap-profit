import os
import requests
from flask import Flask, request, jsonify, url_for, redirect, render_template
from models import Devices
# from pyfcm import FCMNotification

push_service = None
FIREBASE_KEY = os.environ.get('FIREBASE_KEY')
if(FIREBASE_KEY and FIREBASE_KEY != ''):
    push_service = FCMNotification(api_key=FIREBASE_KEY)

EMAIL_NOTIFICATIONS_ENABLED = os.environ.get('EMAIL_NOTIFICATIONS_ENABLED')



def send_email(type, to, data={}):
    
    if EMAIL_NOTIFICATIONS_ENABLED == 'TRUE':
        
        template = get_template_content(type, data, ['email'])
        domain = os.environ.get('MAILGUN_DOMAIN')

        r = requests.post(f'https://api.mailgun.net/v3/{domain}/messages',
            auth=(
                'api',
                os.environ.get('MAILGUN_API_KEY')),
            data={
                'from': f'{domain} <mailgun@swapprofit-test.herokuapp.com>',
                'to': to,
                'subject': template['subject'],
                'text': template['text'],
                'html': template['html']
            })
        
        return r
        
    return False



def send_sms(type, phone_number, data={}):

    template = get_template_content(type, data, ['email', 'fms'])
    
    TWILIO_SID = os.environ.get('TWILIO_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    message = client.messages \
                    .create(
                        body=template['fms'],
                        from_='+15017122661',
                        to='+15558675310'
                    )



def send_fcm(type, user_id, data={}):
    
    devices = Devices.query.filter_by( user_id = user_id )
    registration_ids = [device.token for device in devices]

    if(len(registration_ids) == 0 or push_service is None):
        return False
    
    template = get_template_content(type, data, ['fms'])

    if 'fms' not in template:
        raise APIException(
            f'The template {type} does not seem to have a valid FMS version')

    message_title = template['subject']
    message_body = template['fms']
    if 'data' not in data:
        raise Exception('There is no data for the notification')
    message_data = data['data']

    result = push_service.notify_multiple_devices(
        registration_ids=registration_ids,
        message_title=message_title,
        message_body=message_body,
        data_message=message_data
    )

    if(result['failure'] or not result['success']):
        raise Exception('Problem sending the notification')

    return result
    


def get_template_content(type, data={}, formats=None):
    
    subjects = {
        'email_validation': 'Swap Profit: Email Validation',
        'swap_created': 'Swap Profit: You Have A New Swap',
        'buyin_receipt': 'Swap Profit: Your Buy In Receipt',
        'account_created': 'Swap Profit: Welcome to Swap Profit'
    }

    con = {
        'API_URL': os.environ.get('API_URL'),
        'COMPANY_NAME': 'Swap Profit',
        'COMPANY_LEGAL_NAME': 'Swap Profit LLC',
        'COMPANY_ADDRESS': '2323 Hello, Coral Gables, 33134'
    }
    template_data = {**con, **data}
    
    templates = {
        'subject': subjects[type]
    }

    if formats is None or 'email' in formats:
        templates['text'] = render_template( type +'.txt', **template_data)
        templates['html'] = render_template( type +'.html', **template_data)

    if formats is not None and 'fms' in formats:
        templates['fms'] = render_template( type +'.fms', **template_data)

    
    return templates

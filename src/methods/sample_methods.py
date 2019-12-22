from flask import Flask, jsonify, request
from notifications import send_email
import requests
import os

def attach(app):

    @app.route('/sendemail')
    def sendemailtest():
        msg = {'name':'Hello Hernan'}
        send_email(type='account_created',to='hernanjkd@gmail.com',data=msg)
        l = 'testing'
        return 'email sent'


    @app.route('/testing', methods=['GET'])
    def first_endpoint():
        return jsonify({ 'details': "All good my friend"}), 200

    @app.route('/mailgun')
    def get_logs():
        return jsonify( requests.get(
            f"https://api.mailgun.net/v3/{os.environ.get('MAILGUN_DOMAIN')}/events",
            auth=("api", os.environ.get("MAILGUN_API_KEY")),
            params={"begin"       : "Fri, 13 DEC 2019 09:00:00 -0000",
                    "ascending"   : "yes",
                    "limit"       :  25,
                    "pretty"      : "yes",
                    "recipient" : "hernanjkd@gmail.com"}).json())

    @app.route('/ocr_image', methods=['PUT'])
    def ocr():
        import cloudinary
        from google.cloud import vision

        # return cloudinary.uploader.destroy('ocr')

        result = cloudinary.uploader.upload(
            request.files['image'],
            public_id='ocr',
            crop='limit',
            width=450,
            height=450,
            eager=[{
                'width': 200, 'height': 200,
                'crop': 'thumb', 'gravity': 'face',
                'radius': 100
            }],
            tags=[
                'buyin_receipt',
                f'user_',
                f'buyin_'
            ]
        )
        
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = result['secure_url']

        response = client.text_detection(image=image)
        texts = response.text_annotations

        return jsonify(texts[0].description)

    return app
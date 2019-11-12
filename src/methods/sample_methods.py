from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_jwt_simple import JWTManager, create_jwt, decode_jwt, get_jwt

def attach(app):

    @app.route('/testing', methods=['GET'])
    def first_endpoint():
        return jsonify({ 'details': "All good my friend"}), 406

    return app
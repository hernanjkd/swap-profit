
import os
from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, decode_jwt, get_jwt
from utils import APIException, generate_sitemap, check_params, validation_link, update_table, sha256
from dummy_data import buy_ins, flights, swaps, profiles, tournaments
from models import db, Users, Profiles, Tournaments, Swaps, Flights, Buy_ins, Transactions, Tokens
from datetime import datetime, timedelta



def update_user(data, user):
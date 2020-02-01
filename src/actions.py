import os
import ocr
import json
import cloudinary
import cloudinary.uploader
from google.cloud import vision
from datetime import datetime, timedelta
from flask import request, jsonify, render_template
from flask_jwt_simple import create_jwt, decode_jwt, get_jwt
from sqlalchemy import desc, asc
from utils import (APIException, check_params, jwt_link, update_table, 
    sha256, role_jwt_required, resolve_pagination, isFloat)
from models import (db, Users, Profiles, Tournaments, Swaps, Flights, 
    Buy_ins, Transactions, Devices)
from notifications import send_email, send_fcm



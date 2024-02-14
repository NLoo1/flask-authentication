from flask import Blueprint, flash, redirect, render_template, request, jsonify

from .models import db

rts = Blueprint('rts', __name__)

@rts.route("/", methods=['POST', 'GET'])
def home():
    return 'oogba booga'
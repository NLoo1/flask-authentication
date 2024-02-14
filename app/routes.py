from flask import Blueprint, flash, redirect, render_template, request, jsonify, session

from .models import db

rts = Blueprint('rts', __name__)

@rts.route("/", methods=['POST', 'GET'])
def home():
    return 'oogba booga'


@rts.route('/logout')
def logout():
    session.pop('user_id')
    flash('You have successfully logged out.')
    return redirect('/')
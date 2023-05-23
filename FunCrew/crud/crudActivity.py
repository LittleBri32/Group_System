from flask import Blueprint, request, render_template, session, redirect
import sqlite3 as sql

activity_bp = Blueprint('Activity', __name__)



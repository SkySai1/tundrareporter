from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():
    if 'epics' in request.files and 'stories' in request.files and 'tasks' in request.files:
        epics_file = request.files['epics']
        stories_file = request.files['stories']
        tasks_file = request.files['tasks']

        epics = pd.read_csv(epics_file)
        stories = pd.read_csv(stories_file)
        tasks = pd.read_csv(tasks_file)

        # Here, you would process the data and save it to the database

        return redirect(url_for('main.index'))

    return 'Missing files', 400
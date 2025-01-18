from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import requests
import os

main = Blueprint('main', __name__)

# Получаем разделитель из переменной окружения или используем ',' по умолчанию
CSV_SEPARATOR = os.getenv('CSV_SEPARATOR', ',')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():
    # Обработка файлов
    epics_file = request.files.get('epics')
    stories_file = request.files.get('stories')
    tasks_file = request.files.get('tasks')

    # Обработка ссылок
    epics_url = request.form.get('epics_url')
    stories_url = request.form.get('stories_url')
    tasks_url = request.form.get('tasks_url')

    try:
        # Загрузка данных
        if epics_file:
            epics = pd.read_csv(epics_file, sep=CSV_SEPARATOR, encoding='utf-8', on_bad_lines='skip')
        elif epics_url:
            epics_content = requests.get(epics_url).content.decode('utf-8')
            epics = pd.read_csv(pd.compat.StringIO(epics_content), sep=CSV_SEPARATOR, on_bad_lines='skip')
        else:
            return 'Epics file or URL is required', 400

        if stories_file:
            stories = pd.read_csv(stories_file, sep=CSV_SEPARATOR, encoding='utf-8', on_bad_lines='skip')
        elif stories_url:
            stories_content = requests.get(stories_url).content.decode('utf-8')
            stories = pd.read_csv(pd.compat.StringIO(stories_content), sep=CSV_SEPARATOR, on_bad_lines='skip')
        else:
            return 'Stories file or URL is required', 400

        if tasks_file:
            tasks = pd.read_csv(tasks_file, sep=CSV_SEPARATOR, encoding='utf-8', on_bad_lines='skip')
        elif tasks_url:
            tasks_content = requests.get(tasks_url).content.decode('utf-8')
            tasks = pd.read_csv(pd.compat.StringIO(tasks_content), sep=CSV_SEPARATOR, on_bad_lines='skip')
        else:
            return 'Tasks file or URL is required', 400

        # Здесь можно обработать данные или сохранить их в БД

        return redirect(url_for('main.index'))

    except Exception as e:
        return f'Error processing files or URLs: {str(e)}', 500
from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import requests
import os
from .validators import validate_csv
from .data_processor import process_data

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

    # Проверка на пустые файлы
    if epics_file and epics_file.filename != '' and epics_file.read(1) != b'':
        epics_file.seek(0)  # Перемещаем указатель в начало файла после чтения
    else:
        return "Epics file is empty or missing", 400

    if stories_file and stories_file.filename != '' and stories_file.read(1) != b'':
        stories_file.seek(0)
    else:
        return "Stories file is empty or missing", 400

    if tasks_file and tasks_file.filename != '' and tasks_file.read(1) != b'':
        tasks_file.seek(0)
    else:
        return "Tasks file is empty or missing", 400

    # Загрузка CSV в DataFrame
    epics_df = pd.read_csv(epics_file, sep=CSV_SEPARATOR)
    stories_df = pd.read_csv(stories_file, sep=CSV_SEPARATOR)
    tasks_df = pd.read_csv(tasks_file, sep=CSV_SEPARATOR)

    try:
        # Обработка данных
        task_model = process_data(epics_df, stories_df, tasks_df)

        # Передача данных в шаблон для отображения
        return render_template('results.html', task_model=task_model)

    except ValueError as e:
        import logging
        logging.exception(e)
        return f"Data processing error: {str(e)}", 400
    except Exception as e:
        return f"Unexpected error: {str(e)}", 500
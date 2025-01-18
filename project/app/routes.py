from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
import pandas as pd
import os
import uuid
import requests
from io import StringIO
from .validators import validate_csv
from .data_processor import process_data
import logging

main = Blueprint('main', __name__)

# Получаем разделитель из переменной окружения или используем ',' по умолчанию
CSV_SEPARATOR = os.getenv('CSV_SEPARATOR', ',')

# Папка для хранения CSV файлов
DATA_FOLDER = os.path.join(os.getcwd(), 'public', 'data')
os.makedirs(DATA_FOLDER, exist_ok=True)  # Создаём папку, если она не существует

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
        task_model, csv_data = process_data(epics_df, stories_df, tasks_df)

        # Генерируем уникальный ID для файла
        file_id = str(uuid.uuid4())

        # Путь к файлу, где будет сохранён CSV
        file_path = os.path.join(DATA_FOLDER, f"{file_id}.csv")

        # Сохраняем CSV данные в файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(csv_data)

        # Передача данных в шаблон для отображения (передаем file_id для скачивания)
        return render_template('results.html', task_model=task_model, file_id=file_id)

    except ValueError as e:
        import logging
        logging.exception(e)
        return f"Data processing error: {str(e)}", 400
    except Exception as e:
        return f"Unexpected error: {str(e)}", 500

# Получаем разделитель из переменной окружения или используем ',' по умолчанию
CSV_SEPARATOR = os.getenv('CSV_SEPARATOR', ',')

# Папка для сохранения файлов
DATA_FOLDER = os.path.join(os.getcwd(), 'public', 'data')
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def download_csv(url):
    """Функция для скачивания CSV-файла по URL."""
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()  # Проверим, что запрос успешен (200 OK)
        return StringIO(response.text)  # Читаем текстовый контент как StringIO (что эквивалентно файлу в памяти)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading CSV from {url}: {str(e)}")
        raise ValueError(f"Error downloading CSV from {url}: {str(e)}")  # Бросаем ошибку, если не удалось загрузить

@main.route('/upload_from_url', methods=['POST'])
def upload_from_url():
    # Получаем URL файлов
    epics_url = request.form.get('epics_url')
    stories_url = request.form.get('stories_url')
    tasks_url = request.form.get('tasks_url')

    # Проверка на пустые URL
    if not epics_url or not stories_url or not tasks_url:
        return "All URLs are required", 400

    try:
        # Загрузка CSV файлов по URL
        epics_df = pd.read_csv(download_csv(epics_url), sep=CSV_SEPARATOR)
        stories_df = pd.read_csv(download_csv(stories_url), sep=CSV_SEPARATOR)
        tasks_df = pd.read_csv(download_csv(tasks_url), sep=CSV_SEPARATOR)

        # Обработка данных
        task_model, csv_data = process_data(epics_df, stories_df, tasks_df)

        # Генерация уникального ID для файла
        file_id = str(uuid.uuid4())

        # Путь к файлу, где будет сохранён CSV
        file_path = os.path.join(DATA_FOLDER, f"{file_id}.csv")

        # Сохраняем CSV данные в файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(csv_data)

        # Передача данных в шаблон для отображения (передаем file_id для скачивания)
        return render_template('results.html', task_model=task_model, file_id=file_id)

    except ValueError as e:
        logging.exception(e)
        return f"Data processing error: {str(e)}", 400
    except Exception as e:
        return f"Unexpected error: {str(e)}", 500
    
@main.route('/download/<file_id>', methods=['GET'])
def download(file_id):
    # Путь к файлу
    file_path = os.path.join(DATA_FOLDER, f"{file_id}.csv")

    # Проверяем существует ли файл
    if os.path.exists(file_path):
        # Отправляем файл для скачивания
        return send_from_directory(DATA_FOLDER, f"{file_id}.csv", as_attachment=True)
    else:
        return "File not found", 404

from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import requests
import os
from .validators import validate_csv

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

    # Ожидаемые колонки для каждого типа файла
    epics_columns = [
        'id', 'ref', 'subject', 'description', 'owner', 'owner_full_name',
        'assigned_to', 'assigned_to_full_name', 'status', 'epics_order',
        'client_requirement', 'team_requirement', 'attachments', 'tags',
        'watchers', 'voters', 'created_date', 'modified_date', 'related_user_stories'
    ]
    required_epic_columns = [
        'id', 'ref', 'subject', 'status', 'created_date', 'modified_date'
    ]

    stories_columns = [
        'id', 'ref', 'subject', 'description', 'sprint_id', 'sprint', 'sprint_estimated_start',
        'sprint_estimated_finish', 'owner', 'owner_full_name', 'assigned_to',
        'assigned_to_full_name', 'assigned_users', 'assigned_users_full_name',
        'status', 'is_closed', 'swimlane', 'ekspert-points', 'total-points',
        'backlog_order', 'sprint_order', 'kanban_order', 'created_date', 'modified_date',
        'finish_date', 'client_requirement', 'team_requirement', 'attachments',
        'generated_from_issue', 'generated_from_task', 'from_task_ref',
        'external_reference', 'tasks', 'tags', 'watchers', 'voters', 'due_date',
        'due_date_reason', 'epics'
    ]
    required_story_columns = [
        'id', 'ref', 'subject', 'status', 'created_date', 'modified_date'
    ]

    tasks_columns = [
        'id', 'ref', 'subject', 'description', 'user_story', 'sprint_id', 'sprint',
        'sprint_estimated_start', 'sprint_estimated_finish', 'owner', 'owner_full_name',
        'assigned_to', 'assigned_to_full_name', 'status', 'is_iocaine', 'is_closed',
        'us_order', 'taskboard_order', 'attachments', 'external_reference', 'tags',
        'watchers', 'voters', 'created_date', 'modified_date', 'finished_date',
        'due_date', 'due_date_reason'
    ]
    required_task_columns = [
        'id', 'ref', 'subject', 'status', 'created_date', 'modified_date'
    ]

    try:
        # Валидация файлов с учётом разделителя
        if epics_file:
            valid, error = validate_csv(epics_file, epics_columns, sep=CSV_SEPARATOR, required_columns=required_epic_columns)
            if not valid:
                return f"Validation error for Epics file: {error}", 400

        if stories_file:
            valid, error = validate_csv(stories_file, stories_columns, sep=CSV_SEPARATOR, required_columns=required_story_columns)
            if not valid:
                return f"Validation error for Stories file: {error}", 400

        if tasks_file:
            valid, error = validate_csv(tasks_file, tasks_columns, sep=CSV_SEPARATOR, required_columns=required_task_columns)
            if not valid:
                return f"Validation error for Tasks file: {error}", 400

        # Продолжение обработки данных...

        return redirect(url_for('main.index'))

    except Exception as e:
        return f"Error processing files: {str(e)}", 500
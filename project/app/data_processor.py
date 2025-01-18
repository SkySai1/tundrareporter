import pandas as pd
import os

def process_data(epics_df, stories_df, tasks_df):
    task_model = []

    # Преобразуем эпики в словарь для быстрого поиска по числовым ref
    epics_dict = {int(epic['ref']): epic['subject'] for _, epic in epics_df.iterrows()}  # Сохраняем эпики как числовые ключи
    stories_dict = {int(story['ref']): story for _, story in stories_df.iterrows()}  # Аналогично для историй

    # Считаем количество задач, привязанных к каждой истории
    task_count_per_story = tasks_df.groupby('user_story')['ref'].count()  # Подсчитываем задачи для каждой истории

    for _, task in tasks_df.iterrows():
        # Заполняем информацию о задаче
        task_ref = task['ref']
        task_subject = task['subject']
        story_ref = task.get('user_story', None)  # ref истории (может быть None)

        # Проверяем, если story_ref не пустое
        if pd.notna(story_ref):  # Проверяем, что story_ref не NaN
            story = stories_dict.get(int(story_ref), None)  # Преобразуем в int только если story_ref не NaN
        else:
            story = None

        # Если история существует, получаем её данные
        if story is not None:
            story_subject = story['subject']
            total_points = story['total-points'] if 'total-points' in story else 0.0
            epic_refs = story.get('epics', None)  # Получаем информацию об эпиках из истории
        else:
            story_subject = 'No story'
            total_points = 0.0
            epic_refs = None

        # Получаем количество задач, привязанных к истории
        num_tasks_in_story = task_count_per_story.get(int(story_ref), 1) if pd.notna(story_ref) else 1  # Защита от деления на 0

        # Расчет очков на задачу
        points_per_task = total_points / num_tasks_in_story if num_tasks_in_story > 0 else 0.0

        # Обработка привязки к эпикам (если несколько эпиков, то разбиваем их по запятой)
        epic_subjects = []
        if epic_refs and pd.notna(epic_refs):  # Проверяем, что epic_refs не пусто и не NaN
            if isinstance(epic_refs, str):
                epic_refs_list = [int(epic.strip()) for epic in epic_refs.split(',')]  # Преобразуем каждый эпик в int
            else:
                epic_refs_list = [int(epic_refs)]
            for epic_ref in epic_refs_list:
                # Проверка, если epic_ref находится в epics_dict
                if epic_ref in epics_dict:
                    epic_subjects.append(epics_dict[epic_ref])  # Добавляем название эпика
                else:
                    epic_subjects.append('Unknown Epic')  # Если эпика нет в словаре, добавляем заглушку
        else:
            epic_subjects.append('No epic')  # Если эпиков нет в истории

        epic_subject = ', '.join(epic_subjects) if epic_subjects else 'No epic'

        # Получаем информацию о спринте (может быть None)
        sprint = task.get('sprint', None)  # если спринт не указан, будет None

        # Получаем специалиста (может быть None)
        specialist = task.get('assigned_to_full_name', None)  # если специалист не указан, будет None

        # Получаем информацию о статусе задачи
        status = task['status']
        created_date = task['created_date']
        modified_date = task['modified_date']

        # Добавляем информацию о задаче в модель
        task_model.append({
            'task_ref': task_ref,
            'task_subject': task_subject,
            'story_subject': story_subject,
            'epic_subject': epic_subject,
            'points_per_task': points_per_task,
            'specialist': specialist,
            'status': status,
            'created_date': created_date,
            'modified_date': modified_date,
            'sprint': sprint
        })

    # Преобразуем модель в DataFrame
    task_model_df = pd.DataFrame(task_model)

    # Получаем сепаратор из переменной окружения или по умолчанию запятая
    csv_separator = os.getenv('CSV_SEPARATOR', ',')

    # Преобразуем DataFrame в CSV
    csv_data = task_model_df.to_csv(index=False, sep=csv_separator)

    return task_model, csv_data
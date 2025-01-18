import pandas as pd
import logging

def process_data(epics_df, stories_df, tasks_df):
    task_model = []

    # Преобразуем эпики и истории в удобные словари для быстрого поиска по ref
    epics_dict = {epic['ref']: epic['subject'] for _, epic in epics_df.iterrows()}
    stories_dict = {story['ref']: story for _, story in stories_df.iterrows()}  # Сохраняем всю строку истории

    # Считаем количество задач, привязанных к каждой истории
    # Для этого смотрим, сколько задач в таблице tasks_df имеют ссылку на эту историю
    task_count_per_story = tasks_df.groupby('user_story')['ref'].count()  # Подсчитываем задачи для каждой истории

    for _, task in tasks_df.iterrows():
        # Заполняем информацию о задаче
        task_ref = task['ref']
        task_subject = task['subject']
        story_ref = task.get('user_story', None)  # ref истории (может быть None)
        epic_refs = task.get('epic_id', None)  # ref эпиков (может быть None, или несколько через запятую)

        # Проверяем, если story_ref не пустое
        story = stories_dict.get(story_ref) if pd.notna(story_ref) else None

        # Если история существует, получаем её данные
        if story is not None:
            story_subject = story['subject']
            total_points = story['total-points'] if 'total-points' in story else 0.0
        else:
            story_subject = 'No story'
            total_points = 0.0

        # Получаем количество задач, привязанных к истории
        num_tasks_in_story = task_count_per_story.get(story_ref, 1)  # Защита от деления на 0

        # Расчет очков на задачу
        points_per_task = total_points / num_tasks_in_story if num_tasks_in_story > 0 else 0.0

        # Обработка привязки к эпикам (если несколько эпиков, то разбиваем по запятой)
        epic_subjects = []
        if epic_refs:
            epic_refs_list = epic_refs.split(',') if isinstance(epic_refs, str) else [epic_refs]
            for epic_ref in epic_refs_list:
                if epic_ref in epics_dict:
                    epic_subjects.append(epics_dict[epic_ref])
                else:
                    epic_subjects.append('Unknown Epic')

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

    return task_model
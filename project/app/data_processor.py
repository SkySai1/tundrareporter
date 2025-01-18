import pandas as pd

def process_data(epics_df, stories_df, tasks_df):
    task_model = []

    # Преобразуем эпики и истории в удобные словари для быстрого поиска по ref
    epics_dict = {epic['ref']: epic['subject'] for _, epic in epics_df.iterrows()}
    stories_dict = {story['ref']: story for _, story in stories_df.iterrows()}  # Сохраняем всю строку истории
    story_task_count = stories_df.groupby('ref')['ref'].count()  # Считаем количество задач, привязанных к каждой истории

    for _, task in tasks_df.iterrows():
        # Заполняем информацию о задаче
        task_ref = task['ref']
        task_subject = task['subject']
        story_ref = task.get('user_story', None)  # ref истории (может быть None)
        epic_ref = task.get('epic_id', None)  # ref эпика (может быть None)

        # Проверяем, если story_ref не пустое
        story = stories_dict.get(story_ref) if pd.notna(story_ref) else None

        # Если история существует, получаем её данные
        if story is not None:
            story_subject = story['subject']
        else:
            story_subject = 'No story'

        # Получаем информацию о эпике
        if epic_ref and epic_ref in epics_dict:
            epic_subject = epics_dict[epic_ref]
        else:
            epic_subject = 'No epic'

        # Получаем информацию о спринте (может быть None)
        sprint = task.get('sprint', None)  # если спринт не указан, будет None

        # Получаем специалиста (может быть None)
        specialist = task.get('assigned_to_full_name', None)  # если специалист не указан, будет None

        # Проверка наличия 'total-points' в истории
        if story is not None and 'total-points' in story:
            total_points = story['total-points']
        else:
            total_points = 0.0

        # Количество задач в истории (если история существует)
        num_tasks_in_story = story_task_count.get(story_ref, 1)  # Защита от деления на 0

        # Расчет очков на задачу (делим очки истории на количество задач в истории)
        points_per_task = total_points / num_tasks_in_story if num_tasks_in_story > 0 else 0.0

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
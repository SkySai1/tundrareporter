import pytest
import pandas as pd
from app.data_processor import process_data

# Тест на проверку корректности связей в отчете между эпиками, историями и задачами

def test_report_links():
    # Создаем данные для теста
    epics_data = {'id': [1, 2], 'subject': ['Epic 1', 'Epic 2']}
    stories_data = {'id': [101, 102], 'epics': [1, 999], 'subject': ['Story 1', 'Story 2']}  # История 102 без эпику
    tasks_data = {'id': [1001, 1002], 'user_story': [101, 999], 'subject': ['Task 1', 'Task 2']}  # Задача 1002 без истории

    epics_df = pd.DataFrame(epics_data)
    stories_df = pd.DataFrame(stories_data)
    tasks_df = pd.DataFrame(tasks_data)

    # Обработка данных
    enriched_epics, enriched_stories, enriched_tasks = process_data(epics_df, stories_df, tasks_df)

    # Проверяем, что задачи привязаны к правильной истории
    assert enriched_tasks['story_id'].iloc[0] == '101'  # Задача 1001 должна быть привязана к истории 101
    assert enriched_tasks['story_subject'].iloc[0] == 'Story 1'  # Задача 1001 должна иметь тему истории 'Story 1'

    # Проверяем, что задачи без привязки к истории привязаны к заглушке
    assert enriched_tasks['story_id'].iloc[1] == '0'  # Задача 1002 без истории должна быть привязана к пустой истории
    assert enriched_tasks['story_subject'].iloc[1] == 'Без истории'  # Заглушка для задачи 1002

    # Проверяем, что истории привязаны к правильному эпику
    assert enriched_stories['epic_id'].iloc[0] == '1'  # История 101 должна быть привязана к эпику 1
    assert enriched_stories['epic_subject'].iloc[0] == 'Epic 1'  # История 101 должна иметь тему эпика 'Epic 1'

    # Проверяем, что истории без привязки к эпику привязаны к заглушке
    assert enriched_stories['epic_id'].iloc[1] == '0'  # История 102 без эпика должна быть привязана к пустому эпику
    assert enriched_stories['epic_subject'].iloc[1] == 'Без эпика'  # Заглушка для истории 102

    # Проверяем, что эпики остались правильными
    assert enriched_epics['id'].iloc[0] == '1'  # Эпик 1 должен остаться правильным
    assert enriched_epics['subject'].iloc[0] == 'Epic 1'  # Эпик 1 должен иметь правильную тему

    assert enriched_epics['id'].iloc[1] == '2'  # Эпик 2 должен остаться правильным
    assert enriched_epics['subject'].iloc[1] == 'Epic 2'  # Эпик 2 должен иметь правильную тему
import pytest
import pandas as pd
from app.data_processor import process_data

# 1. Тест на пустые файлы

def test_empty_files():
    empty_df = pd.DataFrame(columns=['id', 'subject'])
    epics_df = empty_df.copy()
    stories_df = empty_df.copy()
    tasks_df = empty_df.copy()

    # Проверяем, что будет выброшена ошибка на отсутствие обязательных колонок
    with pytest.raises(ValueError, match="Missing required columns in Stories data"):
        process_data(epics_df, stories_df, tasks_df)

# 2. Тест на задачи без истории

def test_tasks_without_story():
    epics_data = {'id': [1], 'subject': ['Epic 1']}
    stories_data = {'id': [101], 'epics': [1], 'subject': ['Story 1']}
    tasks_data = {'id': [1001, 1002], 'user_story': [999, 999], 'subject': ['Task 1', 'Task 2']}  # Invalid stories

    epics_df = pd.DataFrame(epics_data)
    stories_df = pd.DataFrame(stories_data)
    tasks_df = pd.DataFrame(tasks_data)

    enriched_epics, enriched_stories, enriched_tasks = process_data(epics_df, stories_df, tasks_df)

    # Ensure that tasks without a valid story are assigned to the placeholder story
    assert enriched_tasks['story_id'].iloc[0] == '0'

# 3. Тест на истории без эпиков

def test_stories_without_epic():
    epics_data = {'id': [1], 'subject': ['Epic 1']}
    stories_data = {'id': [101], 'epics': [999], 'subject': ['Story 1']}  # Invalid epic ID
    tasks_data = {'id': [1001], 'user_story': [101], 'subject': ['Task 1']}

    epics_df = pd.DataFrame(epics_data)
    stories_df = pd.DataFrame(stories_data)
    tasks_df = pd.DataFrame(tasks_data)

    enriched_epics, enriched_stories, enriched_tasks = process_data(epics_df, stories_df, tasks_df)

    # Ensure that stories without a valid epic are assigned to the placeholder epic
    assert enriched_stories['epic_id'].iloc[0] == '0'

# 4. Тест на корректные данные

def test_valid_data():
    epics_data = {'id': [1, 2], 'subject': ['Epic 1', 'Epic 2']}
    stories_data = {'id': [101, 102], 'epics': [1, 2], 'subject': ['Story 1', 'Story 2']}
    tasks_data = {'id': [1001, 1002], 'user_story': [101, 102], 'subject': ['Task 1', 'Task 2']}

    epics_df = pd.DataFrame(epics_data)
    stories_df = pd.DataFrame(stories_data)
    tasks_df = pd.DataFrame(tasks_data)

    enriched_epics, enriched_stories, enriched_tasks = process_data(epics_df, stories_df, tasks_df)

    # Ensure that tasks are correctly enriched with story and epic data
    assert not enriched_tasks.empty
    assert 'story_subject' in enriched_tasks.columns
    assert 'epic_subject' in enriched_tasks.columns
    assert enriched_tasks.loc[0, 'epic_subject'] == 'Epic 1'
    assert enriched_tasks.loc[1, 'story_subject'] == 'Story 2'
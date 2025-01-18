import pytest
import pandas as pd
from app.data_processor import process_data

def test_process_data_valid():
    # Sample data
    epics_data = {'id': [1, 2], 'subject': ['Epic 1', 'Epic 2']}
    stories_data = {'id': [101, 102], 'epics': [1, 2], 'subject': ['Story 1', 'Story 2']}
    tasks_data = {'id': [1001, 1002], 'user_story': [101, 102], 'subject': ['Task 1', 'Task 2']}

    epics_df = pd.DataFrame(epics_data)
    stories_df = pd.DataFrame(stories_data)
    tasks_df = pd.DataFrame(tasks_data)

    enriched_epics, enriched_stories, enriched_tasks = process_data(epics_df, stories_df, tasks_df)

    # Verify tasks are enriched with story and epic details
    assert 'story_subject' in enriched_tasks.columns
    assert 'epic_subject' in enriched_tasks.columns
    assert enriched_tasks.loc[0, 'epic_subject'] == 'Epic 1'
    assert enriched_tasks.loc[1, 'story_subject'] == 'Story 2'

    # Verify stories are enriched with epic details
    assert 'epic_subject' in enriched_stories.columns
    assert enriched_stories.loc[0, 'epic_subject'] == 'Epic 1'

def test_process_data_missing_story_link():
    # Sample data with a task not linked to any story
    epics_data = {'id': [1], 'subject': ['Epic 1']}
    stories_data = {'id': [101], 'epics': [1], 'subject': ['Story 1']}
    tasks_data = {'id': [1001], 'user_story': [999], 'subject': ['Task 1']}

    epics_df = pd.DataFrame(epics_data)
    stories_df = pd.DataFrame(stories_data)
    tasks_df = pd.DataFrame(tasks_data)

    with pytest.raises(ValueError, match="Some tasks are not linked to a valid story."):
        process_data(epics_df, stories_df, tasks_df)

def test_process_data_missing_epic_link():
    # Sample data with a story not linked to any epic
    epics_data = {'id': [1], 'subject': ['Epic 1']}
    stories_data = {'id': [101], 'epics': [999], 'subject': ['Story 1']}
    tasks_data = {'id': [1001], 'user_story': [101], 'subject': ['Task 1']}

    epics_df = pd.DataFrame(epics_data)
    stories_df = pd.DataFrame(stories_data)
    tasks_df = pd.DataFrame(tasks_data)

    with pytest.raises(ValueError, match="Some stories are not linked to a valid epic."):
        process_data(epics_df, stories_df, tasks_df)

def test_process_data_missing_columns():
    # Missing required columns in epics
    epics_data = {'subject': ['Epic 1']}
    stories_data = {'id': [101], 'epics': [1], 'subject': ['Story 1']}
    tasks_data = {'id': [1001], 'user_story': [101], 'subject': ['Task 1']}

    epics_df = pd.DataFrame(epics_data)
    stories_df = pd.DataFrame(stories_data)
    tasks_df = pd.DataFrame(tasks_data)

    with pytest.raises(ValueError, match="Missing required columns in Epics data"):
        process_data(epics_df, stories_df, tasks_df)
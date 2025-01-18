import pandas as pd

def process_data(epics_df, stories_df, tasks_df):
    """
    Process and establish relationships between Epics, Stories, and Tasks.
    Tasks without a valid story and Stories without a valid epic are assigned to placeholder items.

    :param epics_df: DataFrame for epics
    :param stories_df: DataFrame for stories
    :param tasks_df: DataFrame for tasks
    :return: Tuple of enriched DataFrames (epics_df, stories_df, tasks_df)
    """
    # Ensure all necessary columns exist
    epic_required_cols = {'id', 'subject'}
    story_required_cols = {'id', 'epics', 'subject'}
    task_required_cols = {'id', 'user_story', 'subject'}

    if not epic_required_cols.issubset(epics_df.columns):
        raise ValueError(f"Missing required columns in Epics data: {epic_required_cols - set(epics_df.columns)}")

    if not story_required_cols.issubset(stories_df.columns):
        raise ValueError(f"Missing required columns in Stories data: {story_required_cols - set(stories_df.columns)}")

    if not task_required_cols.issubset(tasks_df.columns):
        raise ValueError(f"Missing required columns in Tasks data: {task_required_cols - set(tasks_df.columns)}")

    # Ensure columns are of the same type (convert to string)
    epics_df['id'] = epics_df['id'].astype(str)
    stories_df['epics'] = stories_df['epics'].astype(str)
    stories_df['id'] = stories_df['id'].astype(str)
    tasks_df['user_story'] = tasks_df['user_story'].astype(str)

    # Create placeholder epic and story if they don't exist
    placeholder_epic = pd.DataFrame({'id': ['0'], 'subject': ['Без эпика']})
    placeholder_story = pd.DataFrame({'id': ['0'], 'epics': ['0'], 'subject': ['Без истории']})

    # Ensure there's at least one epic and one story to link invalid ones to
    epics_df = pd.concat([epics_df, placeholder_epic], ignore_index=True)
    stories_df = pd.concat([stories_df, placeholder_story], ignore_index=True)

    # Merge Stories with Epics
    stories_df = stories_df.merge(
        epics_df[['id', 'subject']].rename(columns={'id': 'epic_id', 'subject': 'epic_subject'}),
        left_on='epics', right_on='epic_id', how='left'
    )

    # Merge Tasks with Stories
    tasks_df = tasks_df.merge(
        stories_df[['id', 'subject', 'epic_id', 'epic_subject']].rename(columns={
            'id': 'story_id', 'subject': 'story_subject'
        }),
        left_on='user_story', right_on='story_id', how='left'
    )

    # Replace tasks with missing stories and stories with missing epics with placeholders
    tasks_df['story_id'].fillna('0', inplace=True)
    tasks_df['story_subject'].fillna('Без истории', inplace=True)
    tasks_df['epic_subject'].fillna('Без эпика', inplace=True)
    stories_df['epic_id'].fillna('0', inplace=True)

    return epics_df, stories_df, tasks_df
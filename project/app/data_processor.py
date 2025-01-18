import pandas as pd

def process_data(epics_df, stories_df, tasks_df):
    """
    Process and establish relationships between Epics, Stories, and Tasks.

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

    # Add validation checks
    if tasks_df['story_id'].isnull().any():
        raise ValueError("Some tasks are not linked to a valid story.")

    if stories_df['epic_id'].isnull().any():
        raise ValueError("Some stories are not linked to a valid epic.")

    return epics_df, stories_df, tasks_df

# Example usage
if __name__ == "__main__":
    # Example data
    epics_data = {'id': [1, 2], 'subject': ['Epic 1', 'Epic 2']}
    stories_data = {'id': [101, 102], 'epics': [1, 2], 'subject': ['Story 1', 'Story 2']}
    tasks_data = {'id': [1001, 1002], 'user_story': [101, 102], 'subject': ['Task 1', 'Task 2']}

    epics_df = pd.DataFrame(epics_data)
    stories_df = pd.DataFrame(stories_data)
    tasks_df = pd.DataFrame(tasks_data)

    enriched_epics, enriched_stories, enriched_tasks = process_data(epics_df, stories_df, tasks_df)
    print(enriched_tasks)
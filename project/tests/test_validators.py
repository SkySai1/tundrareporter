import io
import pytest
from app.validators import validate_csv

def test_validate_csv_valid_epics():
    valid_csv = io.StringIO(
        "id,ref,subject,status,created_date,modified_date\n1,EPIC-1,Test Epic,Open,2023-01-01,2023-01-02"
    )
    expected_columns = [
        'id', 'ref', 'subject', 'description', 'owner', 'owner_full_name',
        'assigned_to', 'assigned_to_full_name', 'status', 'epics_order',
        'client_requirement', 'team_requirement', 'attachments', 'tags',
        'watchers', 'voters', 'created_date', 'modified_date', 'related_user_stories'
    ]
    required_columns = ['id', 'ref', 'subject', 'status', 'created_date', 'modified_date']

    valid, error = validate_csv(valid_csv, expected_columns, required_columns=required_columns)
    assert valid
    assert error is None

def test_validate_csv_missing_required_epics():
    invalid_csv = io.StringIO(
        "id,ref,subject,status,created_date,modified_date\n1,EPIC-1,Test Epic,Open,2023-01-01,"
    )
    expected_columns = [
        'id', 'ref', 'subject', 'description', 'owner', 'owner_full_name',
        'assigned_to', 'assigned_to_full_name', 'status', 'epics_order',
        'client_requirement', 'team_requirement', 'attachments', 'tags',
        'watchers', 'voters', 'created_date', 'modified_date', 'related_user_stories'
    ]
    required_columns = ['id', 'ref', 'subject', 'status', 'created_date', 'modified_date']

    valid, error = validate_csv(invalid_csv, expected_columns, required_columns=required_columns)
    assert not valid
    assert "Column 'modified_date' contains empty values." in error

def test_validate_csv_valid_stories():
    valid_csv = io.StringIO(
        "id,ref,subject,status,created_date,modified_date,total-points\n1,STORY-1,Test Story,Closed,2023-01-01,2023-01-02,5"
    )
    expected_columns = [
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
    required_columns = ['id', 'ref', 'subject', 'status', 'created_date', 'modified_date']

    valid, error = validate_csv(valid_csv, expected_columns, required_columns=required_columns)
    assert valid
    assert error is None

def test_validate_csv_missing_required_stories():
    invalid_csv = io.StringIO(
        "id,ref,subject,status,created_date,modified_date,total-points\n1,STORY-1,Test Story,Closed,2023-01-01,,5"
    )
    expected_columns = [
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
    required_columns = ['id', 'ref', 'subject', 'status', 'created_date', 'modified_date']

    valid, error = validate_csv(invalid_csv, expected_columns, required_columns=required_columns)
    assert not valid
    assert "Column 'modified_date' contains empty values." in error

def test_validate_csv_valid_tasks():
    valid_csv = io.StringIO(
        "id,ref,subject,status,created_date,modified_date\n1,TASK-1,Test Task,Open,2023-01-01,2023-01-02"
    )
    expected_columns = [
        'id', 'ref', 'subject', 'description', 'user_story', 'sprint_id', 'sprint',
        'sprint_estimated_start', 'sprint_estimated_finish', 'owner', 'owner_full_name',
        'assigned_to', 'assigned_to_full_name', 'status', 'is_iocaine', 'is_closed',
        'us_order', 'taskboard_order', 'attachments', 'external_reference', 'tags',
        'watchers', 'voters', 'created_date', 'modified_date', 'finished_date',
        'due_date', 'due_date_reason'
    ]
    required_columns = ['id', 'ref', 'subject', 'status', 'created_date', 'modified_date']

    valid, error = validate_csv(valid_csv, expected_columns, required_columns=required_columns)
    assert valid
    assert error is None

def test_validate_csv_missing_required_tasks():
    invalid_csv = io.StringIO(
        "id,ref,subject,status,created_date,modified_date\n1,TASK-1,Test Task,Open,2023-01-01,"
    )
    expected_columns = [
        'id', 'ref', 'subject', 'description', 'user_story', 'sprint_id', 'sprint',
        'sprint_estimated_start', 'sprint_estimated_finish', 'owner', 'owner_full_name',
        'assigned_to', 'assigned_to_full_name', 'status', 'is_iocaine', 'is_closed',
        'us_order', 'taskboard_order', 'attachments', 'external_reference', 'tags',
        'watchers', 'voters', 'created_date', 'modified_date', 'finished_date',
        'due_date', 'due_date_reason'
    ]
    required_columns = ['id', 'ref', 'subject', 'status', 'created_date', 'modified_date']

    valid, error = validate_csv(invalid_csv, expected_columns, required_columns=required_columns)
    assert not valid
    assert "Column 'modified_date' contains empty values." in error
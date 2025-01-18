import pandas as pd

def validate_csv(file, expected_columns, sep=',', required_columns=None, optional_columns=None):
    """
    Validate the structure and content of a CSV file.

    :param file: File-like object (e.g., from Flask request.files)
    :param expected_columns: List of expected column names
    :param sep: CSV separator (default: ',')
    :param required_columns: List of columns that must not contain empty values
    :param optional_columns: List of columns that can have empty values or be missing
    :return: Tuple (is_valid: bool, error_message: str or None)
    """
    try:
        # Load the CSV file with the provided separator
        df = pd.read_csv(file, sep=sep)

        # Check for missing columns in required_columns
        missing_required = [col for col in required_columns if col not in df.columns]
        if missing_required:
            return False, f"Missing required columns: {', '.join(missing_required)}"

        # Check for empty values in required columns
        for col in required_columns:
            if col in df.columns and df[col].isnull().any():
                return False, f"Column '{col}' contains empty values."

        # Optional columns are allowed to be missing, no validation needed here.

        # Validate specific rules (e.g., numeric, dates)
        if 'created_date' in df.columns:
            try:
                pd.to_datetime(df['created_date'])
            except ValueError:
                return False, "Column 'created_date' contains invalid dates."

        if 'modified_date' in df.columns:
            try:
                pd.to_datetime(df['modified_date'])
            except ValueError:
                return False, "Column 'modified_date' contains invalid dates."

        return True, None

    except pd.errors.ParserError as e:
        return False, f"CSV parsing error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
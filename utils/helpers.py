"""
Helper Functions
Common utility functions used throughout the application
"""

from datetime import datetime


def validate_date(date_string):
    """
    Validate that a string is a valid date in YYYY-MM-DD format.
    
    Args:
        date_string (str): Date string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def format_date(date_string):
    """
    Format a date string for display.
    
    Args:
        date_string (str): Date in YYYY-MM-DD format
        
    Returns:
        str: Formatted date string
    """
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')  # e.g., "January 15, 2024"
    except ValueError:
        return date_string


def print_separator(char='-', length=60):
    """
    Print a separator line.
    
    Args:
        char (str): Character to use for separator
        length (int): Length of separator
    """
    print(char * length)


def print_header(text):
    """
    Print a formatted header.
    
    Args:
        text (str): Header text
    """
    print_separator('=')
    print(f"  {text}")
    print_separator('=')


def confirm_action(prompt):
    """
    Ask user to confirm an action.
    
    Args:
        prompt (str): Question to ask the user
        
    Returns:
        bool: True if user confirms, False otherwise
    """
    response = input(f"{prompt} (y/n): ").lower().strip()
    return response in ['y', 'yes']


def get_input(prompt, required=True):
    """
    Get input from user with optional validation.
    
    Args:
        prompt (str): Prompt to display
        required (bool): Whether input is required
        
    Returns:
        str: User input, or None if not required and empty
    """
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value if value else None
        print("This field is required. Please enter a value.")


def display_list(items, title=None, empty_message="No items to display"):
    """
    Display a list of items.
    
    Args:
        items (list): List of items to display
        title (str): Optional title for the list
        empty_message (str): Message to show if list is empty
    """
    if title:
        print_header(title)
    
    if not items:
        print(f"\n{empty_message}\n")
        return
    
    for item in items:
        print(item)
    print()  # Empty line after list


def truncate_text(text, max_length=50):
    """
    Truncate text to a maximum length.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

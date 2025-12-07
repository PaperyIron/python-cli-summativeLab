"""
Data Persistence Utilities
Handles saving and loading data to/from JSON files
"""

import json
import os
from models import User, Project, Task


class DataManager:
    """
    Manages saving and loading data to/from JSON files.
    """
    
    def __init__(self, data_dir='data'):
        """
        Initialize the DataManager.
        
        Args:
            data_dir (str): Directory where data files are stored
        """
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, 'users.json')
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def save_users(self, users):
        """
        Save a list of users to JSON file.
        
        Args:
            users (list): List of User objects
        """
        try:
            # Convert users to dictionaries
            users_data = [user.to_dict() for user in users]
            
            # Write to file with nice formatting
            with open(self.users_file, 'w') as f:
                json.dump(users_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    def load_users(self):
        """
        Load users from JSON file.
        
        Returns:
            list: List of User objects, or empty list if file doesn't exist
        """
        # If file doesn't exist, return empty list
        if not os.path.exists(self.users_file):
            return []
        
        try:
            # Read from file
            with open(self.users_file, 'r') as f:
                users_data = json.load(f)
            
            # Convert dictionaries to User objects
            users = [User.from_dict(data) for data in users_data]
            return users
            
        except json.JSONDecodeError:
            print(f"Error: {self.users_file} contains invalid JSON")
            return []
        except Exception as e:
            print(f"Error loading users: {e}")
            return []
    
    def find_user_by_email(self, users, email):
        """
        Find a user by email address.
        
        Args:
            users (list): List of User objects
            email (str): Email to search for
            
        Returns:
            User or None: The user if found, None otherwise
        """
        for user in users:
            if user.email == email:
                return user
        return None
    
    def find_user_by_id(self, users, user_id):
        """
        Find a user by ID.
        
        Args:
            users (list): List of User objects
            user_id (int): ID to search for
            
        Returns:
            User or None: The user if found, None otherwise
        """
        for user in users:
            if user.user_id == user_id:
                return user
        return None
    
    def backup_data(self):
        """
        Create a backup of the current data file.
        
        Returns:
            bool: True if backup successful, False otherwise
        """
        if not os.path.exists(self.users_file):
            print("No data file to backup")
            return False
        
        try:
            backup_file = self.users_file + '.backup'
            with open(self.users_file, 'r') as source:
                with open(backup_file, 'w') as backup:
                    backup.write(source.read())
            print(f"Backup created: {backup_file}")
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

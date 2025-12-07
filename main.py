#!/usr/bin/env python3
import argparse
import sys
from models import User, Project, Task
from utils.data_manager import DataManager
from utils.helpers import (
    print_header, print_separator, confirm_action, 
    get_input, display_list, format_date, validate_date
)


class ProjectManagerCLI:
    def __init__(self):
        self.data_manager = DataManager()
        self.users = self.data_manager.load_users()
    
    def save_data(self):
        self.data_manager.save_users(self.users)
    
    def add_user(self, args):
        # Check if user with this email already exists
        if self.data_manager.find_user_by_email(self.users, args.email):
            print(f"Error: A user with email {args.email} already exists!")
            return
        
        try:
            # Create new user
            user = User(name=args.name, email=args.email)
            self.users.append(user)
            self.save_data()
            
            print(f"\n✓ User created successfully!")
            print(user)
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def list_users(self, args):
        display_list(self.users, title="All Users", empty_message="No users found")
    
    def delete_user(self, args):
        user = self.data_manager.find_user_by_email(self.users, args.email)
        
        if not user:
            print(f"Error: User with email {args.email} not found!")
            return
        
        # Confirm deletion
        if not confirm_action(f"Delete user {user.name} and all their projects?"):
            print("Cancelled.")
            return
        
        self.users.remove(user)
        self.save_data()
        print(f"✓ User {user.name} deleted successfully!")
    
    #Project Commands
    def add_project(self, args):
        # Find the user
        user = self.data_manager.find_user_by_email(self.users, args.email)
        if not user:
            print(f"Error: User with email {args.email} not found!")
            return
        
        # Validate date
        if not validate_date(args.due_date):
            print("Error: Date must be in YYYY-MM-DD format (e.g., 2024-12-31)")
            return
        
        try:
            # Create new project
            project = Project(
                title=args.title,
                description=args.description,
                due_date=args.due_date,
                owner_email=user.email
            )
            user.add_project(project)
            self.save_data()
            
            print(f"\n✓ Project created successfully for {user.name}!")
            print(project)
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def list_projects(self, args):
        user = self.data_manager.find_user_by_email(self.users, args.email)
        if not user:
            print(f"Error: User with email {args.email} not found!")
            return
        
        display_list(
            user.projects, 
            title=f"Projects for {user.name}",
            empty_message="No projects found"
        )
    
    def delete_project(self, args):
        user = self.data_manager.find_user_by_email(self.users, args.email)
        if not user:
            print(f"Error: User with email {args.email} not found!")
            return
        
        project = user.get_project(args.project_id)
        if not project:
            print(f"Error: Project with ID {args.project_id} not found!")
            return
        
        # Confirm deletion
        if not confirm_action(f"Delete project '{project.title}'?"):
            print("Cancelled.")
            return
        
        user.remove_project(args.project_id)
        self.save_data()
        print(f"✓ Project '{project.title}' deleted successfully!")
    
#Task Commands
    
    def add_task(self, args):
        # Find the user and project
        user = self.data_manager.find_user_by_email(self.users, args.email)
        if not user:
            print(f"Error: User with email {args.email} not found!")
            return
        
        project = user.get_project(args.project_id)
        if not project:
            print(f"Error: Project with ID {args.project_id} not found!")
            return
        
        # Validate assigned_to email if provided
        if args.assigned_to:
            assignee = self.data_manager.find_user_by_email(self.users, args.assigned_to)
            if not assignee:
                print(f"Warning: User {args.assigned_to} not found, but task will be created anyway.")
        
        try:
            # Create new task
            task = Task(
                title=args.title,
                assigned_to=args.assigned_to
            )
            project.add_task(task)
            self.save_data()
            
            print(f"\n✓ Task added to project '{project.title}'!")
            print(task)
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def list_tasks(self, args):
        # Find the user and project
        user = self.data_manager.find_user_by_email(self.users, args.email)
        if not user:
            print(f"Error: User with email {args.email} not found!")
            return
        
        project = user.get_project(args.project_id)
        if not project:
            print(f"Error: Project with ID {args.project_id} not found!")
            return
        
        # Filter by status if provided
        if args.status:
            tasks = project.get_tasks_by_status(args.status)
            title = f"Tasks in '{project.title}' with status '{args.status}'"
        else:
            tasks = project.tasks
            title = f"All Tasks in '{project.title}'"
        
        display_list(tasks, title=title, empty_message="No tasks found")
    
    def complete_task(self, args):
        # Find the user and project
        user = self.data_manager.find_user_by_email(self.users, args.email)
        if not user:
            print(f"Error: User with email {args.email} not found!")
            return
        
        project = user.get_project(args.project_id)
        if not project:
            print(f"Error: Project with ID {args.project_id} not found!")
            return
        
        task = project.get_task(args.task_id)
        if not task:
            print(f"Error: Task with ID {args.task_id} not found!")
            return
        
        # Mark as completed
        task.complete()
        self.save_data()
        print(f"✓ Task '{task.title}' marked as completed!")
    
    def update_task_status(self, args):
        # Find the user and project
        user = self.data_manager.find_user_by_email(self.users, args.email)
        if not user:
            print(f"Error: User with email {args.email} not found!")
            return
        
        project = user.get_project(args.project_id)
        if not project:
            print(f"Error: Project with ID {args.project_id} not found!")
            return
        
        task = project.get_task(args.task_id)
        if not task:
            print(f"Error: Task with ID {args.task_id} not found!")
            return
        
        try:
            task.status = args.status
            self.save_data()
            print(f"✓ Task '{task.title}' status updated to '{args.status}'!")
        except ValueError as e:
            print(f"Error: {e}")


def main():
    # Create the CLI application instance
    cli = ProjectManagerCLI()
    
    # Create main parser
    parser = argparse.ArgumentParser(
        description='Project Manager CLI - Manage users, projects, and tasks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a user
  python main.py add-user "John Doe" john@example.com
  
  # Add a project
  python main.py add-project john@example.com "Website Redesign" "Redesign company website" 2024-12-31
  
  # Add a task
  python main.py add-task john@example.com 1 "Create homepage mockup" --assigned-to jane@example.com
  
  # Complete a task
  python main.py complete-task john@example.com 1 1
        """
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # add-user command
    parser_add_user = subparsers.add_parser('add-user', help='Add a new user')
    parser_add_user.add_argument('name', help='User full name')
    parser_add_user.add_argument('email', help='User email address')
    
    # list-users command
    parser_list_users = subparsers.add_parser('list-users', help='List all users')
    
    # delete-user command
    parser_delete_user = subparsers.add_parser('delete-user', help='Delete a user')
    parser_delete_user.add_argument('email', help='Email of user to delete')
    
    # ==================== PROJECT COMMANDS ====================
    
    # add-project command
    parser_add_project = subparsers.add_parser('add-project', help='Add a new project')
    parser_add_project.add_argument('email', help='Owner email address')
    parser_add_project.add_argument('title', help='Project title')
    parser_add_project.add_argument('description', help='Project description')
    parser_add_project.add_argument('due_date', help='Due date (YYYY-MM-DD)')
    
    # list-projects command
    parser_list_projects = subparsers.add_parser('list-projects', help='List projects for a user')
    parser_list_projects.add_argument('email', help='User email address')
    
    # delete-project command
    parser_delete_project = subparsers.add_parser('delete-project', help='Delete a project')
    parser_delete_project.add_argument('email', help='Owner email address')
    parser_delete_project.add_argument('project_id', type=int, help='Project ID to delete')
    
    
    # add-task command
    parser_add_task = subparsers.add_parser('add-task', help='Add a new task')
    parser_add_task.add_argument('email', help='Project owner email')
    parser_add_task.add_argument('project_id', type=int, help='Project ID')
    parser_add_task.add_argument('title', help='Task title')
    parser_add_task.add_argument('--assigned-to', help='Email of assigned user')
    
    # list-tasks command
    parser_list_tasks = subparsers.add_parser('list-tasks', help='List tasks in a project')
    parser_list_tasks.add_argument('email', help='Project owner email')
    parser_list_tasks.add_argument('project_id', type=int, help='Project ID')
    parser_list_tasks.add_argument('--status', choices=['pending', 'in_progress', 'completed'],
                                   help='Filter by status')
    
    # complete-task command
    parser_complete_task = subparsers.add_parser('complete-task', help='Mark task as completed')
    parser_complete_task.add_argument('email', help='Project owner email')
    parser_complete_task.add_argument('project_id', type=int, help='Project ID')
    parser_complete_task.add_argument('task_id', type=int, help='Task ID')
    
    # update-task-status command
    parser_update_status = subparsers.add_parser('update-task-status', help='Update task status')
    parser_update_status.add_argument('email', help='Project owner email')
    parser_update_status.add_argument('project_id', type=int, help='Project ID')
    parser_update_status.add_argument('task_id', type=int, help='Task ID')
    parser_update_status.add_argument('status', choices=['pending', 'in_progress', 'completed'],
                                     help='New status')
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command provided, show help
    if not args.command:
        parser.print_help()
        return
    
    # Execute the appropriate command
    command_map = {
        'add-user': cli.add_user,
        'list-users': cli.list_users,
        'delete-user': cli.delete_user,
        'add-project': cli.add_project,
        'list-projects': cli.list_projects,
        'delete-project': cli.delete_project,
        'add-task': cli.add_task,
        'list-tasks': cli.list_tasks,
        'complete-task': cli.complete_task,
        'update-task-status': cli.update_task_status,
    }
    
    # Run the command
    if args.command in command_map:
        command_map[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

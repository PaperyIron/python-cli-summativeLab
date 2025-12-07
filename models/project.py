from datetime import datetime
from models.task import Task


class Project:
    # keeps track of the next ID to assign
    _next_id = 1
    
    def __init__(self, title, description, due_date, owner_email, project_id=None):
        # Use provided ID or auto-generate
        if project_id is None:
            self._project_id = Project._next_id
            Project._next_id += 1
        else:
            self._project_id = project_id
            # Update the class counter if needed
            if project_id >= Project._next_id:
                Project._next_id = project_id + 1
        
        self._title = title
        self._description = description
        self._due_date = due_date
        self._owner_email = owner_email
        self._tasks = []  
    
    @property
    def project_id(self):
        return self._project_id
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Project title cannot be empty")
        self._title = value.strip()
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        self._description = value
    
    @property
    def due_date(self):
        return self._due_date
    
    @due_date.setter
    def due_date(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            self._due_date = value
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format")
    
    @property
    def owner_email(self):
        return self._owner_email
    
    @property
    def tasks(self):
        return self._tasks
    
    def add_task(self, task):
        if not isinstance(task, Task):
            raise TypeError("Can only add Task objects")
        self._tasks.append(task)
    
    def remove_task(self, task_id):
        for i, task in enumerate(self._tasks):
            if task.task_id == task_id:
                self._tasks.pop(i)
                return True
        return False
    
    def get_task(self, task_id):
        for task in self._tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def get_tasks_by_status(self, status):
        return [task for task in self._tasks if task.status == status]
    
    def to_dict(self):
        return {
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'owner_email': self.owner_email,
            'tasks': [task.to_dict() for task in self.tasks]
        }
    
    @classmethod
    def from_dict(cls, data):
        project = cls(
            title=data['title'],
            description=data['description'],
            due_date=data['due_date'],
            owner_email=data['owner_email'],
            project_id=data['project_id']
        )
        
        # Add tasks
        for task_data in data.get('tasks', []):
            task = Task.from_dict(task_data)
            project.add_task(task)
        
        return project
    
    def __str__(self):
        task_count = len(self.tasks)
        completed = len(self.get_tasks_by_status('completed'))
        return (f"[{self.project_id}] {self.title}\n"
                f"    Description: {self.description}\n"
                f"    Due: {self.due_date}\n"
                f"    Tasks: {completed}/{task_count} completed")
    
    def __repr__(self):
        return f"Project(id={self.project_id}, title='{self.title}', tasks={len(self.tasks)})"

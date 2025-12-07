import re
from models.project import Project


class User:
    # keeps track of the next ID to assign
    _next_id = 1
    
    def __init__(self, name, email, user_id=None):
        # Use provided ID or auto-generate
        if user_id is None:
            self._user_id = User._next_id
            User._next_id += 1
        else:
            self._user_id = user_id
            # Update the class counter if needed
            if user_id >= User._next_id:
                User._next_id = user_id + 1
        
        self._name = name
        self._email = email
        self._projects = []  
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
        self._email = value
    
    @property
    def projects(self):
        return self._projects
    
    def add_project(self, project):
        if not isinstance(project, Project):
            raise TypeError("Can only add Project objects")
        self._projects.append(project)
    
    def remove_project(self, project_id):
        for i, project in enumerate(self._projects):
            if project.project_id == project_id:
                self._projects.pop(i)
                return True
        return False
    
    def get_project(self, project_id):
        for project in self._projects:
            if project.project_id == project_id:
                return project
        return None
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'projects': [project.to_dict() for project in self.projects]
        }
    
    @classmethod
    def from_dict(cls, data):
        user = cls(
            name=data['name'],
            email=data['email'],
            user_id=data['user_id']
        )
        
        # Add projects
        for project_data in data.get('projects', []):
            project = Project.from_dict(project_data)
            user.add_project(project)
        
        return user
    
    def __str__(self):
        project_count = len(self.projects)
        return f"[{self.user_id}] {self.name} ({self.email}) - {project_count} project(s)"
    
    def __repr__(self):
        return f"User(id={self.user_id}, name='{self.name}', email='{self.email}')"

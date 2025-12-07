class Task:
# keeps track of the next ID to assign
    _next_id = 1
    
    def __init__(self, title, status="pending", assigned_to=None, task_id=None):
        # Use provided ID or auto-generate
        if task_id is None:
            self._task_id = Task._next_id
            Task._next_id += 1
        else:
            self._task_id = task_id
            # Update the class counter if needed
            if task_id >= Task._next_id:
                Task._next_id = task_id + 1
        
        self._title = title
        self._status = status
        self._assigned_to = assigned_to
    
    @property
    def task_id(self):
        return self._task_id
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Task title cannot be empty")
        self._title = value.strip()
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        valid_statuses = ['pending', 'in_progress', 'completed']
        if value not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        self._status = value
    
    @property
    def assigned_to(self):
        return self._assigned_to
    
    @assigned_to.setter
    def assigned_to(self, value):
        self._assigned_to = value
    
    def complete(self):
        self.status = 'completed'
    
    def to_dict(self):
        return {
            'task_id': self.task_id,
            'title': self.title,
            'status': self.status,
            'assigned_to': self.assigned_to
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data['title'],
            status=data['status'],
            assigned_to=data.get('assigned_to'),
            task_id=data['task_id']
        )
    
    def __str__(self):
        assigned = self.assigned_to if self.assigned_to else "Unassigned"
        return f"[{self.task_id}] {self.title} - {self.status} (Assigned to: {assigned})"
    
    def __repr__(self):
        return f"Task(id={self.task_id}, title='{self.title}', status='{self.status}')"

from app import mongo

class Project:
    def __init__(self, name, goal, deadline, team_members, milestones):
        self.name = name
        self.goal = goal
        self.deadline = deadline
        self.team_members = team_members
        self.milestones = milestones
    
    def save(self):
        return mongo.db.projects.insert_one({
            'name': self.name,
            'goal': self.goal,
            'deadline': self.deadline,
            'team_members': self.team_members,
            'milestones': self.milestones
        })

class Task:
    def __init__(self, project_id, description, assigned_to, due_date, dependencies=None):
        self.project_id = project_id
        self.description = description
        self.assigned_to = assigned_to
        self.due_date = due_date
        self.dependencies = dependencies or []
    
    def save(self):
        return mongo.db.tasks.insert_one({
            'project_id': self.project_id,
            'description': self.description,
            'assigned_to': self.assigned_to,
            'due_date': self.due_date,
            'dependencies': self.dependencies
        })

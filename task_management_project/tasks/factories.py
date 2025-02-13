from .models import Task

def task_factory(title, description="", is_completed=False, category=None):
    return Task(title=title, description=description, is_completed=is_completed, category=category)



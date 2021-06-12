from datetime import datetime

from RHU.models import Action

def log(type, description, user):
    action = Action(
        type=type,
        timePerformed=datetime.now(),
        description=description, 
        user=user,
    )
    action.save()
from src.models import Team

def create_team(driver1, driver2, car, principal, team_name="YOUR DRAFT TEAM"):
    return Team(driver1=driver1, driver2=driver2, car=car, principal=principal, name=team_name)
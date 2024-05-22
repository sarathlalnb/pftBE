from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator



class CustomUser(AbstractUser):
    user_type_choices=[
        ("hr","hr"),
        ("employee","employee"),
        ("teamlead","teamlead"),
    ]
    user_type=models.CharField(max_length=50,choices=user_type_choices,default="admin")
    
class Hr(CustomUser):
    name=models.CharField(max_length=200)
    email_address=models.CharField(max_length=100)
    phoneno=models.PositiveIntegerField()
    is_adminapproved=models.BooleanField(default=False)
  

class TeamLead(CustomUser):
    name=models.CharField(max_length=200)
    email_address=models.CharField(max_length=100)
    phoneno=models.PositiveIntegerField()  
    is_adminapproved=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
   
    
class Employee(CustomUser):
    Firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=200)
    email_address=models.EmailField(unique=True)
    phoneno=models.PositiveIntegerField()
    position=models.CharField(max_length=200)
    in_team=models.BooleanField(default=False)
    is_adminapproved=models.BooleanField(default=False)


    def __str__(self):
        return self.Firstname
    
class Teams(models.Model):
    name=models.CharField(max_length=100)
    teamlead=models.OneToOneField(TeamLead,on_delete=models.CASCADE,unique=True) 
    members=models.ManyToManyField(Employee)
    is_approved=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    
class Projects(models.Model):
    topic=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    end_date=models.DateField()
    options=[
        ("pending","pending"),
        ("Ongoing","Ongoing"),
        ("completed","completed")
    ]
    project_status=models.CharField(max_length=50,choices=options,default="pending")
    
    def __str__(self):
        return self.topic
    
    
class ProjectUpdates(models.Model):
    project=models.ForeignKey(Projects,on_delete=models.CASCADE)
    description=models.CharField(max_length=200)


class Project_assign(models.Model):
    project=models.OneToOneField(Projects,on_delete=models.CASCADE,unique=True)
    teamlead=models.ForeignKey(TeamLead,on_delete=models.CASCADE)
    team=models.ForeignKey(Teams,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.project.topic 
    


class ProjectDetail(models.Model):
    teamlead=models.ForeignKey(TeamLead,on_delete=models.CASCADE)    
    projectassigned=models.ForeignKey(Project_assign,on_delete=models.CASCADE)  
    assigned_part=models.CharField(max_length=100)
    assigned_person=models.OneToOneField(Employee,on_delete=models.CASCADE)
    options=[
        ("In progress","In progress"),
        ("completed","completed")
    ]
    status=models.CharField(max_length=50,choices=options,default="In progress")
    
    def __str__(self):
        return self.projectassigned.project.topic
    

class TaskChart(models.Model):
    project_detail=models.ForeignKey(ProjectDetail,on_delete=models.CASCADE) 
    assigned_person=models.OneToOneField(Employee,on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    total_days=models.IntegerField()
    
    
class TaskUpdateChart(models.Model):
    task = models.ForeignKey(TaskChart, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    updated_by=models.ForeignKey(Employee, on_delete=models.CASCADE)
    description=models.CharField(max_length=100)
    performance_level=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(3)])
    date_updated=models.DateTimeField(auto_now_add=True) 
    
    
class Performance_assign(models.Model):
    hr=models.ForeignKey(Hr,on_delete=models.CASCADE)
    employee=models.OneToOneField(Employee,on_delete=models.CASCADE,unique=True)
    performance=models.FloatField()

    
    
class Meeting(models.Model):
    organizer=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    link=models.CharField(max_length=100,null=True)
    date=models.DateField(null=True)
    time=models.TimeField(null=True)
    posted_at=models.DateTimeField(auto_now_add=True)

    
class DailyTask(models.Model):
    teamlead=models.ForeignKey(TeamLead,on_delete=models.CASCADE)    
    task=models.CharField(max_length=100)
    emp=models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_completed=models.BooleanField(default=False)
    
class Rating(models.Model):
    teamlead=models.ForeignKey(TeamLead,on_delete=models.CASCADE)    
    emp=models.ForeignKey(Employee, on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=100)

   
class TechnologiesList(models.Model):
    no=models.PositiveIntegerField()
    data=models.CharField(max_length=100)



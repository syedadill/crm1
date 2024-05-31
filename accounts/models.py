from django.db import models

# Create your models here.


    
class Projects(models.Model):
    ProjectName = models.CharField(max_length=200, null=True)
    ProjectType = models.CharField(max_length=200, null=True)
    DueDate = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.ProjectName

class Tags(models.Model):
    Technology = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.Technology 

class Tasks (models.Model):
    TASKTYPE = (
        ('Design', 'Desgin'),
        ('Testing', 'Testing'),
        ('Development', 'Development'),
        ('Deployement', 'Deployement'),
    )
    TASKASSIGN = (
        ('Hamza', 'Hamza'),
        ('Adil', 'Adil'),
        ('Usama', 'Usama'),

    )
    Board =  (
            ('ToDo', 'ToDO'),
            ('In Progress', 'In Progress'),
            ('Testing', 'Testing'),
            ('Bug', 'Bug'),  
            ('Completed', 'Completed'),
    )
    TaskName = models.CharField(max_length=200, null= True)
    TaskDescription = models.CharField(max_length=1500, null=True)
    TaskType = models.CharField(max_length = 200, null= True, choices=TASKTYPE)
    TaskAssignTo = models.CharField(max_length = 200, null = True,choices = TASKASSIGN )
    SelectStatus = models.CharField(max_length = 200, null = True,choices = Board)
    DueDate = models.DateTimeField(null=True)
    Date=models.DateField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tags)
    project = models.ForeignKey(Projects, null=True, on_delete=models.SET_NULL )
    

    def __str__(self):
        return self.TaskName
    
class Status (models.Model):
    STATUS =  (
            ('Open', 'Open'),
            ('In Progress', 'In Progress'),
            ('Pending', 'Pending'),
            ('Testing', 'Testing'),
            ('Bug', 'Bug'),  
    )
    project = models.ForeignKey(Projects, null=True, on_delete=models.SET_NULL )
    task = models.ForeignKey(Tasks, null=True, on_delete=models.SET_NULL )
    CurrentDate =models.DateTimeField( auto_now_add=True, null= True)
    Due_Date = models.DateField(null=True)
    Status = models.CharField(max_length=50, null = True, choices= STATUS)
   
    def __str__(self):
        return self.Status 





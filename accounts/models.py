from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  # Use RichTextField
from ckeditor_uploader.fields import RichTextUploadingField 

# Create your models here.

class Customers(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    EmployeeName = models.CharField(max_length=200, null=True,)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="icon1", null=True, blank = True)
    
    def __str__(self):
        return self.EmployeeName if self.EmployeeName else 'No Title'
    
class Projects(models.Model):
    
    ProjectName = models.CharField(max_length=200, null=True)
    ProjectType = models.CharField(max_length=200, null=True)
    DueDate = models.DateTimeField(null=True)
    Assign = models.ManyToManyField(Customers, null=True)
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
    TaskDescription = RichTextUploadingField(null=True)
    TaskType = models.CharField(max_length = 200, null= True, choices=TASKTYPE)
    SelectStatus = models.CharField(default='ToDo', max_length = 200, null = True,choices = Board)
    DueDate = models.DateField(null=True)
    Date=models.DateField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tags)
    project = models.ForeignKey(Projects, null=True, on_delete=models.SET_NULL) 
    employe = models.ForeignKey(Customers, null=True, on_delete=models.SET_NULL)
    files = models.FileField(upload_to='files/', null = True, blank=True)
    Image = models.ImageField(upload_to='images/',null = True, blank=True)
    Comments = models.CharField(default= '0',  max_length=200, null=True)
    ImageURL= models.URLField(null=True)
    def __str__(self):
        return self.TaskName
    
class Status (models.Model):
    STATUS =  (
            ('ToDo', 'ToDo'),
            ('In Progress', 'In Progress'),
            ('Pending', 'Pending'),
            ('Testing', 'Testing'),
            ('Bug', 'Bug'),  
    )
    Assign = models.ForeignKey(Customers, null=True, on_delete=models.SET_NULL )
    Status = models.CharField(max_length=50, null = True, choices= STATUS)
   
    def __str__(self):
        return self.Status 

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Article(models.Model):
    title = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    datePosted = models.CharField(max_length=20, default="")
    timePosted = models.CharField(max_length=20, default="")
    category = models.CharField(max_length=300)
    content = RichTextField(null=True, blank=True)
    contentImage = models.ImageField(upload_to='images/')

class Comment(models.Model):
    text = models.CharField(max_length=200, null=True)
    

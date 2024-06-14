from django.forms import ModelForm
from django import forms
from .models import Tasks, Projects, Customers, Status, Article, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField, RichTextFormField, forms
from ckeditor.widgets import CKEditorWidget
class EmployeeForm(ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'
        exclude = ['user']
        
   
class TaskForm(ModelForm):
    class Meta:
        model = Tasks
        fields = '__all__'
        exclude = ["ImageURL"]
        widget = {
            'content': CKEditorWidget(),
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if project:
            self.fields['project'].initial = project
            self.fields['project'].widget.attrs['readonly'] = True
        
        self.fields.pop('project')
    
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = '__all__'

class CHangeStatus(ModelForm):
    class Meta:
        model = Tasks
        fields = ['SelectStatus','employe','Comments']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'contentImage']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}),
            'category': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Category'}),            
            'content' : RichTextFormField(config_name="default"),        
            'contentImage': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Image'})
        }
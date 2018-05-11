from django.contrib.auth.models import User,Group
from .models import Video,Subject
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'contatct-form'}))
    groups = forms.ModelChoiceField(queryset=Group.objects.all(),required=True,initial=0)

    class Meta:
        model = User
        fields = ['groups','username','email','password',]

class SubjForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name',]

class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password',]

class DocumentForm(forms.ModelForm):
    faculty = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='faculty'),required=True)
    class Meta:
        model = Video
        fields = ('video_title', 'file_file','faculty','subject')

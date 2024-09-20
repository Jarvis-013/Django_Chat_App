from django import forms
from django.contrib.auth.models import User
from .models import ChatGroup

class GroupCreationForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = ChatGroup
        fields = ['name', 'members']

    def __init__(self, *args, **kwargs):
        super(GroupCreationForm, self).__init__(*args, **kwargs)
        self.fields['members'].label = "Select Group Members"

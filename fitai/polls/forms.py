from django import forms
from .models import FitnessData

class FitnessDataForm(forms.ModelForm):
    class Meta:
        model = FitnessData
        fields = ['age', 'weight', 'height', 'goal', 'gender', 'fitness_level']

from django.db import models
from django.contrib.auth.models import User

class WorkoutRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    routine = models.TextField()
     
    def __str__(self):
        return self.routine

class FitnessData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=25)
    weight = models.FloatField(default=145)
    height = models.FloatField(default=60)
    goal = models.CharField(max_length=200, default="Lose weight")
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default="Male")
    fitness_level = models.CharField(max_length=50, default='active')
    workout_routine = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Fitness Data"
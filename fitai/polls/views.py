from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import WorkoutRoutine
from .chatgpt_wrapper import generate_workout_routine
from django.contrib.auth.decorators import login_required
from .forms import FitnessDataForm
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FitnessData
from .forms import FitnessDataForm



from django.http import HttpResponse

def home(request):
    if request.user.is_authenticated:
        fitness_data = FitnessData.objects.filter(user=request.user).first()
        workout_routine = WorkoutRoutine.objects.filter(user=request.user).first()
        context = {
            'fitness_data': fitness_data,
            'workout_routine': workout_routine,
        }
    else:
        context = {}
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Specify the backend while logging in the user
            backend = ModelBackend()
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def fitness_data(request):
    if request.method == 'POST':
        form = FitnessDataForm(request.POST)
        if form.is_valid():
            # Check if the user already has fitness data
            existing_fitness_data = FitnessData.objects.filter(user=request.user).first()

            # If the user has fitness data, update it
            if existing_fitness_data:
                form = FitnessDataForm(request.POST, instance=existing_fitness_data)
                form.save()
            # If the user doesn't have fitness data, create a new record
            else:
                fitness_data = form.save(commit=False)
                fitness_data.user = request.user
                fitness_data.save()

            return redirect('workout_routine')
    else:
        form = FitnessDataForm()
    return render(request, 'fitness_data.html', {'form': form})

@login_required
def workout_routine(request):
    # Check if the user already has a workout routine
    existing_workout_routine = WorkoutRoutine.objects.filter(user=request.user).first()

    # If the user has a workout routine, display it
    if existing_workout_routine:
        context = {
            'response': existing_workout_routine.routine,
        }

    # If the user doesn't have a workout routine, call the API and save it to the database
    else:
        fitness_data = FitnessData.objects.filter(user=request.user).first()

        if fitness_data:
            user_message = f"Create a workout routine for a {fitness_data.age}-year-old {fitness_data.gender} with fitness level {fitness_data.fitness_level}."
            messages = [
                {"role": "user", "content": user_message},
            ]

            response = generate_workout_routine(messages)

            # Save the generated workout routine
            workout_routine = WorkoutRoutine(user=request.user, routine=response)
            workout_routine.save()

            context = {
                'response': response,
            }
        else:
            context = {
                'response': "Please provide your fitness data to generate a workout routine.",
            }

    return render(request, 'polls/get_workout_routine.html', context)

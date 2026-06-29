from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Avg

from .forms import RegisterForm, FeedbackForm
from .models import Feedback

def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            profile = user.profile
            profile.role = form.cleaned_data.get('role')
            profile.save()
            
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been registered successfully as {profile.get_role_display()}.')
            return redirect('/feedback/')

    return render(request, 'register.html', {'form': form})


@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Feedback Submitted Successfully!')
            return redirect('feedback')
    else:
        form = FeedbackForm()

    # Fetch recent feedbacks from database
    feedbacks = Feedback.objects.all().order_by('-created_at')

    # Calculate average ratings
    breakfast_avg = Feedback.objects.filter(food_item='Breakfast').aggregate(Avg('rating'))['rating__avg']
    lunch_avg = Feedback.objects.filter(food_item='Lunch').aggregate(Avg('rating'))['rating__avg']
    dinner_avg = Feedback.objects.filter(food_item='Dinner').aggregate(Avg('rating'))['rating__avg']

    def format_rating(val):
        return round(val, 1) if val is not None else 0.0

    stats = {
        'Breakfast': format_rating(breakfast_avg),
        'Lunch': format_rating(lunch_avg),
        'Dinner': format_rating(dinner_avg),
    }

    return render(request, 'feedback.html', {
        'form': form,
        'feedbacks': feedbacks,
        'stats': stats,
    })
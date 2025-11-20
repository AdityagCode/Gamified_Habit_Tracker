from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Habit, HabitEntry
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user).prefetch_related('entries')
    today = timezone.localdate()

    # 🧮 Calculate total points
    total_points = sum(habit.points for habit in habits)

    # 🎯 Calculate level (example: every 100 points = 1 level)
    level = total_points // 100 + 1
    progress_to_next = total_points % 100  # remainder for progress bar

    # 📅 Weekly range
    #from datetime import timedelta
    week_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    next_level_points = 100 - progress_to_next

    return render(request, "home.html", {
        "habits": habits,
        "today": today,
        "week_days": week_days,
        "total_points": total_points,
        "level": level,
        "progress_to_next": progress_to_next,
        "next_level_points": next_level_points, 
    })


@login_required
def create_habit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("description", "")
        if title:
            Habit.objects.create(user=request.user, title=title, description=desc)
            messages.success(request, "Habit created.")
            return redirect("dashboard")
    return render(request, "create_habit.html")

@login_required
def toggle_done(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = timezone.localdate()
    entry, created = HabitEntry.objects.get_or_create(habit=habit, date=today)
    entry.done = not entry.done
    if entry.done:
        entry.earned_points = 10  # simple rule: 10 points per day
        habit.points += entry.earned_points
    else:
        # revert points if toggled off
        habit.points = max(0, habit.points - entry.earned_points)
        entry.earned_points = 0
    entry.save()
    habit.save()
    return redirect("dashboard")

@login_required(login_url='/accounts/login/')
def admin_dashboard(request):

    # Allow only superusers
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access the admin dashboard.")
        return redirect('/')

    total_users = User.objects.count()
    total_habits = Habit.objects.count()
    total_entries = HabitEntry.objects.count()
    completed_entries = HabitEntry.objects.filter(done=True).count()

    latest_habits = Habit.objects.order_by('-created_at')


    context = {
        "total_users": total_users,
        "total_habits": total_habits,
        "total_entries": total_entries,
        "completed_entries": completed_entries,
        "latest_habits": latest_habits
    }
    return render(request, "admin_dashboard.html", context)
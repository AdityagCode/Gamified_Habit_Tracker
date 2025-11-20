from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import google.generativeai as genai

from myapp.models import Habit, HabitEntry   # <-- Import your models


@csrf_exempt
@login_required(login_url="/accounts/login/")
def chat_view(request):

    if request.method == "GET":
        return render(request, "chat.html")

    elif request.method == "POST":
        user_message = request.POST.get("message", "")

        if not user_message:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        try:
            # ----------------------------
            # FETCH USER DATA FROM DB
            # ----------------------------
            habits = Habit.objects.filter(user=request.user)
            entries_today = HabitEntry.objects.filter(
                habit__user=request.user,
                date=timezone.localdate()
            )

            # Prepare structured info for AI
            db_context = f"""
User Name: {request.user.username}
Total Habits: {habits.count()}
Today's Completed Habits: {entries_today.filter(done=True).count()}
Today's Pending Habits: {entries_today.filter(done=False).count()}
Active Habits List:
{', '.join(h.title for h in habits if h.is_active)}
            """

            # ----------------------------
            # SEND DATA + USER QUERY TO GEMINI
            # ----------------------------
            genai.configure(api_key="AIzaSyBPTDIs7CCp31XiLxk_7wUqHsftJHMe04A")
            model = genai.GenerativeModel("gemini-2.0-flash")

            prompt = f"""
You are a personalized habit tracking assistant.

Here is the user's real data from the database:
{db_context}

Now answer this user query politely and based only on their data:
"{user_message}"
            """

            response = model.generate_content(prompt)
            bot_reply = response.text

            return JsonResponse({"reply": bot_reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai

@csrf_exempt
def chat_view(request):
    if request.method == "GET":
        # Just show the chat page
        return render(request, "chat.html")

    elif request.method == "POST":
        user_message = request.POST.get("message", "")
        if not user_message:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        try:
            genai.configure(api_key="AIzaSyB0QCA495PShjFQc4uXe-Ftk-wwLly85FE")# put your Gemini API key here  
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(user_message)
            bot_reply = response.text
            return JsonResponse({"reply": bot_reply})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

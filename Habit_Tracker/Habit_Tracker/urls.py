from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("myapp.urls")),
    #path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")), # login/logout templates
    #path("chatbot/", include("chatbot.urls")),
    
path("chat/", include("chatbot.urls")),

]

#chatbot/chat/
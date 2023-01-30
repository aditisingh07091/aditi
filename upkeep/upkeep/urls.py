from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/',include('my_app.urls')),
    path('api/chat',include('chat.urls')),
    path('api/Home',include('Home.urls'))
]


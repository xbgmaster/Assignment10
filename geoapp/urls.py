from django.urls import path
from . import views
from django.contrib import admin 
 
urlpatterns = [
    path('', views.continent_view),
    path('admin/', admin.site.urls),
    path('history/', views.history_view),
]

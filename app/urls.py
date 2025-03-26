from django.urls import re_path, path

from . import views

app_name = "app"

# http://localhost:8000/reports/f8d29622-f0af-46d8-b871-287fd6dbd5ec/
urlpatterns = [
    path('reports/<slug:slug>/', views.view, name='detail'),
]

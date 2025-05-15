
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',IndexView.as_view(),name="index"),
    path('tasks/<int:pk>/delete',task_delete_view,name="task_delete"),
    path('tasks/<int:pk>/update',TaskEditView.as_view(),name="task_update"),
]

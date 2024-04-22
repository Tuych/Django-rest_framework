from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api-viewset', views.TodoViewSet)

urlpatterns = [
    path('api/', views.TodoListApiView.as_view() ),
    path('api/<int:todo_id>/', views.TodoDetailApiView.as_view()),
    path('', include(router.urls))
]
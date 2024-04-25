from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api-viewset', views.TodoViewSet)

urlpatterns = [
    path('api/', views.TodoListApiView.as_view() ),
    path('api/<int:todo_id>/', views.TodoDetailApiView.as_view()),
    path('', include(router.urls)),
    path('generic/<int:pk>/', views.RetrieveDeleteItem.as_view()),
    path('mixins', views.CreateListItem.as_view()),
    path('mixins/<int:pk>/', views.RetrieveUpdateDeleteItem.as_view()),
    path('concreate-view/', views.ListAPIItem.as_view()),
    path('movie/create/', views.MovieCreateItem.as_view()),
    path('movie/list/', views.MovieListItem.as_view()),

]
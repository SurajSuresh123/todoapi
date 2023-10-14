from django.urls import path
from .views import * 
urlpatterns=[
  path('',userview.as_view()),
  path('create/',createTodo.as_view()),
  path('update/<str:pk>/',updateTodo.as_view()),
  path('delete/<str:pk>/',deleteTodo.as_view()),
  path('register/',register.as_view()),
  path('login/',login.as_view()),
  path('logout/',logout.as_view()),
]
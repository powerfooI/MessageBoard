from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('manage_the_message/', views.manage, name='manage'),
    path('index/<int:page_num>/', views.index, name='index'),
    path('manage_the_message/<int:page_num>/', views.manage, name='manage'),
    path('write_message/', views.write_message, name='write_message'),
    path('check_pass/<int:message_id>/<int:page_num>/', views.check_pass, name='check_pass'),
    path('detail/<int:message_id>/<int:page_num>/', views.detail, name='detail'),
]

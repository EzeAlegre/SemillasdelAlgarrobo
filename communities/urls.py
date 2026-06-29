from django.urls import path

from . import views

app_name = 'communities'

urlpatterns = [
    path('', views.community_list, name='list'),
    path('<int:pk>/', views.community_detail, name='detail'),
    path('necesidades/<int:need_pk>/donar/', views.donate_api, name='donate'),
    path('mis-necesidades/', views.my_needs, name='my_needs'),
]

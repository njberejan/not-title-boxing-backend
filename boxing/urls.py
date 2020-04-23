from django.urls import path

from boxing import views

urlpatterns = [
    path('', views.WorkOutView.as_view(), name='workout')
]

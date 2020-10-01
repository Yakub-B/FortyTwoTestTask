from django.urls import path

from apps.requests import views

app_name = 'requests'

urlpatterns = [
    path('', views.LastTenRequestsView.as_view(), name='last_requests')
]

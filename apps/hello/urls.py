from django.urls import path
from apps.hello import views

app_name = 'hello'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('edit-profile/', views.EditProfileDataView.as_view(), name='edit')
]

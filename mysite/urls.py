from django.urls import path
from .views import views

app_name = 'mysite'

urlpatterns = [
    path('',views.shihuto_submit,name='submit'),
    path('check/<int:pk>',views.check,name='check')
]
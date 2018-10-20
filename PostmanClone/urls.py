from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('contact', views.contact, name='contact'),
    path('thanks', views.emailThankYou, name='thanks'),
    path('changeCollection', views.changeCollection, name='changeCollection'),
]
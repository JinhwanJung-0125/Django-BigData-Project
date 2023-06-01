from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("accessDB", views.accessDB, name="accessDB"),
    path("houseListTable", views.houseListTable, name="houseListTable"),
]

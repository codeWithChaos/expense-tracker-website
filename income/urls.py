from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="income"),
    path('add-income', views.add_income, name="add-income"),
    path('edit-income/<int:id>/', views.edit_income, name='edit-income'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expenses.urls')),
    path('authentication/', include('authentication.urls')),
    path('userpreferences/', include('userpreferences.urls')),
    path('income/', include('income.urls')),
]

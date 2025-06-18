from django.urls import path, include

urlpatterns = [
    path('api/', include('virtual_ta.urls')),
    path('', include('virtual_ta.urls')),
]

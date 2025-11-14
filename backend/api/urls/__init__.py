from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.urls.auth_urls')),

    path('public/', include('api.urls.public_urls')),
    path('image/', include('api.urls.image_urls')),
]
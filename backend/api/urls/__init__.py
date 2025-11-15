from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.urls.auth_urls')),
    path('image/', include('api.urls.image_urls')),

    path('participants/', include('api.urls.participant_urls')),
    path('public/', include('api.urls.public_urls')),
]
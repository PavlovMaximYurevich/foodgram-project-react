import djoser as djoser
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SimpleUserViewSet

app_name = 'users'

router = DefaultRouter()

router.register('users', SimpleUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

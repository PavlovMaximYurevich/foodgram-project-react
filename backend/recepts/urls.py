from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, IngridientsViewSet

app_name = 'recepts'

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngridientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]

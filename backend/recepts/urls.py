from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, IngridientsViewSet

app_name = 'recepts'

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingridients', IngridientsViewSet, basename='ingridients')

urlpatterns = [
    path('', include(router.urls)),
]

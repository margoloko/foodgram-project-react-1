from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet 


app_name = 'api'

router = DefaultRouter()

#router.register('users', UsersViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
    #re_path(r'auth/', include('djoser.urls.authtoken')),
    #path('', include('djoser.urls')),
    #path(r'^auth/', include('djoser.urls.authtoken'))
]
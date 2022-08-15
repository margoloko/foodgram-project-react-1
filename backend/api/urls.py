from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet, IngredientViewSet, RecipeViewSet, TagViewSet, UsersViewSet


app_name = 'api'

router = DefaultRouter()

router.register('users', UsersViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
#router.register('users/subscriptions', FollowViewSet, basename='subscriptions')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    #path('users/<int:user_id>/subscribe/', name='subscribe')
]

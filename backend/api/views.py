from djoser.views import UserViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework import (filters, mixins,
                           permissions, status, viewsets)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

from .pagination import LimitPagePagination
from .permissions import AdminOrAuthor, AdminOrReadOnly
from recipes.models import Ingredient, Recipe, Tag
from .serializers import (IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          UsersSerializer, TagSerializer)
from users.models import Follow, User
#User = get_user_model()


class UsersViewSet(UserViewSet):
    """Вьюсет для модели пользователей."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = LimitPagePagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('username', 'email')


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPagePagination

    permission_classes = (AdminOrAuthor,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_favorited', 'author', 'is_in_shopping_cart', 'tags',)

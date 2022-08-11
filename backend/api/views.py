from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import decorators, filters, mixins, permissions, status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

from .pagination import LimitPagePagination
from .permissions import AdminOrAuthor, AdminOrReadOnly
from recipes.models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, RecipeSerializer, UsersSerializer, TagSerializer
from users.models import Follow, User


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


#User = get_user_model()


class UsersViewSet(UserViewSet):
    """Класс-вьюсет для модели User."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = LimitPagePagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('email', 'username')


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPagePagination
    permission_classes = (AllowAny,)
    #permission_classes = (AdminOrAuthor,)
    #filter_backends = (DjangoFilterBackend,)
    #filterset_fields = ('is_favorited', 'author', 'is_in_shopping_cart', 'tags',)
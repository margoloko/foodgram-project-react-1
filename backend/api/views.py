from django.shortcuts import render
#from djoser.views import UserViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import decorators, filters, mixins, permissions, status, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from .pagination import LimitPagePagination
from .permissions import AdminOrAuthor, AdminOrReadOnly
from recipes.models import Ingredient, Recipe, Tag
#from users.models import Follow, User


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    #permission_classes = (AdminOrAuthor,)
    filter_backends = (DjangoFilterBackend,)
    #filterset_fields = ('is_favorited', 'author', 'is_in_shopping_cart', 'tags',)
    pagination_class = LimitPagePagination
from django.shortcuts import render
from urllib import request
from django.http import HttpResponse
from djoser.views import UserViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import (filters, mixins,
                           permissions, status, viewsets)
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated


from .pagination import LimitPagePagination
from .permissions import AdminOrAuthor, AdminOrReadOnly
from recipes.models import AmountIngredients, Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .serializers import (FollowRecipeSerializer, IngredientSerializer,
                          RecipeCreateSerializer,
                          RecipeForFollowersSerializer,
                          RecipeSerializer,
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

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        following = Follow.objects.filter(user=self.request.user)
        pages = self.paginate_queryset(following)
        serializer = FollowRecipeSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowRecipeSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)





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
    filterset_fields = ('author', 'tags',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            Favorite.objects.create(user=request.user,
                                    recipe=recipe)
            serializer = RecipeForFollowersSerializer(recipe)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        deleted = get_object_or_404(Favorite,
                                         user=request.user,
                                         recipe=recipe)
        deleted.delete()
        return Response({'message': 'Рецепт успешно удален из избранного'},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            ShoppingCart.objects.create(user=request.user,
                                    recipe=recipe)
            serializer = RecipeForFollowersSerializer(recipe)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        deleted = get_object_or_404(ShoppingCart,
                                    user=request.user,
                                    recipe=recipe)
        deleted.delete()
        return Response({'message': 'Рецепт успешно удален из списка покупок'},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        recipes = list(
            request.user.shopping_cart.all().values_list('recipe__id', flat=True)
        )
        ingredients = AmountIngredients.objects.filter(recipe__in=recipes).values('ingredients__name', 'ingredients__measurement_unit').annotate(amount=Sum('amount'))
        data = ingredients.values_list('ingredients__name',
                                       'ingredients__measurement_unit',
                                       'amount')
        shopping_cart = 'Список покупок: '
        for name, measure, amount in data:
            shopping_cart += (f'{name.capitalize()} {amount} {measure}, ')
        response = HttpResponse(shopping_cart, content_type='text/plain')
        #response['Content-Disposition'] = ('attachment' 'filename="shopping_cart.txt"')
        return response








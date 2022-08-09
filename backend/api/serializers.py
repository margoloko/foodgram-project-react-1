#from requests import request
from wsgiref.validate import validator
from drf_extra_fields.fields import Base64ImageField
from string import hexdigits
from requests import request
#from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, ReadOnlyField, SerializerMethodField, ValidationError, EmailField, CharField
from rest_framework.validators import UniqueValidator
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import AmountIngredients, Ingredient, Recipe, Tag
from users.models import User

#User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""
    username = CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    email = EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name',
                  'password',)
        extra_kwargs = {'password': {'write_only': True}}


class UsersSerializer(UserSerializer):
    """."""
    is_subscribed = SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username',
                  'first_name', 'last_name',
                  'email', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.subscribe.filter(id=obj.id).exists()
        return False




class FollowSerializer(UserSerializer):
    """С."""
    #is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username',
                  'first_name', 'last_name',
                  'email', 'is_subscribed',
                  'recipes_count', 'recipes')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.subscribe.filter(id=obj.id).exists()
        return False

    def get_recipes(self, obj):
        limit = self.context['limit']
        if limit:
            recipes = obj.author.recipes.all()[:int(limit)]
        recipes = obj.author.recipes.all()
        return FollowSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class TagSerializer(ModelSerializer):
    """Сериализатор для тэгов."""
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__'


class IngredientSerializer(ModelSerializer):
    """."""
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__'


class RecipeSerializer(ModelSerializer):
    """."""
    author = UserSerializer(read_only=True)
    #ingrediens = AmountIngredientsSerializer(many=True,
                                             #read_only=True,)
    tags = TagSerializer(many=True, read_only=True)
    is_in_shopping_cart = SerializerMethodField()
    is_favorited = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.favorites.filter(id=obj.id).exists() #!!!!!!!!!!
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            #!!!!!!!!!!
            return user.carts.filter(id=obj.id).exists()
        return False

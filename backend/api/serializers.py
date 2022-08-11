#from requests import request
from wsgiref.validate import validator
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from string import hexdigits
from requests import request
#from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError, IntegerField, PrimaryKeyRelatedField, ModelSerializer, ReadOnlyField, SerializerMethodField, ValidationError, EmailField, CharField
from rest_framework.validators import UniqueValidator
#from rest_framework import serializers
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
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')


class TagSerializer(ModelSerializer):
    """Сериализатор для тэгов."""
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['id', 'name', 'slug', 'color',]


class IngredientSerializer(ModelSerializer):
    """."""
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ['id', 'name', 'measurement_unit',]


class IngredientAmountSerializer(ModelSerializer):
    """."""
    #ingredient = IngredientSerializer(many=True)
    id = IntegerField()
    #name = ReadOnlyField(source='ingredient.name')
    #measurement_unit = ReadOnlyField(source='ingredient.measurement_unit'    )
    #amount = IntegerField()
    

    class Meta:
        model = AmountIngredients
        fields = ('id', 'amount')
    def to_representation(self, instance):
        representation = IngredientSerializer(instance.amount_ingredient).data
        representation['amount'] = instance.amount
        return representation

        



class RecipeSerializer(ModelSerializer):
    """."""
    author = UsersSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True)#, source='ingredient')
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

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            #!!!!!!!!!!
            return user.carts.filter(id=obj.id).exists()
        return False

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.favorites.filter(id=obj.id).exists() #!!!!!!!!!!
        return False

 

  
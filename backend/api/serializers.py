#from requests import request
from wsgiref.validate import validator
from drf_extra_fields.fields import Base64ImageField
from string import hexdigits
from requests import request
#from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, ReadOnlyField, SerializerMethodField, ValidationError, EmailField, CharField
from rest_framework.validators import UniqueValidator
#from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Ingredient, Tag
#from users.models import User

#User = get_user_model()





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


class RecipeSerializer(ModelSerializer):
    """."""
    #author = UserSerializer(read_only=True)
    #ingrediens = AmountIngredientsSerializer(many=True,
                                             #read_only=True,)
    tags = TagSerializer(many=True, read_only=True)
    #is_in_shopping_cart = SerializerMethodField()
    #is_favorited = SerializerMethodField()
    image = Base64ImageField()
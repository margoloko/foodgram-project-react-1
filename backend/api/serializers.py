from django.db.models import F
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (AmountIngredients, Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from rest_framework.serializers import (CharField, EmailField, Field,
                                        IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField, ValidationError)
from rest_framework.validators import UniqueValidator
from users.models import Follow, User


class CreateUserSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""
    username = CharField(validators=[UniqueValidator(
        queryset=User.objects.all())])
    email = EmailField(validators=[UniqueValidator(
        queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name',
                  'password',)
        extra_kwargs = {'password': {'write_only': True}}


class UsersSerializer(UserSerializer):
    """Сериализатор пользователей."""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Follow.objects.filter(user=user, author=obj).exists()
        return False


class TagSerializer(ModelSerializer):
    """Сериализатор для тэгов."""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    """Сериализатор для ингредиентов."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientCreateSerializer(ModelSerializer):
    """Сериализатор для добавления ингредиентов при создании рецепта."""
    id = IntegerField()

    class Meta:
        model = AmountIngredients
        fields = ('id', 'amount')


class ReadIngredientsInRecipeSerializer(ModelSerializer):
    """Сериализатор для чтения ингредиентов в рецепте."""
    id = ReadOnlyField(source='ingredients.id')
    name = ReadOnlyField(source='ingredients.name')
    measurement_unit = ReadOnlyField(source='ingredients.measurement_unit')

    class Meta:
        model = AmountIngredients
        fields = ('id', 'name',
                  'measurement_unit',
                  'amount',)


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов."""
    author = UsersSerializer(read_only=True)
    ingredients = SerializerMethodField()
    tags = TagSerializer(many=True)
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
            return ShoppingCart.objects.filter(
                user=user, recipe=obj).exists()
        return False

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated or self.context.get('request') is not None:
            return Favorite.objects.filter(
                user=user, recipe=obj).exists()
        return False

    @staticmethod
    def get_ingredients(obj):
        ingredients = AmountIngredients.objects.filter(recipe=obj)
        return ReadIngredientsInRecipeSerializer(ingredients, many=True).data


class RecipeCreateSerializer(ModelSerializer):
    """Сериализатор для создания рецептов."""
    ingredients = IngredientCreateSerializer(many=True)
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                  many=True)
    image = Base64ImageField()
    name = CharField(max_length=200)
    cooking_time = IntegerField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags',
                  'image', 'name', 'text',
                  'cooking_time', 'author')

    @staticmethod
    def create_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            amount = ingredient['amount']
            if AmountIngredients.objects.filter(
                    recipe=recipe,
                    ingredients=get_object_or_404(
                        Ingredient, id=ingredient['id'])).exists():
                amount += F('amount')
            AmountIngredients.objects.update_or_create(
                recipe=recipe,
                ingredients=get_object_or_404(
                    Ingredient, id=ingredient['id']),
                defaults={'amount': amount})

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(image=image,
                                       **validated_data)
        self.create_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        AmountIngredients.objects.filter(recipe=recipe).delete()
        self.create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def to_representation(self, recipe):
        data = RecipeSerializer(
            recipe,
            context={'request': self.context.get('request')}).data
        return data

    def validate_cooking_time(self, cooking_time):
        if cooking_time <= 0:
            raise ValidationError('Время приготовления должно быть больше 0')
        return cooking_time

    def validate_ingredients(self, ingredients):
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise ValidationError(
                    'Количество ингредиентов должно быть больше 0')
        return ingredients


class RecipeForFollowersSerializer(ModelSerializer):
    """Сериализатор для вывода рецептов в избранном и списке покупок."""
    class Meta:
        model = Recipe
        fields = ('id', 'name',
                  'image', 'cooking_time')


class RecipeFollowUserField(Field):
    """Сериализатор для вывода рецептов в подписках."""

    def get_attribute(self, instance):
        return Recipe.objects.filter(author=instance.author)

    def to_representation(self, recipes_list):
        recipes_data = []
        for recipes in recipes_list:
            recipes_data.append(
                {
                    "id": recipes.id,
                    "name": recipes.name,
                    "image": recipes.image.url,
                    "cooking_time": recipes.cooking_time,
                }
            )
        return recipes_data


class FollowSerializer(ModelSerializer):
    """Сериализатор для подписок."""
    recipes = RecipeFollowUserField()
    recipes_count = SerializerMethodField(read_only=True)
    id = ReadOnlyField(source='author.id')
    email = ReadOnlyField(source='author.email')
    username = ReadOnlyField(source='author.username')
    first_name = ReadOnlyField(source='author.first_name')
    last_name = ReadOnlyField(source='author.last_name')
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed',
                  'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(user=obj.user, author=obj.author).exists()

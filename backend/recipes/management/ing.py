from recipes.models import AmountIngredients

def recipe_ingredients_set(recipe, ingredients):
    for ingredient in ingredients:
        AmountIngredients.objects.get_or_create(
            recipe=recipe,
            ingredients=ingredient['ingredient'],
            amount=ingredient['amount']
        )

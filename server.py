"""
The Server file. Hosts the server.
"""
# Standard imports
import os
from pathlib import Path

# Third Party Imports
from flask import render_template

# Custom Imports
import core
from planner_logger import add_to_log
from recipe_manager import RecipeManager
import ingredient_aggregator # Initializes socket listener

# Creates the manager
manager = RecipeManager()

def get_recipe_image(image_name, resolution):
    """
    Checks for the existence of an image, then returns it in POSIX style for the webpage.
    """
    # A list of accepted image extensions
    extensions = ['.png', '.jpeg', '.jpg']

    recipe_image_dir = Path('static/images/recipes')

    image_to_check = recipe_image_dir / image_name

    image_exists = False

    for ext in extensions:
        if os.path.exists(image_to_check.with_suffix(ext)):
            image_exists = True
            image = image_to_check.with_suffix(ext)
            break

    if image_exists:
        return image.relative_to('static').as_posix()
    else:
        return f'images/placeholder_{resolution}.svg'

def condense_array(array):
    """
    Condenses a 2D array into a 1D array.
    """
    return [x for row in array for x in row]

def condense_data(ingredients, data_type):
    """
    Ingredients are stored in a split up format if sectioned. This condenses it if necessary.
    """
    flatten = False
    ingredient_list = []

    # If sectioned, data is stored in a dict within.
    for ingredient in ingredients:

        if isinstance(ingredients.get(ingredient), dict):
            flatten = True
            ingredient_list.append(ingredients.get(ingredient).get(data_type))

    if flatten:
        return condense_array(ingredient_list)

    return ingredients.get(data_type)

@core.app.route('/')
def homepage():
    """
    The homepage.
    """
    recipe_names = manager.get_recipe_names()

    recipe_images = [get_recipe_image(recipe, 300) for recipe in recipe_names]

    recipe_data = manager.get_recipes()
    ingredients  = []
    measurements = []

    for recipe in recipe_data:
        ingredients .append(condense_data(recipe_data.get(recipe).get('ingredients'), 'ingredients'))
        measurements.append(condense_data(recipe_data.get(recipe).get('ingredients'), 'measurements'))

    recipe_card_data= zip(manager.get_recipe_names(), measurements, ingredients, manager.get_recipe_meal_types(), recipe_images)

    return render_template('homepage.html', page_id='homepage', page_name="Homepage", recipe_data=recipe_data, recipe_card_data=recipe_card_data)

@core.app.route('/recipe/<recipe>')
def recipe_page(recipe):
    """
    The page for recipes.
    """
    recipe = manager.get_recipe(recipe)
    recipe_name = recipe.get('name')
    recipe_image = get_recipe_image(recipe_name, 500)

    headers = []
    recipe_ingredients = []
    ingredients = []
    measurements = []

    for header in recipe.get('ingredients'):
        if isinstance(recipe.get('ingredients').get(header), dict):
            headers.append(header)

            ingredients .append(recipe.get('ingredients').get(header).get('ingredients'))
            measurements.append(recipe.get('ingredients').get(header).get('measurements'))

    if len(headers) == 0:
        ingredients  = condense_data(recipe.get('ingredients'), 'ingredients')
        measurements = condense_data(recipe.get('ingredients'), 'measurements')

        # Opposite because better looking format is # - ingredient
        recipe_ingredients = zip(measurements, ingredients)
    else:
        for header, ingredient_list, measurement_list in zip(headers, ingredients, measurements):
            recipe_ingredients.append((header, list(zip(measurement_list, ingredient_list))))

    print('headers', headers)
    return render_template('recipe_page.html', page_id='recipe_page', page_name=recipe_name, recipe=recipe, headers=headers, recipe_ingredients=recipe_ingredients, recipe_image=recipe_image)

@core.socketio.on('delete-recipe')
def delete_recipe(data):
    """
    Deletes a recipe from the data if it exists.
    """
    recipe_to_delete = data['recipe']

    # recipe_to_delete = recipe_to_delete.title()

    if manager.contains_recipe(recipe_to_delete):
        manager.delete_recipe(recipe_to_delete)
        core.socketio.emit('recipe-deleted')

if __name__ == '__main__':
    add_to_log('[INFO] Starting server!')

    manager.load_tsv_recipes('data/recipes.tsv', 'data/instructions.tsv')

    core.socketio.run(core.app, debug=True)

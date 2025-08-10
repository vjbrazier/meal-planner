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

@core.app.route('/')
def homepage():
    """
    The homepage.
    """
    recipe_names = manager.get_recipe_names()

    recipe_images = [get_recipe_image(recipe, 300) for recipe in recipe_names]

    recipe_data = manager.get_recipes()
    recipe_card_data= zip(manager.get_recipe_names(), manager.get_recipe_measurements(), manager.get_recipe_ingredients(), manager.get_recipe_meal_types(), recipe_images)

    return render_template('homepage.html', page_id='homepage', recipe_data=recipe_data, recipe_card_data=recipe_card_data)

@core.app.route('/<recipe>')
def recipe_page(recipe):
    """
    The page for recipes.
    """
    recipe = manager.get_recipe(recipe)
    recipe_name = recipe.get('name')

    recipe_image = get_recipe_image(recipe_name, 500)

    recipe_ingredients = zip(recipe.get('measurements'), recipe.get('ingredients'))

    return render_template('recipe_page.html', page_id='recipe_page', recipe=recipe, recipe_ingredients=recipe_ingredients, recipe_image=recipe_image)

if __name__ == '__main__':
    add_to_log('[INFO] Starting server!')

    manager.load_tsv_recipes('data/data.tsv', 'data/instructions.tsv')

    core.app.run('0.0.0.0', 5000, debug=True)

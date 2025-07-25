"""
The Server file. Hosts the server.
"""
# Third Party Imports
from flask import render_template

# Custom Imports
import core
from planner_logger import add_to_log
from recipe_manager import RecipeManager

# Creates the manager
manager = RecipeManager()

@core.app.route('/')
def index():
    """
    The index page.
    """
    return render_template('index.html', recipes=manager.get_recipe_list())

@core.app.route('/<recipe>')
def recipe_page(recipe):
    """
    The page for recipes.
    """
    return render_template('recipe_page.html', recipe=manager.get_recipe(recipe))

if __name__ == '__main__':
    add_to_log('[INFO] Starting server!')

    manager.create_recipe('enchiliadas', ['corn', 'chicken'], ['1 cup', '2 cups'], ['Grab shell', 'Make thing'], 'Dinner', 100, 50, 10, 5)
    manager.create_recipe('enchiliadas2', ['corn', 'chicken'], ['1 cup', '2 cups'], ['Grab shell', 'Make thing'], 'Dinner', 100, 50, 10, 5)
    manager.create_recipe('enchiliadas3', ['corn', 'chicken'], ['1 cup', '2 cups'], ['Grab shell', 'Make thing'], 'Dinner', 100, 50, 10, 5)
    manager.create_recipe('enchiliadas4', ['corn', 'chicken'], ['1 cup', '2 cups'], ['Grab shell', 'Make thing'], 'Dinner', 100, 50, 10, 5)
    manager.create_recipe('enchiliadas5', ['corn', 'chicken'], ['1 cup', '2 cups'], ['Grab shell', 'Make thing'], 'Dinner', 100, 50, 10, 5)

    # manager.load_tsv_recipes('data/data.tsv')

    core.app.run('0.0.0.0', 5000, debug=True)

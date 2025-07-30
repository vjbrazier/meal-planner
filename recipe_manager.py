"""
Recipe Manager. Handles creation of recipes, as well as saving and loading saved recipe data.
"""
# Standard Imports
import json

# Custom Imports
import core
from recipe import Recipe
from planner_logger import add_to_log

class RecipeManager:
    """
    Class used to handle recipes.
    """
    def __init__(self, recipe_data_path=core.recipe_data_path):
        self.recipe_data_path = recipe_data_path

        self.recipes = self.load_input_recipes()

    def clean_array_items(self, arr):
        """
        Strips whitespace, and lowercases all letters in an array's items.
        """
        for index, item in enumerate(arr):
            item = item.strip().lower()
            arr[index] = item

        return arr

    def load_input_recipes(self, dict_data=None):
        """
        Loads recipes from the JSON file or from the data provided into live memory.
        Returns a dictionary of the data loaded.
        """
        if dict_data is None:
            with open(self.recipe_data_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
        else:
            raw_data = dict_data

        recipes = {}

        for recipe, data in raw_data.items():
            add_to_log(f'[INFO] Loading data for {recipe}...')

            recipes[recipe] = Recipe(
                name=recipe,
                ingredients= data.get('ingredients'),
                measurements=data.get('measurements'),
                instructions=data.get('instructions'),
                meal_type=data.get('meal_type'),
                calories=data.get('calories'),
                protein=data.get('protein'),
                carbs=data.get('carbs'),
                fat=data.get('fat')
            )

            add_to_log(f'[INFO] Finished loading data for {recipe}!')

        add_to_log('[INFO] Successfully loaded all recipes!')
        return recipes

    def load_tsv_recipes(self, data_tsv_file, instruction_tsv_file):
        """
        Loads recipes from a .tsv file into live memory
        """
        recipe_data = {}

        with open(data_tsv_file, 'r', encoding='utf-8') as f:
            next(f) # Skips the header

            for line_count, line in enumerate(f, start=2):
                current_line = line.strip().split('\t')

                try:
                    name = current_line[0].lower()

                    recipe = {
                        'name': name,
                        'ingredients':  self.clean_array_items(current_line[1].split(',')),
                        'measurements': self.clean_array_items(current_line[2].split(',')),
                        'meal_type': current_line[3],
                        'calories': int(current_line[4]) if len(current_line) > 4 and current_line[4].isdigit() else 'N/A',
                        'protein':  int(current_line[5]) if len(current_line) > 5 and current_line[5].isdigit() else 'N/A',
                        'carbs':    int(current_line[6]) if len(current_line) > 6 and current_line[6].isdigit() else 'N/A',
                        'fat':      int(current_line[7]) if len(current_line) > 7 and current_line[7].isdigit() else 'N/A',
                    }

                    recipe_data[name] = recipe

                except Exception as e:
                    add_to_log(f'[ERROR] An error occurred on line {line_count} of {data_tsv_file}: {e}')

        with open(instruction_tsv_file, 'r', encoding='utf-8') as f:
            next(f) # Skips the header

            for line_count, line in enumerate(f, start=2):
                current_line = line.strip().split('\t')

                try:
                    name = current_line[0].lower()
                    current_line.pop(0)

                    if recipe_data.get(name):
                        recipe_data[name].setdefault('instructions', current_line)

                except Exception as e:
                    add_to_log(f'[ERROR] An error occurred on line {line_count} of {instruction_tsv_file}: {e}')

        self.recipes.update(self.load_input_recipes(recipe_data))
        self.save_recipes()

    def save_recipes(self):
        """
        Saves current recipes to the JSON.
        """
        add_to_log('[INFO] Saving current recipes...')
        with open(self.recipe_data_path, 'w', encoding='utf-8') as f:
            json.dump({recipe.name.lower(): recipe.to_dict() for recipe in self.recipes.values()}, f, indent=4)
        add_to_log('[INFO] Finished saving recipes!')

    def create_recipe(self, name, ingredients, measurements, instructions, meal_type, calories, protein, carbs, fat):
        """
        Creates a new recipe.
        """
        add_to_log(f'[INFO] Creating recipe {name}...')
        self.recipes[name] =  Recipe(
                name=name,
                ingredients=ingredients,
                measurements=measurements,
                instructions=instructions,
                meal_type=meal_type,
                calories=calories,
                protein=protein,
                carbs=carbs,
                fat=fat
            )
        self.save_recipes()

    def get_recipe_names(self):
        """
        Returns all of the recipes names as a list.
        """
        return self.recipes.keys()

    def get_recipes(self):
        """
        Returns all of the recipes in a dict format.
        """
        return {recipe.name.lower(): recipe.to_dict() for recipe in self.recipes.values()}

    def get_recipe(self, recipe):
        """
        Returns a recipe as a dict.
        """
        return self.recipes.get(recipe).to_dict()

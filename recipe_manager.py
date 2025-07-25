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

        self.recipes = self.load_json_recipes()

    def clean_array_items(self, arr):
        """
        Trims and capitalizes all items in an array.
        """

        for index, item in enumerate(arr):
            item = item.strip().lower()
            arr[index] = item

    def load_json_recipes(self):
        """
        Loads recipes from the JSON file into live memory.
        """
        with open(self.recipe_data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

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

    def load_tsv_recipes(self, tsv_file):
        """
        Loads recipes from a .tsv file into live memory
        """
        with open(tsv_file, 'r', encoding='utf-8') as f:
            # Skips the header
            next(f)
            
            line_count = 0
            for line in f:
                line_count += 1
                current_line = line.split('\t')

                print(current_line)

                if len(current_line) == 9:
                    name = current_line[0]
                    ingredients  = list(current_line[1].split(','))
                    measurements = list(current_line[2].split(','))
                    instructions = list(current_line[3].split(','))
                    meal_type = current_line[4]
                    calories = current_line[5]
                    protein = current_line[6]
                    carbs = current_line[7]
                    fat = current_line[8]

                    self.clean_array_items(ingredients)
                    self.clean_array_items(measurements)
                    self.clean_array_items(instructions)

                    self.create_recipe(name, ingredients, measurements, instructions, meal_type, calories, protein, carbs, fat)

                else:
                    add_to_log(f'[ERROR] An error occurred when trying to read line {line_count} of {tsv_file}.')


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

    def get_recipe_list(self):
        """
        Returns a list of all the recipe names.
        """
        return self.recipes.keys()

    def get_recipe(self, recipe):
        """
        Returns a recipe as a dict.
        """
        return self.recipes.get(recipe).to_dict()

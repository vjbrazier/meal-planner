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

    def determine_headers(self, ingredients):
        """
        Determines if ingredients contains sections like [Filling].
        """
        if '[' in ingredients:
            headers = []
            
            while '[' in ingredients:
                # Gets the section part
                start_index = ingredients.index('[')
                end_index = ingredients.index(']')

                headers.append(ingredients[start_index+1:end_index])
                ingredients = ingredients[:start_index] + ingredients[end_index + 1:]
            return headers
        
        return None

    def convert_ingredients(self, passed_ingredients, headers=None):
        """
        Converts ingredients from a long string into a list.
        If headers are involved, it's a 2D list with each row belonging to a section.
        """
        if headers:
            ingredients = []

            while ']' in passed_ingredients:
                # Get index of the end of the first header
                start_index = passed_ingredients.index(']')

                # Find the beginning of the next header
                next_header = passed_ingredients.find('[', start_index)
                if next_header is not -1:
                    end_index  = passed_ingredients.index('[', start_index)
                else:
                    end_index = len(passed_ingredients)

                # Append just the current ingredients
                ingredients.append(self.clean_array_items(passed_ingredients[start_index + 1:end_index].split(',')))

                # Remove the current ingredients from the string before checking again
                passed_ingredients = passed_ingredients[start_index + 1:]

            return ingredients

        return passed_ingredients.split(',')

    def split_ingredient(self, ingredient, segment_desired):
        """
        Splits ingredients and gets either the ingredient or the measurement from it.
        """
        units = [
            'lb', 'lbs', 'pound', 'pounds',
            'oz', 'ounce', 'ounces',
            'cup', 'cups',
            'tbsp', 'tbsps', 'tablespoon', 'tablespoons',
            'tsp', 'tsps', 'teaspoon', 'teaspoons'
        ]

        # Check if this is measured or flat
        for unit in units:
            if unit in ingredient:
                # Determines what segement to keep
                if segment_desired == 'ingredient':
                    index = ingredient.index(unit) + len(unit)
                    return ingredient[index:].strip()
                
                index = ingredient.index(unit) + len(unit)
                return ingredient[:index].strip()

        # Same as above, but for lack of a measurement
        index = ingredient.index(' ')
        if segment_desired == 'ingredient':
            return ingredient[index:].strip()
        
        return ingredient[:index].strip()

    def extract_ingredients(self, raw_ingredients, headers):
        """
        Takes an array of ingredients, and creates dicts with their ingredients and measurements split.
        """
        if headers:
            ingredients = {}

            for section, header in enumerate(headers):
                ingredients.setdefault(header, {'ingredients': [], 'measurements': []})

                for ingredient in raw_ingredients[section]:
                    ingredients.get(header).get('ingredients') .append(self.split_ingredient(ingredient.strip(), 'ingredient'))
                    ingredients.get(header).get('measurements').append(self.split_ingredient(ingredient.strip(), 'measurement'))

            return ingredients

        ingredients = {'ingredients': [], 'measurements': []}
        for ingredient in raw_ingredients:
            ingredients.get('ingredients') .append(self.split_ingredient(ingredient.strip(), 'ingredient'))
            ingredients.get('measurements').append(self.split_ingredient(ingredient.strip(), 'measurement'))
        return ingredients

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
                instructions=data.get('instructions'),
                meal_type=data.get('meal_type'),
                servings=data.get('servings'),
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

                # try:
                if True:
                    name = current_line[0].lower()

                    headers = self.determine_headers(current_line[1].strip())
                    raw_ingredients = self.convert_ingredients(current_line[1], headers)
                    ingredients  = self.extract_ingredients(raw_ingredients, headers)

                    recipe = {
                        'name': name,
                        'ingredients':  ingredients,
                        'meal_type': current_line[2],
                        'servings': int(current_line[3]) if len(current_line) > 3 and current_line[3].isdigit() else 'N/A',
                        'calories': int(current_line[4]) if len(current_line) > 4 and current_line[4].isdigit() else 'N/A',
                        'protein':  int(current_line[5]) if len(current_line) > 5 and current_line[5].isdigit() else 'N/A',
                        'carbs':    int(current_line[6]) if len(current_line) > 6 and current_line[6].isdigit() else 'N/A',
                        'fat':      int(current_line[7]) if len(current_line) > 7 and current_line[7].isdigit() else 'N/A',
                    }

                    recipe_data[name] = recipe

                # except Exception as e:
                #     add_to_log(f'[ERROR] An error occurred on line {line_count} of {data_tsv_file}: {e}')
                #     continue

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

    def sort_recipes(self):
        """
        Sorts the recipes alphabetically by name.
        """
        sorted_names = sorted(self.recipes.keys())
        sorted_recipes = {}

        for recipe in sorted_names:
            sorted_recipes.setdefault(recipe, self.recipes.get(recipe))

        self.recipes = sorted_recipes

    def save_recipes(self):
        """
        Saves current recipes to the JSON.
        """
        self.sort_recipes()

        add_to_log('[INFO] Saving current recipes...')
        with open(self.recipe_data_path, 'w', encoding='utf-8') as f:
            json.dump({recipe.name.lower(): recipe.to_dict() for recipe in self.recipes.values()}, f, indent=4)
        add_to_log('[INFO] Finished saving recipes!')

    def create_recipe(self, name, ingredients, instructions, meal_type, servings, calories, protein, carbs, fat):
        """
        Creates a new recipe.
        """
        add_to_log(f'[INFO] Creating recipe {name}...')
        self.recipes[name] =  Recipe(
                name=name,
                ingredients=ingredients,
                instructions=instructions,
                meal_type=meal_type,
                servings=servings,
                calories=calories,
                protein=protein,
                carbs=carbs,
                fat=fat
            )
        self.save_recipes()

    def delete_recipe(self, recipe):
        """
        Deletes a recipe, then refreshes the data.
        """
        self.recipes.pop(recipe)
        self.save_recipes()

    def contains_recipe(self, recipe):
        """
        Checks if a recipe exists in its live memory.
        """
        exists = recipe in self.recipes
        if not exists:
            add_to_log(f'[WARN]It seems a non-existent recipe was tried to be deleted: {recipe}')
            
        return exists

    def get_recipe_names(self):
        """
        Returns all of the recipes names as a list.
        """
        return self.recipes.keys()

    def get_recipe_measurements(self):
        """
        Returns a 2D array containing all recipe measurements.
        """
        names = self.get_recipe_names()
        return [self.recipes.get(name).get_measurements() for name in names]

    def get_recipe_ingredients(self):
        """
        Returns a 2D array containing all recipe ingredients.
        """
        names = self.get_recipe_names()
        return [self.recipes.get(name).get_ingredients() for name in names]

    def get_recipe_meal_types(self):
        """
        Returns a 2D array containing all recipe types.
        """
        names = self.get_recipe_names()
        return [self.recipes.get(name).get_meal_type() for name in names]

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

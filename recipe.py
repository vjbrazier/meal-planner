"""
The recipe class.
"""
# Standard Imports
import json

class Recipe:
    """
    Recipe class. Has the following attributes:
    """
    def __init__(self, name='', ingredients=None, measurements=None, instructions=None,
                 meal_type='', calories=0, protein=0, carbs=0, fat=0):
        # Sets defaults in a safe way
        if ingredients is None:
            ingredients = []
        if measurements is None:
            measurements = []
        if instructions is None:
            instructions = []

        self.name = name
        self.ingredients = ingredients
        self.measurements = measurements
        self.instructions = instructions
        self.meal_type = meal_type
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat

    def to_dict(self):
        """
        Returns the recipe as a dictionary.
        """
        return {
            'name': self.name,
            'ingredients': self.ingredients,
            'measurements': self.measurements,
            'instructions': self.instructions,
            'meal_type': self.meal_type,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat
        }


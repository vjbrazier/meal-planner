"""
This file handles identifying ingredients regardless of plurality (egg vs eggs).
It also handles a universal conversion (cups to oz or similar) for generating a shopping list. 
"""
# Standard imports
import ast
from collections import Counter

# Third party imports
from flask_socketio import emit

# Custom imports
from planner_logger import add_to_log
from core import socketio, lemmatizer

def name_conversion(unit):
    """
    Simplifies the name of the unit provided.
    """
    pound = ['lb', 'pound', 'pounds']
    ounce = ['oz', 'ounce', 'ounces']
    cup   = ['cup', 'cups']
    tbsp  = ['tbsp', 'tablespoon', 'tablespoons']
    tsp   = ['tsp', 'teaspoon', 'teaspoons']

    if unit in pound:
        return 'lb'

    if unit in ounce:
        return 'oz'

    if unit in cup:
        return 'cup'

    if unit in tbsp:
        return 'tbsp'

    if unit in tsp:
        return 'tsp'

    add_to_log(f'[WARN] It seems an invalid unit was provided: {unit}')

value_conversions = {
    'lb': 1,      # Conversion to pounds.
    'oz': 0.0625, # Conversion to pounds. Divide by 16.
    'cup': 8,     # Conversion to ounces. Multiply by 8.
    'tbsp': 0.5,  # Conversion to ounces. Divide by 2.
    'tsp': 0.1666 # Conversion to ounces. Divide by 6.
}

unit_conversions = {
    'lb': 'lb',
    'oz': 'lb',
    'cup': 'oz',
    'tbsp': 'oz',
    'tsp': 'oz'
}

def convert_unit(measurement, unit):
    """
    Converts the unit to its generalized version
    """
    unit = name_conversion(unit)
    new_measurement = round((measurement * value_conversions.get(unit)), 2)
    new_unit = unit_conversions.get(unit)

    return [new_measurement, new_unit]

def merge_ingredients(ingredients, measurements):
    """
    Merges ingredients that are the same.
    """
    for index, ingredient in enumerate(ingredients):
        if ingredient in ingredients[index + 1:]:
            second_index = ingredients.index(ingredient, index + 1)

            measurement1 = measurements[index]
            measurement2 = measurements[second_index]

            if not isinstance(measurement1, list):
                measurements[index] = measurement1 + measurement2
                ingredients.pop(second_index)
                measurements.pop(second_index)
            else:
                measurements[index][0] = measurement1[0] + measurement2[0]
                ingredients.pop(second_index)
                measurements.pop(second_index)

            break

@socketio.on('aggregate_ingredients')
def aggregate_ingredients(data=None, data_ingredients=None, data_measurements=None, skip_merge=False,
                          return_ingredients=False, return_measurements=False):
    """
    Lemmatizes the ingredients, and makes their measurements all normalized.
    """
    if data_ingredients is None:
        data_ingredients = data['ingredients']
        data_ingredients = ast.literal_eval(data_ingredients)

    if data_measurements is None:
        data_measurements = data['measurements']
        data_measurements = ast.literal_eval(data_measurements)

    ingredients = []
    measurements = []

    # Normalize all the data first
    for item1, item2 in zip(data_ingredients, data_measurements):
        item1 = item1.strip().lower()
        ingredients.append(item1)

        item2 = item2.strip().lower()
        measurements.append(item2)

    # Lemmatize all the ingredients
    ingredients = [lemmatizer.lemmatize(ingredient, pos='n') for ingredient in ingredients]

    # Split up the measurements appropriately
    split_measurements = []
    for measurement in measurements:
        if ' ' in measurement:
            split_measurements.append(measurement.split(' '))
        else :
            split_measurements.append(measurement)

    # Normalizes all measurements
    for index, item in enumerate(split_measurements):
        if isinstance(item, list):
            measurement = item[0]
            unit = item[1]

            split_measurements[index] = [convert_unit(float(measurement), unit)][0]
        else:
            split_measurements[index] = float(split_measurements[index])

    # print(ingredients)
    # print(split_measurements)

    if return_ingredients:
        return ingredients
    
    if return_measurements:
        return split_measurements

    if not skip_merge:
        counts = Counter(ingredients)
        duplicates = {item: count for item, count in counts.items() if count > 1}

        while duplicates:
            merge_ingredients(ingredients, split_measurements)
            counts = Counter(ingredients)
            duplicates = {item: count for item, count in counts.items() if count > 1}

        emit('append_ingredients', {'ingredients': ingredients, 'measurements': split_measurements, 'combined': False})

@socketio.on('combine_ingredients')
def combine_ingredients(data):
    """
    Combines two lists before aggregating them.
    """
    ingredients1 = data['ingredients1']
    ingredients2 = data['ingredients2']
    ingredients2 = ast.literal_eval(ingredients2)

    measurements1 = data['measurements1']
    measurements2 = data['measurements2']
    measurements2 = ast.literal_eval(measurements2)

    print(ingredients2)
    print(measurements2)

    ingredients = ingredients1 + ingredients2
    measurements = measurements1 + measurements2

    counts = Counter(ingredients)
    duplicates = {item: count for item, count in counts.items() if count > 1}

    while duplicates:
        merge_ingredients(ingredients, measurements)
        counts = Counter(ingredients)
        duplicates = {item: count for item, count in counts.items() if count > 1}
    
    # print(ingredients)
    # print(measurements)
    emit('append_ingredients', {'ingredients': ingredients, 'measurements': measurements, 'combined': True})

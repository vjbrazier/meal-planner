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

# Helper functions for the Socket listener
def clean_data(data):
    """
    Cleans data by stripping and lowering it.
    """
    return [item.strip().lower() for item in data]

def split_measurements(measurements):
    """
    Splits measurements from '1 tsp' to [1, 'tsp'] or similar.
    """
    split_measurements = []

    for measurement in measurements:
        if ' ' in measurement:
            split_measurements.append(measurement.split(' '))
        else:
            split_measurements.append(measurement)

    return split_measurements

def simplify_unit(unit):
    """
    Simplifies the name of the unit provided.
    """
    units = {
        'lb'  : ['lb', 'lbs', 'pound', 'pounds'],
        'oz'  : ['oz', 'ounce', 'ounces'],
        'cup' : ['cup', 'cups'],
        'tbsp': ['tbsp', 'tbsps', 'tablespoon', 'tablespoons'],
        'tsp' : ['tsp', 'tsps', 'teaspoon', 'teaspoons']
    }

    for simple_name, other_names in units.items():
        if unit in other_names:
            return simple_name

    add_to_log(f'[WARN] It seems an invalid unit was provided: {unit}')
    return unit

def convert_unit(measurement, unit):
    """
    Converts the unit's name and value.
    """
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

    unit = simplify_unit(unit)
    return [round(measurement * value_conversions.get(unit), 2), unit_conversions.get(unit)]

def normalize_measurements(measurements):
    """
    Normalizes measurements to a standardized unit.
    """
    normalized_measurements = []

    print(measurements)
    for item in measurements:
        # Check if it is '1' vs [1, 'tsp']
        if isinstance(item, list):
            measurement = item[0]
            unit = item[1]

            normalized_measurements.append(convert_unit(float(measurement), unit))
        else:
            normalized_measurements.append(float(item))

    return normalized_measurements

@socketio.on('aggregate_ingredients')
def aggregate_ingredients(data):
    """
    Lemmatizes the ingredients, and makes their measurements all normalized.
    """
    # Convert JS data passed into actual Python data
    data_ingredients  = data['ingredients']
    data_ingredients  = ast.literal_eval(data_ingredients)

    data_measurements = data['measurements']
    data_measurements = ast.literal_eval(data_measurements)

    # Put clean data into new arrays
    ingredients   = clean_data(data_ingredients)
    measurements = clean_data(data_measurements)

    # Lemmatizes all the ingredients
    ingredients = [lemmatizer.lemmatize(ingredient, pos='n') for ingredient in ingredients]

    # Split up the measurements
    measurements = split_measurements(measurements)

    # Normalize all the measurements
    measurements = normalize_measurements(measurements)

    # Emit the data back to JS.
    emit('append_ingredients', {
        'ingredients' : ingredients,
        'measurements': measurements,
        'modified'    : False
    })

# Merging and removal of existing ingredients
def ensure_list(data):
    """
    Prior to using ast, it confirms whether a string or list was passed.
    """
    if isinstance(data, str):
        return ast.literal_eval(data)
    return data

def correct_ingredients(ingredients, measurements, modification):
    """
    Merges ingredients that are the same.
    """
    for index, ingredient in enumerate(ingredients):
        if ingredient in ingredients[index + 1:]:
            second_index = ingredients.index(ingredient, index + 1)

            measurement1 = measurements[index]
            measurement2 = measurements[second_index]

            if not isinstance(measurement1, list):
                if modification == 'merge':
                    measurements[index] = measurement1 + measurement2
                else:
                    measurements[index] = measurement1 - measurement2

                ingredients.pop(second_index)
                measurements.pop(second_index)
            else:
                if modification == 'merge':
                    measurements[index][0] = measurement1[0] + measurement2[0]
                else:
                    measurements[index][0] = measurement1[0] - measurement2[0]

                ingredients.pop(second_index)
                measurements.pop(second_index)
            break

def remove_outliers(ingredients, measurements):
    """
    Removes outliers from float precision errors, such as 0.00000001 tsp.
    """
    indices = []

    for index, measurement in enumerate(measurements):
        # 1/8 tsp, the smallest, is 0.02173 oz roughly
        if isinstance(measurement, list):
            if measurement[0] < 0.021:
                indices.append(index)
        else:
            if measurement < 0.021:
                indices.append(index)

    # Goes through backwards to prevent index bound errors
    for index in reversed(indices):
        ingredients.pop(index)
        measurements.pop(index)

@socketio.on('modify_ingredients')
def modify_ingredients(data):
    """
    Modifies two lists before aggregating them.
    """
    # Gather and convert data as necessary
    ingredients1 = data['ingredients1']
    ingredients2 = data['ingredients2']

    measurements1 = data['measurements1']
    measurements2 = data['measurements2']

    ingredients1  = ensure_list(ingredients1)
    ingredients2  = ensure_list(ingredients2)
    measurements1 = ensure_list(measurements1)
    measurements2 = ensure_list(measurements2)

    modification = data['modification']

    # Remove is called from the clear button. This means the data stored is untouched, and needs to be
    if modification == 'remove':
        # Put clean data into new arrays
        ingredients2   = clean_data(ingredients2)
        measurements2 = clean_data(measurements2)

        # Lemmatizes all the ingredients
        ingredients2 = [lemmatizer.lemmatize(ingredient, pos='n') for ingredient in ingredients2]

        # Split up the measurements
        measurements2 = split_measurements(measurements2)

        # Normalize all the measurements
        measurements2 = normalize_measurements(measurements2)

    # Merge the lists of data
    ingredients = ingredients1 + ingredients2
    measurements = measurements1 + measurements2

    # This counter finds duplicates, as long as they exist, it will continue correcting
    counts = Counter(ingredients)
    duplicates = {item: count for item, count in counts.items() if count > 1}

    while duplicates:
        correct_ingredients(ingredients, measurements, modification)
        counts = Counter(ingredients)
        duplicates = {item: count for item, count in counts.items() if count > 1}

    # Removes outliers in the data
    remove_outliers(ingredients, measurements)

    emit('append_ingredients', {
        'ingredients': ingredients, 
        'measurements': measurements, 
        'modified': True
    })

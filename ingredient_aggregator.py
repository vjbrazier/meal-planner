"""
This file handles identifying ingredients regardless of plurality (egg vs eggs).
It also handles a universal conversion (cups to oz or similar) for generating a shopping list. 
"""
# Custom imports
from planner_logger import add_to_log
from core import lemmatizer

def name_conversion(unit):
    """
    Simplifies the name of the unit provided.
    """
    if unit is 'lb' or 'pound' or 'pounds':
        return 'lb'

    if unit is 'oz' or 'ounce' or 'ounces':
        return 'oz'

    if unit is 'cup' or 'cups':
        return 'cup'

    if unit is 'tbsp' or 'tablespoon' or 'tablespoons':
        return 'tbsp'

    if unit is 'tsp' or 'teaspoon' or 'teaspooons':
        return 'tsp'

    add_to_log(f'[WARN] It seems an invalid unit was provided: {unit}')

value_conversions = {
    'lb': 1,      # Conversion to pounds.
    'oz': 0.0625, # Conversion to pounds. Divide by 16.
    'cup': 8,     # Conversion to ounces. Multiply by 8.
    'tbsp': 0.5,  # Conversion to ounces. Divide by 2.
    'tsp': 0.1666 # Conversion to ounces. Divide by 6.
}

def convert_unit(measurement, unit):
    """
    Converts the unit to its generalized version
    """
    unit = name_conversion(unit)
    new_measurement = measurement * value_conversions.get(unit)

    return new_measurement



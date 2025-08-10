"""
Variables and objects shared across the site.
"""
# Standard Imports
from pathlib import Path
import os

# Third Party Imports
from flask import Flask
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# Custom Imports
from planner_logger import add_to_log

# Flask app
app = Flask(__name__)

# Lemmatizer
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

# Logs folder path
logs_folder_path = Path('logs/')

# Recipe data path
data_folder_path = Path('data/')
recipe_data_path = data_folder_path / Path('recipes.json')
recipe_image_path = Path('static/images/recipes')

# Create missing folders/files
if not os.path.exists(logs_folder_path):
    os.makedirs(logs_folder_path)
    add_to_log('[INFO] Created logs folder.')

if not os.path.exists(data_folder_path):
    os.makedirs(data_folder_path)
    add_to_log('[INFO] Created data folder.')

if not os.path.exists(recipe_image_path):
    os.makedirs(recipe_image_path)
    add_to_log('[INFO] Created recipe image folder.')

if not os.path.exists(recipe_data_path):
    with open(recipe_data_path, 'w', encoding='utf-8') as f:
        f.write('{}')

    add_to_log('[INFO] Created recipe data file.')

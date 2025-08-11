// Elements across the page \\
const socket = io();

// Recipe cards
const recipe_cards    = document.getElementsByClassName('recipe-card');
const recipe_names    = document.getElementsByClassName('recipe-name');
const selected_recipe = document.getElementById('selected-recipe');

// Weekday planning
const ingredient_list    = document.getElementById('ingredient-list');
const weekday_buttons    = document.getElementsByClassName('weekday-button');
const weekday_inner_text = document.getElementsByClassName('weekday-inner-text');
const weekday_clears     = document.getElementsByClassName('weekday-clear');
const weekday_multis     = document.getElementsByClassName('weekday-multi');
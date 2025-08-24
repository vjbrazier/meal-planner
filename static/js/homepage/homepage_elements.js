// Elements across the page \\
const socket = io();

// Searching and filters
const filters = document.getElementById('filters');
const filter_buttons = document.getElementsByClassName('filter-button');

// Recipe cards
const data_holders    = document.getElementsByClassName('data-holder');
const recipe_cards    = document.getElementsByClassName('recipe-card');
const recipe_links    = document.getElementsByClassName('recipe-link');
const recipe_names    = document.getElementsByClassName('recipe-name');
const selected_recipe = document.getElementById('selected-recipe');

// Weekday planning
const ingredient_div     = document.getElementById('ingredient-div');
const ingredient_list    = document.getElementById('ingredient-list');
const placeholders       = document.getElementsByClassName('weekday-placeholder');
const planned_meals      = document.getElementsByClassName('planned-meals');
const add_meals          = document.getElementsByClassName('add-meals');
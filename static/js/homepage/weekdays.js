// Handles the weekdays functions \\
// Variables
let adding_meal = false;
let recipe_to_spread = '';
let spreading_meal = false;
let selected_weekday = null;

// Resets all of the add meal buttons and associated variables
function reset_meal_adding() {
    selected_weekday = null;
    adding_meal = false;

    for (let i = 0; i < add_meals.length; i++) {
        add_meals[i].innerText = '+ Add Meal +';
    }
}

// Adds the ability to toggle adding meals to each button
for (let i = 0; i < add_meals.length; i++) {    
    add_meals[i].addEventListener('click', () => {
        // A quick ternary to find the state
        let currently_selected  = add_meals[i].innerText == '+ Add Meal +' ? false : true;
        
        // If you are spreading a meal, it needs to go through differently
        if (spreading_meal) {
            selected_weekday = i;
            create_planned_meal(i, true);
        } else {
            // Sets variables according to ternary above
            if (!currently_selected) {
                reset_meal_adding();
                add_meals[i].innerText = 'Select a meal above!';
                adding_meal = true;
                selected_weekday = i;
            } else {
                add_meals[i].innerText = '+ Add Meal +';
                adding_meal = false;
                selected_weekday = null;
            }
        }
    })
}

// Checks each weekday to determine if the placeholder text is needed
function check_for_planned_meals() {
    for (let i = 0; i < planned_meals.length; i++) {
        if (planned_meals[i].children.length == 0) {
            placeholders[i].classList.add('visible');
        } else {
            placeholders[i].classList.remove('visible');
        }
    }
}

// Checks if spreading is currently enabled or not
function check_for_spreading(current_button) {
    let spread_buttons = document.getElementsByClassName('spread-button');

    for (let i = 0; i < spread_buttons.length; i++) {
        if ((spread_buttons[i].innerText == 'Spreading') && (spread_buttons[i] != current_button)) {
            return true;
        }
    }

    return false;
}

// Adds an event listener to the spread button provided
function create_spread_function(spread_button) {
    spread_button.addEventListener('click', () => {
        // Gets the buttons at the start, to account for any additions/removals
        let recipe_buttons = document.getElementsByClassName('recipe-button');
        let spread_buttons = document.getElementsByClassName('spread-button');
        
        for (let i = 0; i < spread_buttons.length; i++) {
            if (spread_buttons[i] == spread_button) {
                // "Other recipe" refers to if another recipe is being spread
                let other_recipe_spreading   = check_for_spreading(spread_button);
                
                // So long as one isn't, the current can begin spreading
                if (!other_recipe_spreading) {
                    // A quick ternary to find the state
                    let current_recipe_spreading = spread_buttons[i].innerText == 'Spread' ? false : true;
                    
                    // Disables spreading an already spread recipe
                    if (spread_button.innerText != 'Already Spread') {
                        // Mostly setting variables based on above
                        if (!current_recipe_spreading) {
                            reset_meal_adding();

                            // Updates add meal buttons, to make it more clear to the user
                            for (let k = 0; k < add_meals.length; k++) {
                                add_meals[k].innerText = 'Spread Recipe Here';
                            }

                            spread_button.innerText = 'Spreading';
                            recipe_to_spread = recipe_buttons[i].innerText.toLowerCase().replaceAll(' ', '-');
                            spreading_meal = true;
                        } else {
                            reset_meal_adding();
                            spread_button.innerText = 'Spread';
                            recipe_to_spread = '';
                            spreading_meal = false;
                        }
                    }
                } else { // Gives a quick popup to alert the user they are spreading another recipe
                    let warning_text = document.getElementById('spread-warning');

                    warning_text.classList.add('visible');
                    setTimeout(() => {
                        warning_text.classList.remove('visible');
                    }, 1000);
                }
            }
        }
    })
}

// Creates the three buttons that make up a planned meal
function create_planned_meal(index, spread_meal) {
    // The recipe button, has the name and some data attached
    let recipe_button = document.createElement('button');
    // Where the data comes from depends on whether or not it is spread
    if (spread_meal) {
        let data_holder = document.getElementById(recipe_to_spread);

        recipe_button.setAttribute('data-measurements', data_holder.getAttribute('data-measurements'));
        recipe_button.setAttribute('data-ingredients', data_holder.getAttribute('data-ingredients'));
        recipe_button.innerText = recipe_to_spread.replaceAll('-', ' ').replace(/\b\w/g, char => char.toUpperCase());
    } else {
        recipe_button.setAttribute('data-measurements', data_holders[index].getAttribute('data-measurements'));
        recipe_button.setAttribute('data-ingredients', data_holders[index].getAttribute('data-ingredients'));
        recipe_button.innerText = recipe_names[index].innerText;
    }
    recipe_button.classList.add('recipe-button')
    
    // The spread button, its functions are complex and go through another function
    let spread_button = document.createElement('button');
    // Determines inside text
    if (spread_meal) {
        spread_button.innerText = 'Already Spread';
    } else {
        spread_button.innerText = 'Spread';
    }
    spread_button.classList.add('spread-button');
    create_spread_function(spread_button)
    
    // The clear button. Has code that provides deleting functionality
    let clear_button = document.createElement('button');
    clear_button.innerText = 'X';
    clear_button.classList.add('clear-button')
    // Determines its data attribute
    if (spread_meal) {
        clear_button.setAttribute('data-spread', 'spread');
    }

    clear_button.addEventListener('click', () => {
        // Gets upon click to account for additions/deletions
        let recipe_buttons = Array.from(document.getElementsByClassName('recipe-button'));
        let spread_buttons = Array.from(document.getElementsByClassName('spread-button'));
        let clear_buttons  = Array.from(document.getElementsByClassName('clear-button'));
        
        for (let i = 0; i < clear_buttons.length; i++) {
            if (clear_buttons[i] == clear_button) {
                let outer_spread = clear_buttons[i].getAttribute('data-spread');
                
                // Iterates through other planned recipes, and deletes spread ones that match
                for (let j = 0; j < recipe_buttons.length; j++) {
                    let inner_spread = clear_buttons[j].getAttribute('data-spread');

                    if ((inner_spread == 'spread') && (recipe_buttons[i].innerText == recipe_buttons[i].innerText)) {
                        recipe_buttons[j].remove();
                        spread_buttons[j].remove();
                        clear_buttons[j].remove();

                        check_for_planned_meals();
                    }
                }

                recipe_buttons[i].remove();
                spread_buttons[i].remove();
                clear_buttons[i].remove();
                
                check_for_planned_meals()

                // Only removes ingredients from the original, and not spread recipes to prevent negatives
                if (outer_spread != 'spread') {
                    let removed_ingredients  = recipe_buttons[i].getAttribute('data-ingredients');
                    let removed_measurements = recipe_buttons[i].getAttribute('data-measurements');

                    let attached_ingredients  = JSON.parse(ingredient_list.getAttribute('data-ingredients'));
                    let attached_measurements = JSON.parse(ingredient_list.getAttribute('data-measurements'));

                    socket.emit('modify_ingredients', {
                                    'ingredients1' : attached_ingredients,  'ingredients2' : removed_ingredients,
                                    'measurements1': attached_measurements, 'measurements2': removed_measurements,
                                    'modification': 'remove',
        })
                }
            }
        }
    })
    
    // Only adds ingredients if this is the original, and not a spread meal
    if (!spread_meal) {
        socket.emit('aggregate_ingredients', data={
            ingredients:  recipe_button.getAttribute('data-ingredients'),
            measurements: recipe_button.getAttribute('data-measurements')
        });
    }

    planned_meals[selected_weekday].appendChild(recipe_button);
    planned_meals[selected_weekday].appendChild(spread_button);
    planned_meals[selected_weekday].appendChild(clear_button)
    check_for_planned_meals();
}

// Appends a recipe to a weekday
for (let i = 0; i < recipe_links.length; i++) {
    recipe_links[i].addEventListener('click', (event) => {
        if (adding_meal) {
            // Prevents redirection to recipe page
            event.preventDefault();

            create_planned_meal(i, false);
        }
    })
}
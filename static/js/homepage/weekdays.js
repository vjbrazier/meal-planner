// Handles the weekdays functions \\
// Variables
let adding_meal = false;
let recipe_to_spread = '';
let spreading_meal = false;
let selected_weekday = null;

function reset_meal_adding() {
    selected_weekday = null;
    adding_meal = false;

    for (let i = 0; i < add_meals.length; i++) {
        add_meals[i].innerText = '+ Add Meal +';
    }
}

for (let i = 0; i < add_meals.length; i++) {    
    add_meals[i].addEventListener('click', () => {
        let currently_selected  = add_meals[i].innerText == '+ Add Meal +' ? false : true;
        
        if (spreading_meal) {
            selected_weekday = i;
            create_planned_meal(i, true);
        } else {
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

function check_for_planned_meals() {
    for (let i = 0; i < planned_meals.length; i++) {
        if (planned_meals[i].children.length == 0) {
            placeholders[i].classList.add('visible');
        } else {
            placeholders[i].classList.remove('visible');
        }
    }
}

function check_for_spreading(current_button) {
    let spread_buttons = document.getElementsByClassName('spread-button');

    for (let i = 0; i < spread_buttons.length; i++) {
        if ((spread_buttons[i].innerText == 'Spreading') && (spread_buttons[i] != current_button)) {
            return true;
        }
    }

    return false;
}

function create_spread_function(spread_button) {
    spread_button.addEventListener('click', () => {
        let recipe_buttons = document.getElementsByClassName('recipe-button');
        let spread_buttons = document.getElementsByClassName('spread-button');
        
        for (let i = 0; i < spread_buttons.length; i++) {
            if (spread_buttons[i] == spread_button) {
                let other_recipe_spreading   = check_for_spreading(spread_button);
                
                if (!other_recipe_spreading) {
                    let current_recipe_spreading = spread_buttons[i].innerText == 'Spread' ? false : true;
                    
                    if (spread_button.innerText != 'Already Spread') {
                        if (!current_recipe_spreading) {
                            reset_meal_adding();

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
                } else {
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

function create_planned_meal(index, spread_meal) {
    let recipe_button = document.createElement('button');
    
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
    
    let spread_button = document.createElement('button');
    if (spread_meal) {
        spread_button.innerText = 'Already Spread';
    } else {
        spread_button.innerText = 'Spread';
    }
    spread_button.classList.add('spread-button');
    
    create_spread_function(spread_button)
    
    let clear_button = document.createElement('button');
    clear_button.innerText = 'X';
    clear_button.classList.add('clear-button')
    if (spread_meal) {
        clear_button.setAttribute('data-spread', 'spread');
    }

    clear_button.addEventListener('click', () => {
        let recipe_buttons = Array.from(document.getElementsByClassName('recipe-button'));
        let spread_buttons = Array.from(document.getElementsByClassName('spread-button'));
        let clear_buttons  = Array.from(document.getElementsByClassName('clear-button'));
        
        for (let j = 0; j < clear_buttons.length; j++) {
            if (clear_buttons[j] == clear_button) {
                let outer_spread = clear_buttons[j].getAttribute('data-spread');
                
                for (let k = 0; k < recipe_buttons.length; k++) {
                    let inner_spread = clear_buttons[k].getAttribute('data-spread');

                    if ((inner_spread == 'spread') && (recipe_buttons[j].innerText == recipe_buttons[k].innerText)) {
                        recipe_buttons[k].remove();
                        spread_buttons[k].remove();
                        clear_buttons[k].remove();

                        check_for_planned_meals();
                    }
                }

                recipe_buttons[j].remove();
                spread_buttons[j].remove();
                clear_buttons[j].remove();
                
                check_for_planned_meals()

                if (outer_spread != 'spread') {
                    console.log('delete');
                }
            }
        }
    })
    
    if (spread_meal) {
        console.log('spread');
    } else {
        console.log('not spread');
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
            event.preventDefault();

            create_planned_meal(i, false);
        }
    })
}
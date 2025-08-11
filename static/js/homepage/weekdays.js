// Handles the weekdays functions \\
// Variables
let multi_selection = false;
let recipe_selected = null;
let weekday_selected = [false, false, false, false, false, false, false]

// Checks for if cursor is over a weekday button.
for (let i = 0; i < weekday_buttons.length; i++) {
    weekday_buttons[i].addEventListener('click', () => {
        if (multi_selection) {
            recipe_info = document.getElementById(recipe_selected.toLowerCase());

            weekday_buttons[i].style.backgroundImage = `url(${recipe_info.getAttribute('data-image')})`;
            weekday_buttons[i].style.backgroundColor = 'var(--button-hover-color)';
            weekday_inner_text[i].classList.add('visible');
            weekday_multis[i].classList.add('visible');
            weekday_inner_text[i].innerText = `${recipe_selected}`;
        }
    })

    weekday_buttons[i].addEventListener(('mouseover'), () => {
        weekday_selected[i] = true;
    })

    weekday_buttons[i].addEventListener(('mouseout'), () => {
        weekday_selected[i] = false;
    })
}

// Clears the data inside the weekday
for (let i = 0; i < weekday_clears.length; i++) {
    weekday_clears[i].addEventListener('click', () => {
        weekday_buttons[i].style.backgroundColor = 'var(--button-background-color)';
        weekday_buttons[i].style.backgroundImage = 'none';
        weekday_inner_text[i].innerText = '';
        weekday_inner_text[i].classList.remove('visible');
        weekday_multis[i].classList.remove('visible');
    })
}

// Allows you to make a recipe apply to multiple days without doubling ingredients
// Allows you to set multiple days for one recipe
for (let i = 0; i < weekday_multis.length; i++) {
    weekday_multis[i].addEventListener('click', () => {
        if (weekday_multis[i].classList.contains('visible')) {
            for (let j = 0; j < weekday_multis.length; j++) {
                if (weekday_multis[j].innerText.includes('Disabled')) {
                    weekday_multis[j].innerText = 'Spread out recipe: Enabled';
                } else {
                    weekday_multis[j].innerText = 'Spread out recipe: Disabled';
                }
            }

            multi_selection = !multi_selection
            recipe_selected = weekday_inner_text[i].innerText;
        }
    })
}
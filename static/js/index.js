// Variables and page elements \\
const recipe_cards = document.getElementsByClassName('recipe-link');
const recipe_names = document.getElementsByClassName('recipe-name');
const selected_recipe = document.getElementById('selected-recipe');
const weekdays = document.getElementsByClassName('weekday');
const weekdays_inner_text = document.getElementsByClassName('weekday-inner-text');

let selected = false;
let selectedIndex = null;
let weekday_selected = [false, false, false, false, false, false, false]

// Sets images using the path put into the data-image tag
for (let i = 0; i < recipe_cards.length; i++) {
    let image = recipe_cards[i].getAttribute('data-image');
    recipe_cards[i].style.backgroundImage = `url("${image}")`;
}

// Moving recipes into the weekdays \\
// Adds the hovering functionality to each recipe card
for (let i = 0; i < recipe_cards.length; i++) {
    recipe_cards[i].addEventListener('mousedown', (event) => {
        event.preventDefault();
        selected = true;
        selectedIndex = i;

        // Slight delay makes it more smooth looking
        setTimeout((() => {
            selected_recipe.classList.add('visible');
        }), 100)

        selected_recipe.innerText = recipe_names[i].innerText;
        selected_recipe.setAttribute('data-measurements', recipe_cards[i].getAttribute('data-measurements'))
        selected_recipe.setAttribute('data-ingredients', recipe_cards[i].getAttribute('data-ingredients'))
        selected_recipe.setAttribute('data-meal-type', recipe_cards[i].getAttribute('data-meal-type'))
        selected_recipe.setAttribute('data-image', recipe_cards[i].getAttribute('data-image'))
    })
}

// Moves selector with cursor as it moves
document.addEventListener('mousemove', (event) => {
    if (selected && selectedIndex !== null) {
        const mouse_x = event.clientX;
        const mouse_y = event.clientY;
        let width = selected_recipe.offsetWidth;

        selected_recipe.style.left = `${mouse_x - (width / 2)}px`;
        selected_recipe.style.top =  `${mouse_y - 32}px`;
    }
})

// Checks for if cursor is over a weekday button.
for (let i = 0; i < weekdays.length; i++) {
    weekdays[i].addEventListener(('mouseover'), () => {
        weekday_selected[i] = true;
    })

    weekdays[i].addEventListener(('mouseout'), () => {
        weekday_selected[i] = false;
    })
}

document.addEventListener('mouseup', () => {
    for (let i = 0; i < weekday_selected.length; i++) {
        if (weekday_selected[i] == true) {
            weekdays[i].style.backgroundImage = `url(${selected_recipe.getAttribute('data-image')})`;
            weekdays[i].style.backgroundColor = 'var(--button-hover-color)';
            weekdays_inner_text[i].innerText = `${selected_recipe.innerText}`;
        }
    }

    selected = false;
    selectedIndex = null;
    selected_recipe.classList.remove('visible');
})
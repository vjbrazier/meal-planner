// Page Elements and Variables \\
const recipe_cards = document.getElementsByClassName('recipe-card');
const recipe_names = document.getElementsByClassName('recipe-name');
const selected_recipe = document.getElementById('selected-recipe');
const weekday_buttons = document.getElementsByClassName('weekday-button');
const weekdays_inner_text = document.getElementsByClassName('weekday-inner-text');

let selected = false;
let selectedIndex = null;
let weekday_selected = [false, false, false, false, false, false, false]

// // Sets images using the path put into the data-image tag
for (let i = 0; i < recipe_cards.length; i++) {
    let image = recipe_cards[i].getAttribute('data-image');
    let recipe_href = recipe_cards[i].getAttribute('data-href');

    recipe_cards[i].style.backgroundImage = `url("${image}")`;
    recipe_cards[i].addEventListener('click', () => {
        window.location.href = recipe_href;
    })
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
for (let i = 0; i < weekday_buttons.length; i++) {
    weekday_buttons[i].addEventListener(('mouseover'), () => {
        weekday_selected[i] = true;
    })

    weekday_buttons[i].addEventListener(('mouseout'), () => {
        weekday_selected[i] = false;
    })
}

document.addEventListener('mouseup', () => {
    for (let i = 0; i < weekday_selected.length; i++) {
        if (weekday_selected[i] == true) {
            let recipe = selected_recipe.innerText.toLowerCase();
            let current_recipe_info = document.getElementById(recipe);

            weekday_buttons[i].style.backgroundImage = `url(${current_recipe_info.getAttribute('data-image')})`;
            weekday_buttons[i].style.backgroundColor = 'var(--button-hover-color)';
            weekdays_inner_text[i].classList.add('visible');
            weekdays_inner_text[i].innerText = `${selected_recipe.innerText}`;
        }
    }

    selected = false;
    selectedIndex = null;
    selected_recipe.classList.remove('visible');
})
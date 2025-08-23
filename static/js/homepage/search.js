// The search bar, and filters \\
// Variables
let filtered = [];

// Updates the filter on all recipe cards
function update_filter() {
    if (filtered.length === 0) {
        for (let i = 0; i < recipe_cards.length; i++) {
            recipe_cards[i].classList.remove('hidden');
        }

        return;
    }

    for (let i = 0; i < recipe_cards.length; i++) {
        recipe_cards[i].classList.add('hidden');
    }

    for (let i = 0; i < filtered.length; i++) {
        for (let j = 0; j < recipe_cards.length; j++) {
            if (data_holders[j].getAttribute('data-meal-type').toLowerCase() == filtered[i]) {
                recipe_cards[j].classList.remove('hidden');
            }
        }
    }   
}

// Enables and disables filters on click.
for (let i = 0; i < filter_buttons.length; i++) {
    filter_buttons[i].addEventListener('click', () => {
        meal_filter = filter_buttons[i].innerText.toLowerCase();
        
        if (filters.classList.contains('visible')) {
            if (filter_buttons[i].classList.contains('enabled')) {
                filter_buttons[i].classList.remove('enabled');
                filtered.splice(filtered.indexOf(meal_filter), 1);
                update_filter();
            }
    
            else {
                filter_buttons[i].classList.add('enabled');
                filtered.push(meal_filter);
                update_filter();
            }
        }
    })
}

// Updates what is visible based on what is currently typed
function search_meals(search) {
    if (search == '') {
        for (let i = 0; i < recipe_cards.length; i++) {
            recipe_cards[i].classList.remove('hidden');
        }

        return;
    }

    for (let i = 0; i < data_holders.length; i++) {
        if (data_holders[i].id.toLowerCase().includes(search)) {
            recipe_cards[i].classList.remove('hidden');
        } else {
            recipe_cards[i].classList.add('hidden');
        }

    }
}

document.getElementById('search-bar').addEventListener('input', (e) => {
    const search = e.target.value.toLowerCase();

    search_meals(search);
})
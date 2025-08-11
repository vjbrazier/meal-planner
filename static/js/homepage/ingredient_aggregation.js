// Compiles ingredients into a summed list \\
// Variables

// Updates the inner text of the ingredient list
function update_list() {
    ingredient_list.innerText = 'Ingredients required: ';
    
    let attached_ingredients = JSON.parse(ingredient_list.getAttribute('data-ingredients'));
    let attached_measurements = JSON.parse(ingredient_list.getAttribute('data-measurements'));

    for (let i = 0; i < attached_ingredients.length; i++) {
        if (Array.isArray(attached_measurements[i])) {
            attached_measurements[i] = `${attached_measurements[i][0].toFixed(2)} ${attached_measurements[i][1]}`
        }
        
        if (i != attached_ingredients.length - 1) {
            ingredient_list.innerText += ` ${attached_measurements[i]} ${attached_ingredients[i]}, `;
        } else {
            ingredient_list.innerText += ` ${attached_measurements[i]} ${attached_ingredients[i]}`;
        }
    }
}

// When a recipe is added to the week, its aggregated data comes back through here.
socket.on('append_ingredients', (data) => {
    if (data.combined) {
        ingredient_list.setAttribute('data-ingredients', JSON.stringify(data.ingredients));
        ingredient_list.setAttribute('data-measurements', JSON.stringify(data.measurements));
        update_list();
        return;
    }

    let attached_ingredients = ingredient_list.getAttribute('data-ingredients');
    let attached_measurements = ingredient_list.getAttribute('data-measurements');
    
    let data_ingredients = data.ingredients;
    let data_measurements = data.measurements;


    if ((attached_ingredients == '') || (attached_measurements == '')) {
        ingredient_list.setAttribute('data-ingredients', JSON.stringify(data_ingredients));
        ingredient_list.setAttribute('data-measurements', JSON.stringify(data_measurements));
        update_list();
    } else {
        socket.emit('combine_ingredients', {
            'ingredients1': data_ingredients, 'ingredients2': attached_ingredients,
            'measurements1': data_measurements, 'measurements2': attached_measurements
        })
    }
})
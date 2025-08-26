// Compiles ingredients into a checklist \\
// Variables

// Adds items to the ingredient list
function update_list() {
    let attached_ingredients  = JSON.parse(ingredient_list.getAttribute('data-ingredients'));
    let attached_measurements = JSON.parse(ingredient_list.getAttribute('data-measurements'));

    if ((attached_ingredients  != '') && (attached_measurements != '')) {
        ingredient_div.classList.add('visible');
        ingredient_list.innerHTML = '';
        for (let i = 0; i < attached_ingredients.length; i++) {
            if (Array.isArray(attached_measurements[i])) {
                attached_measurements[i] = `${attached_measurements[i][0].toFixed(2)} ${attached_measurements[i][1]}`;
            }

            let input = document.createElement('input');
            input.type = 'checkbox';
            input.id = 'ingredient' + i;

            let label = document.createElement('label')
            label.innerText = `${attached_measurements[i]} ${attached_ingredients[i]}`

            ingredient_list.appendChild(input);
            ingredient_list.appendChild(label);
        }
    } else {
        ingredient_div.classList.remove('visible');
    }
}

// When a recipe is added to the week, its aggregated data comes back through here.
socket.on('append_ingredients', (data) => {
    if (data.modified) {
        ingredient_list.setAttribute('data-ingredients',  JSON.stringify(data.ingredients));
        ingredient_list.setAttribute('data-measurements', JSON.stringify(data.measurements));
        update_list();
        return;
    }

    let data_ingredients  = data.ingredients;
    let data_measurements = data.measurements;

    let attached_ingredients  = ingredient_list.getAttribute('data-ingredients');
    let attached_measurements = ingredient_list.getAttribute('data-measurements');

    if ((attached_ingredients === '') || (attached_measurements === '')) {
        ingredient_list.setAttribute('data-ingredients',  JSON.stringify(data_ingredients));
        ingredient_list.setAttribute('data-measurements', JSON.stringify(data_measurements));
        update_list();
    } else {
        socket.emit('modify_ingredients', {
            'ingredients1' : data_ingredients,  'ingredients2' : attached_ingredients,
            'measurements1': data_measurements, 'measurements2': attached_measurements,
            'modification': 'merge',
        })
    }
})
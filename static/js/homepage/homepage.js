// Functions that utilize multiple parts of the page are in here \\
// Sets styles of filters on page start
document.addEventListener('DOMContentLoaded', () => {
    let subs = document.getElementsByClassName('filter-subcategory');
    let sub_count = subs.length;

    document.getElementById('filters').style.gridTemplateColumns = `repeat(${sub_count}, auto)`
})

// Visbility of filters
document.getElementById('filter-opener').addEventListener('click', () => {
    let filters = document.getElementById('filters');
    
    filters.classList.toggle('visible');
})

// RECIPE_CATALOG + WEEKDAYS combination \\
// Updates the weekday once you stop holding click
// document.addEventListener('mouseup', () => {
//     for (let i = 0; i < weekday_selected.length; i++) {
//         if ((weekday_selected[i] == true) && (selected == true)) {
//             let recipe = selected_recipe.innerText.toLowerCase();
//             let current_recipe_info = document.getElementById(recipe);

//             socket.emit('aggregate_ingredients', data={
//                 ingredients: current_recipe_info.getAttribute('data-ingredients'),
//                 measurements: current_recipe_info.getAttribute('data-measurements')
//             });

//             weekday_buttons[i].style.backgroundImage = `url(${current_recipe_info.getAttribute('data-image')})`;
//             weekday_buttons[i].style.backgroundColor = 'var(--button-hover-color)';
//             weekday_inner_text[i].classList.add('visible');
//             weekday_multis[i].classList.add('visible');
//             weekday_inner_text[i].innerText = `${selected_recipe.innerText}`;
//         }
//     }

//     selected = false;
//     selectedIndex = null; 
//     selected_recipe.classList.remove('visible');
// })
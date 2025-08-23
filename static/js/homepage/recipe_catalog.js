// Handles the recipe catalog's functions \\
// Variables
let selected = false;
let selectedIndex = null;

// Sets images using the path put into the data-image tag
// for (let i = 0; i < recipe_cards.length; i++) {
//     let image = recipe_cards[i].getAttribute('data-image');
//     let recipe_href = recipe_cards[i].getAttribute('data-href');

//     recipe_cards[i].style.backgroundImage = `url("${image}")`;
//     recipe_cards[i].addEventListener('click', () => {
//         window.location.href = recipe_href;
    // })
// }

// // Adds the hovering functionality to each recipe card
// for (let i = 0; i < recipe_cards.length; i++) {
//     recipe_cards[i].addEventListener('mousedown', (event) => {
//         event.preventDefault();
//         selected = true;
//         selectedIndex = i;

//         // Slight delay makes it more smooth looking
//         setTimeout((() => {
//             selected_recipe.classList.add('visible');
//         }), 100)

//         selected_recipe.innerText = recipe_names[i].innerText;
//     })
// }

// // Moves selector with cursor as it moves
// document.addEventListener('mousemove', (event) => {
//     if (selected && selectedIndex !== null) {
//         const mouse_x = event.clientX;
//         const mouse_y = event.clientY;
//         let width = selected_recipe.offsetWidth;

//         selected_recipe.style.left = `${mouse_x - (width / 2)}px`;
//         selected_recipe.style.top =  `${mouse_y - 32}px`;
//     }
// })
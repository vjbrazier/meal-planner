const recipe_cards = document.getElementsByClassName('recipe-link');

for (let i = 0; i < recipe_cards.length; i++) {
    let image = recipe_cards[i].getAttribute('data-image');

    console.log(image);
    console.log(recipe_cards[i])

    recipe_cards[i].style.backgroundImage = `url("${image}")`;
}
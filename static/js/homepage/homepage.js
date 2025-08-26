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

// Delete functionality
for (let i = 0; i < delete_recipes.length; i++) {
    delete_recipes[i].addEventListener('click', () => {
        let recipe = data_holders[i].id.replaceAll('-', ' ');

        socket.emit('delete-recipe', data={
            recipe: recipe
        });
    })
}

// Refreshes the page to update the recipe cards upon deletion
socket.on('recipe-deleted', () => {
    window.location.reload();
})
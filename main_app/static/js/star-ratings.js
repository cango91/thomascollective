window.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.star-rating:not(.star-rating-editable)');
    for (let i = 0; i < elements.length; i++) {
        const rating = Number(elements[i].textContent);
        if (rating > 0) {
            let halfStarIdx=-1;
            if (parseInt(rating) !== rating) {
                halfStarIdx = Math.ceil(rating);
            }
                elements[i].textContent = "";
                for (let j = 0; j < 5; j++) {
                    if(j+1===halfStarIdx){
                        elements[i].innerHTML += `<span class="material-icons">star_half</span>`;
                        continue;
                    }
                    elements[i].innerHTML += `<span class="material-icons">${rating < j + 1 ? 'star_border' : 'star'}</span>`;
                }
            elements[i].title = parseInt(rating) === rating ? rating : rating.toFixed(1);
        } else {
            elements[i].textContent = 'No Rating.';
            elements[i].title = 'Not rated';
        }
    }
});

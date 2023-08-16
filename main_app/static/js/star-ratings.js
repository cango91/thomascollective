window.addEventListener('DOMContentLoaded', () => {
    // We select all elements with class 'star-rating' that don't have 'star-rating-editable' class
    const elements = document.querySelectorAll('.star-rating:not(.star-rating-editable)');
    for (let i = 0; i < elements.length; i++) {
        // we get the numeric rating from the elements content
        const rating = Number(elements[i].textContent);
        // if there is a rating:
        if (rating > 0) {
            let halfStarIdx = -1;
            // we check to see if rating  is an integer or float
            if (parseInt(rating) !== rating) {
                // if it's a float, we find out which star should be half-filled
                halfStarIdx = Math.ceil(rating);
            }
            elements[i].textContent = "";
            // adding the stars
            for (let j = 0; j < 5; j++) {
                if (j + 1 === halfStarIdx) {
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
    // We select all elements with both classes: star-rating and star-rating-editable
    // (even though our forms will only have one, this way we're not constrained by that)
    const inputs = document.querySelectorAll('.star-rating.star-rating-editable');
    for (let i = 0; i < inputs.length; i++) {
        const ratingInput = inputs[i];
        // hide the original number field
        ratingInput.type = 'hidden';
        // create the container to house the stars
        const container = document.createElement('span');
        container.className = 'star-container left';
        const initialRating = ratingInput.value || -1;
        for (let j = 5; j > 0; j--) {
            const star = document.createElement('span');
            star.className = 'material-icons star';
            // each star span element gets a data-rating attribute
            star.dataset.rating = j;
            if(initialRating >= j) star.classList.add('star-filled');
            container.appendChild(star);
        }

        ratingInput.parentNode.appendChild(container);

        container.addEventListener('click', (evt) => {
            if (!evt.target.dataset.rating) return;
            // When a star is clicked we set value of the input we hid (the actual form input Django uses in POST)
            ratingInput.value = Number(evt.target.dataset.rating);
            const stars = evt.target.closest('.star-container').querySelectorAll('.star');
            const currentRating = ratingInput.value || -1;
            for (let j = 0; j < 5; j++) {
                if (currentRating >= Number(stars[j].dataset.rating)) {
                    stars[j].classList.add('star-filled');
                } else {
                    stars[j].classList.remove('star-filled');
                }
            }
        });

        container.addEventListener('mouseenter', evt => {
            container.classList.add('editing');
        });

        container.addEventListener('mouseleave', evt => {
            container.classList.remove('editing');
        });
    }


});

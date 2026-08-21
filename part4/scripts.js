document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
        });
    }

    const placesList = document.getElementById('places-list');

    if (placesList) {
        checkAuthentication();

        const priceFilter = document.getElementById('price-filter');

        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                filterPlaces(event.target.value);
            });
        }
    }
});


async function loginUser(email, password) {
    const errorMessage = document.getElementById('login-error');

    try {
        const response = await fetch(
            'http://127.0.0.1:5000/api/v1/auth/login',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );

        const data = await response.json();

        if (response.ok) {
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            errorMessage.textContent =
                data.error || 'Invalid email or password.';
        }
    } catch (error) {
        console.error(error);
        errorMessage.textContent =
            'Unable to connect to the server.';
    }
}


function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }

    return null;
}


function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        if (token) {
            loginLink.style.display = 'none';
        } else {
            loginLink.style.display = 'block';
        }
    }

    fetchPlaces(token);
}


async function fetchPlaces(token) {
    const headers = {};

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(
            'http://127.0.0.1:5000/api/v1/places/',
            {
                method: 'GET',
                headers: headers
            }
        );

        if (!response.ok) {
            throw new Error('Failed to fetch places');
        }

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error(error);

        const placesList = document.getElementById('places-list');

        if (placesList) {
            placesList.innerHTML =
                '<p>Unable to load places.</p>';
        }
    }
}


function displayPlaces(places) {
    const placesList = document.getElementById('places-list');

    placesList.innerHTML = '';

    if (places.length === 0) {
        placesList.innerHTML = '<p>No places available.</p>';
        return;
    }

    places.forEach((place) => {
        const card = document.createElement('article');

        card.className = 'place-card';
        card.dataset.price = place.price;

        const title = place.title || place.name || 'Unnamed Place';
        const description = place.description || 'No description available.';

        card.innerHTML = `
            <h2>${title}</h2>
            <p>${description}</p>
            <p><strong>Price per night:</strong> $${place.price}</p>
            <a href="place.html?id=${place.id}" class="details-button">
                View Details
            </a>
        `;

        placesList.appendChild(card);
    });
}


function filterPlaces(selectedPrice) {
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach((card) => {
        const price = Number(card.dataset.price);

        if (selectedPrice === 'all') {
            card.style.display = 'block';
        } else if (price <= Number(selectedPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}


/* Task 3 - Place details */

document.addEventListener('DOMContentLoaded', () => {
    const placeDetails = document.getElementById('place-details');

    if (!placeDetails) {
        return;
    }

    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');

    updatePlaceAuthentication(token, placeId);

    if (!placeId) {
        placeDetails.innerHTML = '<p>Place not found.</p>';
        return;
    }

    fetchPlaceDetails(token, placeId);
});


function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);

    return params.get('id');
}


function updatePlaceAuthentication(token, placeId) {
    const loginLink = document.getElementById('login-link');
    const addReview = document.getElementById('add-review');
    const addReviewLink = document.getElementById('add-review-link');

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    if (addReview) {
        addReview.style.display = token ? 'block' : 'none';
    }

    if (token && addReviewLink && placeId) {
        addReviewLink.href =
            `add_review.html?place_id=${placeId}`;
    }
}


async function fetchPlaceDetails(token, placeId) {
    const headers = {};

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(
            `http://127.0.0.1:5000/api/v1/places/${placeId}`,
            {
                method: 'GET',
                headers: headers
            }
        );

        if (!response.ok) {
            throw new Error('Failed to fetch place details');
        }

        const place = await response.json();

        displayPlaceDetails(place);
    } catch (error) {
        console.error(error);

        const placeDetails =
            document.getElementById('place-details');

        if (placeDetails) {
            placeDetails.innerHTML =
                '<p>Unable to load place details.</p>';
        }
    }
}


function displayPlaceDetails(place) {
    const placeDetails =
        document.getElementById('place-details');

    const reviewsList =
        document.getElementById('reviews-list');

    const title =
        place.title || place.name || 'Unnamed Place';

    let host = 'Unknown';

    if (place.owner) {
        if (place.owner.first_name || place.owner.last_name) {
            host = [
                place.owner.first_name,
                place.owner.last_name
            ].filter(Boolean).join(' ');
        } else if (place.owner.name) {
            host = place.owner.name;
        }
    }

    const amenities = place.amenities || [];

    let amenitiesHTML = '<p>No amenities available.</p>';

    if (amenities.length > 0) {
        amenitiesHTML = '<ul>';

        amenities.forEach((amenity) => {
            const name =
                amenity.name || amenity;

            amenitiesHTML += `<li>${name}</li>`;
        });

        amenitiesHTML += '</ul>';
    }

    placeDetails.innerHTML = `
        <h1>${title}</h1>

        <div class="place-info">
            <p>
                <strong>Host:</strong>
                ${host}
            </p>

            <p>
                <strong>Price per night:</strong>
                $${place.price}
            </p>

            <p>
                <strong>Description:</strong>
                ${place.description || 'No description available.'}
            </p>

            <h2>Amenities</h2>
            ${amenitiesHTML}
        </div>
    `;

    if (!reviewsList) {
        return;
    }

    reviewsList.innerHTML = '';

    const reviews = place.reviews || [];

    if (reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet.</p>';
        return;
    }

    reviews.forEach((review) => {
        const card = document.createElement('article');

        card.className = 'review-card';

        let userName = 'Anonymous';

        if (review.user) {
            if (review.user.first_name ||
                review.user.last_name) {
                userName = [
                    review.user.first_name,
                    review.user.last_name
                ].filter(Boolean).join(' ');
            } else if (review.user.name) {
                userName = review.user.name;
            }
        }

        card.innerHTML = `
            <p>${review.text || ''}</p>
            <p>
                <strong>User:</strong>
                ${userName}
            </p>
            <p>
                <strong>Rating:</strong>
                ${review.rating}/5
            </p>
        `;

        reviewsList.appendChild(card);
    });
}


/* Task 4 - Add review */

document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');

    if (!reviewForm) {
        return;
    }

    const token = getCookie('token');

    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    const placeId = getReviewPlaceIdFromURL();

    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const reviewText =
            document.getElementById('review').value.trim();

        const rating =
            document.getElementById('rating').value;

        await submitReview(
            token,
            placeId,
            reviewText,
            rating
        );
    });
});


function getReviewPlaceIdFromURL() {
    const params =
        new URLSearchParams(window.location.search);

    return params.get('place_id');
}


async function submitReview(token, placeId, reviewText, rating) {
    const message =
        document.getElementById('review-message');

    try {
        const response = await fetch(
            'http://127.0.0.1:5000/api/v1/reviews/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    text: reviewText,
                    rating: Number(rating),
                    place_id: placeId
                })
            }
        );

        const data = await response.json();

        if (response.ok) {
            message.textContent =
                'Review submitted successfully!';

            document.getElementById('review-form').reset();

            setTimeout(() => {
                window.location.href =
                    `place.html?id=${placeId}`;
            }, 1500);
        } else {
            message.textContent =
                data.error || 'Failed to submit review.';
        }
    } catch (error) {
        console.error(error);

        message.textContent =
            'Unable to connect to the server.';
    }
}

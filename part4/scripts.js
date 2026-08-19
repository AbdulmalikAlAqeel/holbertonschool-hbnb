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

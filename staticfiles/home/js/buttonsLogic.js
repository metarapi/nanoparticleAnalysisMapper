console.log('buttonsLogic.js loaded');

document.addEventListener("DOMContentLoaded", function() {
    const importDataButton = document.getElementById('displayForm');

    if (importDataButton) {
        importDataButton.addEventListener('click', function() {
            // Get the CSRF token from the cookie
            const csrfToken = getCookie('csrftoken');

            // Create a POST request with the CSRF token in the headers
            fetch('/displayForm/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, // Include the CSRF token in the request headers
                },
            })
            .then(response => response.text())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});

// Function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if the cookie's name matches the CSRF cookie name
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

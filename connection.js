// SmartEduX Base API Connection Configuration
const API_BASE_URL = "http://127.0.0.1:8000/api";

// Helper function for API Requests
async function apiRequest(endpoint, method = "GET", data = null) {
    // Endpoints handling slash
    const formattedEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
    
    // Yahan 'access' key kar di gayi hai taake token theek se mil sakay
    const token = localStorage.getItem("access_token") || localStorage.getItem("access") || sessionStorage.getItem("access");

    const headers = {
        "X-CSRFToken": getCookie("csrftoken") || ""
    };

    // Agar token mojood hai toh headers mein attach kar dein
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const options = {
        method: method,
        headers: headers,
    };

    if (data) {
        if (data instanceof FormData) {
            options.body = data;
        } else {
            headers["Content-Type"] = "application/json";
            options.body = JSON.stringify(data);
        }
    }

    try {
        const response = await fetch(`${API_BASE_URL}${formattedEndpoint}`, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("API Connection Error:", error);
        return null;
    }
}

// Function to get Django CSRF Cookie Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
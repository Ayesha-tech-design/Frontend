/**
 * SmartEduX Client-Side Authentication Service
 * Gateway Endpoint: Django REST Framework User Verification
 */

const AUTH_API_URL = "http://127.0.0.1:8000/api/auth/login/";

document.getElementById("loginForm").addEventListener("submit", async (event) => {
    // Intercept default submission to prevent synchronous page reloads
    event.preventDefault();

    // Query active state values from DOM input streams
    const emailPayload = document.getElementById("emailInput").value;
    const passwordPayload = document.getElementById("password").value;

    try {
        // Dispatch asynchronous HTTP POST dispatch to verification sequence
        const networkResponse = await fetch(AUTH_API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ 
                email: emailPayload, 
                password: passwordPayload 
            })
        });

        const responseData = await networkResponse.json();

        // Evaluate server infrastructure execution flags
        if (networkResponse.ok) {
            // Commit token string into client session local memory
            localStorage.setItem("authToken", responseData.token);
            
            alert("Authentication Verified successfully. Redirecting to user platform...");
            window.location.href = "dashboard.html";
        } else {
            alert("Authentication Rejected: " + (responseData.error || "Invalid user footprint."));
        }
    } catch (networkFault) {
        console.error("Pipeline failure during remote server initialization:", networkFault);
        alert("Server unreachable. Please verify network interfaces or active host systems.");
    }
});
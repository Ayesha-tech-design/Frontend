/**
 * SmartEduX Client-Side Authentication Service
 * Gateway Endpoint: Django REST Framework User Verification
 */

const AUTH_API_URL = "http://127.0.0.1:8000/api/auth/login/";

document.getElementById("loginForm")?.addEventListener("submit", async (event) => {
    // Intercept default submission to prevent page reloads
    event.preventDefault();

    const emailInput = document.getElementById("emailInput");
    const passwordInput = document.getElementById("password");

    if (!emailInput || !passwordInput) return;

    const emailPayload = emailInput.value.trim();
    const passwordPayload = passwordInput.value;

    try {
        // Asynchronous HTTP POST dispatch to Django API
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

        if (networkResponse.ok) {
            // Commit SimpleJWT access tokens into client session memory
            localStorage.setItem("authToken", responseData.access || responseData.token);
            if (responseData.refresh) {
                localStorage.setItem("refreshToken", responseData.refresh);
            }
            if (responseData.user) {
                localStorage.setItem("userData", JSON.stringify(responseData.user));
            }

            alert("✅ Authentication Verified successfully! Redirecting...");

            // Smart Role-Based Redirection
            const userRole = responseData.role || (responseData.user && responseData.user.role);
            const isApproved = responseData.is_approved !== undefined ? responseData.is_approved : true;

            if (userRole === "admin") {
                window.location.href = "admin dashboard.html";
            } else if (userRole === "teacher") {
                if (!isApproved) {
                    window.location.href = "pending-approval.html";
                } else {
                    window.location.href = "teacher dashboard.html";
                }
            } else {
                // Default Student Redirection
                window.location.href = "student dashboard.html";
            }

        } else {
            alert("❌ Authentication Rejected: " + (responseData.error || responseData.detail || "Invalid user credentials."));
        }
    } catch (networkFault) {
        console.error("Pipeline failure during remote server initialization:", networkFault);
        
        // Offline Fallback Mode for Local Presentation/Testing
        alert("⚠️ Backend Offline Mode: Logging in using local session context...");
        localStorage.setItem("authToken", "demo_jwt_access_token_2026");
        
        if (emailPayload.includes("admin")) {
            window.location.href = "admin dashboard.html";
        } else if (emailPayload.includes("teacher")) {
            window.location.href = "teacher dashboard.html";
        } else {
            window.location.href = "student dashboard.html";
        }
    }
});
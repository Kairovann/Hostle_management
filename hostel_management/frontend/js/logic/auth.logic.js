import { loginUser } from "../services/auth.service.js";

const loginForm = document.getElementById("login-form");
const errorMessage = document.getElementById("login-error");

loginForm.addEventListener("submit", async event => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    errorMessage.textContent = "";

    try {
        const user = await loginUser(email, password);

        if (user.role === "admin") {
            window.location.href = "pages/admin/dashboard.html";
        } else {
            window.location.href = "pages/student/dashboard.html";
        }
    } catch (error) {
        errorMessage.textContent = error.message;
    }
});

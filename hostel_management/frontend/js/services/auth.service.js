// Demo login only. Real authentication must be handled by the backend.
export async function loginUser(email, password) {
    if (email === "admin@hostel.com" && password === "admin123") {
        const user = { name: "Hostel Admin", email, role: "admin" };
        localStorage.setItem("hostel_user", JSON.stringify(user));
        return user;
    }

    if (email === "student@hostel.com" && password === "student123") {
        const user = { name: "Aarav Sharma", email, role: "student" };
        localStorage.setItem("hostel_user", JSON.stringify(user));
        return user;
    }

    throw new Error("Incorrect email or password.");
}

export function getCurrentUser() {
    const user = localStorage.getItem("hostel_user");
    return user ? JSON.parse(user) : null;
}

export function logoutUser() {
    localStorage.removeItem("hostel_user");
    window.location.href = "../../index.html";
}

import { getCurrentUser, logoutUser } from "./services/auth.service.js";
import { createNavbar } from "./components/navbar.js";
import { createSidebar } from "./components/sidebar.js";

const user = getCurrentUser();
const page = document.body.dataset.page;
const role = document.body.dataset.role || "admin";

if (!user) {
    window.location.href = "../../index.html";
} else if (user.role !== role) {
    window.location.href = user.role === "admin"
        ? "../admin/dashboard.html"
        : "../student/dashboard.html";
} else {
    document.getElementById("app").innerHTML = `
        ${createNavbar(user)}
        <div class="app-layout">
            ${createSidebar(role, page)}
            <main class="main-content" id="page-content">
                <div class="loading-message">Loading page...</div>
            </main>
        </div>
    `;

    document.getElementById("logout-button").addEventListener("click", logoutUser);

    document.getElementById("menu-toggle").addEventListener("click", () => {
        document.getElementById("sidebar").classList.toggle("sidebar-open");
    });

    const pageModules = {
        dashboard: () => import("./pages/dashboard.js"),
        students: () => import("./pages/students.js"),
        rooms: () => import("./pages/rooms.js"),
        allocations: () => import("./pages/allocations.js"),
        fees: () => import("./pages/fees.js"),
        complaints: () => import("./pages/complaints.js"),
        visitors: () => import("./pages/visitors.js"),
        expenses: () => import("./pages/expenses.js"),
        reports: () => import("./pages/reports.js"),
        complaint: () => import("./pages/complaints.js")
    };

    if (pageModules[page]) {
        pageModules[page]().then(module => module.initPage(user));
    }
}

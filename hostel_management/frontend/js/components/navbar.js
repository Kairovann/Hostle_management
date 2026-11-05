export function createNavbar(user) {
    return `
        <header class="topbar">
            <div class="topbar-left">
                <button class="menu-button" id="menu-toggle" aria-label="Toggle menu">☰</button>
                <a class="brand" href="${user.role === "admin" ? "dashboard.html" : "../student/dashboard.html"}">
                    <span class="brand-mark">H</span>
                    <span>Hostel<span class="brand-light">Desk</span></span>
                </a>
            </div>
            <div class="topbar-right">
                <span class="user-name">${user.name}</span>
                <span class="role-label">${user.role}</span>
                <button class="button button-outline button-small" id="logout-button">Logout</button>
            </div>
        </header>
    `;
}

const adminLinks = [
    ["dashboard", "Dashboard", "▦"],
    ["students", "Students", "♙"],
    ["rooms", "Rooms", "▤"],
    ["allocations", "Room allocation", "⌂"],
    ["fees", "Fees", "₹"],
    ["complaints", "Complaints", "☷"],
    ["visitors", "Visitors", "♧"],
    ["expenses", "Expenses", "↗"],
    ["reports", "Reports", "▥"]
];

export function createSidebar(role, currentPage) {
    const links = role === "admin"
        ? adminLinks.map(([page, label, icon]) => ({
            page, label, icon, href: page + ".html"
        }))
        : [
            { page: "dashboard", label: "My dashboard", icon: "▦", href: "dashboard.html" },
            { page: "complaint", label: "Submit complaint", icon: "☷", href: "complaint.html" }
        ];

    return `
        <aside class="sidebar" id="sidebar">
            <p class="sidebar-heading">${role === "admin" ? "ADMIN MENU" : "STUDENT MENU"}</p>
            <nav>
                ${links.map(link => `
                    <a class="nav-link ${currentPage === link.page ? "active" : ""}"
                       href="${link.href}">
                        <span class="nav-icon">${link.icon}</span>
                        <span>${link.label}</span>
                    </a>
                `).join("")}
            </nav>
            <div class="sidebar-note">
                <strong>HostelDesk</strong>
                <span>Hostel management portal</span>
            </div>
        </aside>
    `;
}

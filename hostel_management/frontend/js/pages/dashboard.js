import { getAll } from "../services/api.js";

export async function initPage(user) {
    const content = document.getElementById("page-content");

    if (user.role === "student") {
        const complaints = (await getAll("complaints")).filter(item => item.student === user.name);
        content.innerHTML = `
            <div class="page-heading">
                <div><p class="eyebrow">STUDENT PORTAL</p><h1>My dashboard</h1><p>Welcome back, ${user.name}.</p></div>
            </div>
            <div class="stats-grid">
                <article class="stat-card"><span class="stat-label">Room</span><strong>A-101</strong><span class="stat-foot">Block A</span></article>
                <article class="stat-card"><span class="stat-label">Fee status</span><strong>Pending</strong><span class="stat-foot">Check with hostel office</span></article>
                <article class="stat-card"><span class="stat-label">My complaints</span><strong>${complaints.length}</strong><span class="stat-foot">Submitted by you</span></article>
            </div>
            <section class="panel">
                <div class="panel-heading"><div><h2>Quick links</h2><p>Common student actions</p></div></div>
                <div class="quick-links">
                    <a class="quick-link" href="complaint.html"><span>＋</span><strong>Submit a complaint</strong><small>Report an issue to the hostel office</small></a>
                </div>
            </section>
            <section class="panel"><div class="panel-heading"><div><h2>My recent complaints</h2><p>Track the status of your requests</p></div></div>
                ${complaints.length ? complaints.map(item => `<div class="list-row"><div><strong>${item.subject}</strong><small>${item.date}</small></div><span class="status status-${item.status.toLowerCase().replaceAll(" ", "-")}">${item.status}</span></div>`).join("") : '<div class="empty-state">You have not submitted any complaints.</div>'}
            </section>
        `;
        return;
    }

    const [students, rooms, fees, complaints] = await Promise.all([
        getAll("students"), getAll("rooms"), getAll("fees"), getAll("complaints")
    ]);

    const pendingFees = fees.filter(item => item.status !== "Paid").length;
    const openComplaints = complaints.filter(item => item.status !== "Resolved").length;

    content.innerHTML = `
        <div class="page-heading">
            <div><p class="eyebrow">OVERVIEW</p><h1>Admin dashboard</h1><p>Here is what is happening in your hostel.</p></div>
            <span class="date-label">${new Date().toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" })}</span>
        </div>
        <div class="stats-grid">
            <article class="stat-card"><span class="stat-label">Total students</span><strong>${students.length}</strong><span class="stat-foot">Registered students</span></article>
            <article class="stat-card"><span class="stat-label">Total rooms</span><strong>${rooms.length}</strong><span class="stat-foot">Across all blocks</span></article>
            <article class="stat-card"><span class="stat-label">Pending fees</span><strong>${pendingFees}</strong><span class="stat-foot">Need attention</span></article>
            <article class="stat-card"><span class="stat-label">Open complaints</span><strong>${openComplaints}</strong><span class="stat-foot">Not yet resolved</span></article>
        </div>
        <div class="dashboard-columns">
            <section class="panel"><div class="panel-heading"><div><h2>Recent complaints</h2><p>Latest student requests</p></div><a href="complaints.html">View all</a></div>
                ${complaints.slice(0, 4).map(item => `<div class="list-row"><div><strong>${item.subject}</strong><small>${item.student} · ${item.date}</small></div><span class="status">${item.status}</span></div>`).join("") || '<div class="empty-state">No complaints yet.</div>'}
            </section>
            <section class="panel"><div class="panel-heading"><div><h2>Quick actions</h2><p>Go directly to a section</p></div></div>
                <div class="quick-links">
                    <a class="quick-link" href="students.html"><span>＋</span><strong>Add student</strong><small>Register a new hostel student</small></a>
                    <a class="quick-link" href="rooms.html"><span>＋</span><strong>Add room</strong><small>Update hostel room details</small></a>
                    <a class="quick-link" href="allocations.html"><span>⌂</span><strong>Allocate room</strong><small>Assign a student to a room</small></a>
                </div>
            </section>
        </div>
    `;
}

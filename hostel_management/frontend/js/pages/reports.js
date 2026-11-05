import { getAll } from "../services/api.js";

export async function initPage() {
    const [students, rooms, fees, expenses, complaints] = await Promise.all([
        getAll("students"), getAll("rooms"), getAll("fees"),
        getAll("expenses"), getAll("complaints")
    ]);

    const totalFees = fees.filter(item => item.status === "Paid").reduce((sum, item) => sum + Number(item.amount), 0);
    const pendingFees = fees.filter(item => item.status !== "Paid").reduce((sum, item) => sum + Number(item.amount), 0);
    const totalExpenses = expenses.reduce((sum, item) => sum + Number(item.amount), 0);
    const occupiedBeds = rooms.reduce((sum, room) => sum + Number(room.occupied || 0), 0);
    const totalBeds = rooms.reduce((sum, room) => sum + Number(room.capacity || 0), 0);

    document.getElementById("page-content").innerHTML = `
        <div class="page-heading"><div><p class="eyebrow">HOSTEL MANAGEMENT</p><h1>Reports</h1><p>A quick summary of hostel records.</p></div>
            <button class="button button-outline" onclick="window.print()">Print report</button>
        </div>
        <div class="stats-grid">
            <article class="stat-card"><span class="stat-label">Students</span><strong>${students.length}</strong></article>
            <article class="stat-card"><span class="stat-label">Rooms</span><strong>${rooms.length}</strong></article>
            <article class="stat-card"><span class="stat-label">Occupied beds</span><strong>${occupiedBeds} / ${totalBeds}</strong></article>
            <article class="stat-card"><span class="stat-label">Complaints</span><strong>${complaints.length}</strong></article>
        </div>
        <section class="panel"><div class="panel-heading"><div><h2>Financial summary</h2><p>Amounts are based on the current demo records.</p></div></div>
            <div class="report-grid">
                <div><span>Fees collected</span><strong>₹${totalFees.toLocaleString("en-IN")}</strong></div>
                <div><span>Pending fees</span><strong>₹${pendingFees.toLocaleString("en-IN")}</strong></div>
                <div><span>Total expenses</span><strong>₹${totalExpenses.toLocaleString("en-IN")}</strong></div>
            </div>
        </section>
    `;
}

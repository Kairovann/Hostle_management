import { showRecordsPage } from "../logic/page-tools.js";
import { createRecord, getAll } from "../services/api.js";
import { showNotification } from "../components/notification.js";

export async function initPage(user) {
    if (user.role === "student") {
        const content = document.getElementById("page-content");
        content.innerHTML = `
            <div class="page-heading"><div><p class="eyebrow">STUDENT PORTAL</p><h1>Submit a complaint</h1><p>Tell the hostel office about an issue.</p></div></div>
            <section class="panel form-panel">
                <form id="complaint-form" class="form-grid">
                    <label class="form-field"><span>Subject</span><input name="subject" required placeholder="e.g. Fan not working"></label>
                    <label class="form-field full-field"><span>Description</span><textarea name="description" rows="5" required placeholder="Describe the issue clearly..."></textarea></label>
                    <div class="form-actions"><button class="button button-primary" type="submit">Submit complaint</button></div>
                </form>
            </section>
            <section class="panel"><div class="panel-heading"><div><h2>My complaints</h2><p>Check the current status of your requests.</p></div></div><div id="my-complaints"></div></section>
        `;

        async function drawMyComplaints() {
            const complaints = (await getAll("complaints")).filter(item => item.student === user.name);
            document.getElementById("my-complaints").innerHTML = complaints.length
                ? complaints.map(item => `<div class="list-row"><div><strong>${item.subject}</strong><small>${item.date}</small></div><span class="status">${item.status}</span></div>`).join("")
                : '<div class="empty-state">No complaints submitted yet.</div>';
        }

        document.getElementById("complaint-form").addEventListener("submit", async event => {
            event.preventDefault();
            const formData = new FormData(event.target);
            await createRecord("complaints", {
                student: user.name,
                subject: formData.get("subject"),
                description: formData.get("description"),
                date: new Date().toISOString().slice(0, 10),
                status: "Submitted"
            });
            event.target.reset();
            showNotification("Complaint submitted.");
            drawMyComplaints();
        });

        drawMyComplaints();
        return;
    }

    showRecordsPage({
        title: "Complaint management",
        description: "Review student complaints and update their progress.",
        resource: "complaints",
        columns: [
            { key: "student", label: "Student" },
            { key: "subject", label: "Subject" },
            { key: "date", label: "Date" },
            { key: "status", label: "Status" }
        ],
        fields: [
            { name: "student", label: "Student name", type: "text" },
            { name: "subject", label: "Subject", type: "text" },
            { name: "description", label: "Description", type: "text" },
            { name: "date", label: "Date", type: "date" },
            { name: "status", label: "Status", type: "select", options: ["Submitted", "In Progress", "Resolved"] }
        ]
    });
}

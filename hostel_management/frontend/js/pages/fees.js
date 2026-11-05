import { showRecordsPage } from "../logic/page-tools.js";

export function initPage() {
    showRecordsPage({
        title: "Fee management",
        description: "Record hostel fees and track payment status.",
        resource: "fees",
        columns: [
            { key: "student", label: "Student" },
    { key: "amount", label: "Amount (₹)" },
    { key: "dueDate", label: "Due date" },
    { key: "status", label: "Status" }
        ],
        fields: [
            { name: "student", label: "Student name", type: "text" },
    { name: "amount", label: "Amount (₹)", type: "number" },
    { name: "dueDate", label: "Due date", type: "date" },
    { name: "status", label: "Status", type: "select", options: ["Pending", "Paid", "Overdue"] }
        ]
    });
}

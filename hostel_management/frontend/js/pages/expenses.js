import { showRecordsPage } from "../logic/page-tools.js";

export function initPage() {
    showRecordsPage({
        title: "Expense management",
        description: "Record and review hostel operating expenses.",
        resource: "expenses",
        columns: [
            { key: "title", label: "Expense" },
    { key: "category", label: "Category" },
    { key: "amount", label: "Amount (₹)" },
    { key: "date", label: "Date" },
    { key: "notes", label: "Notes" }
        ],
        fields: [
            { name: "title", label: "Expense title", type: "text" },
    { name: "category", label: "Category", type: "select", options: ["Utilities", "Maintenance", "Food", "Supplies", "Other"] },
    { name: "amount", label: "Amount (₹)", type: "number" },
    { name: "date", label: "Date", type: "date" },
    { name: "notes", label: "Notes", type: "text" }
        ]
    });
}

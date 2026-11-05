import { showRecordsPage } from "../logic/page-tools.js";

export function initPage() {
    showRecordsPage({
        title: "Room allocation",
        description: "Assign rooms to students and manage existing allocations.",
        resource: "allocations",
        columns: [
            { key: "student", label: "Student" },
    { key: "room", label: "Room" },
    { key: "date", label: "Allocation date" },
    { key: "status", label: "Status" }
        ],
        fields: [
            { name: "student", label: "Student name", type: "text" },
    { name: "room", label: "Room number", type: "text" },
    { name: "date", label: "Allocation date", type: "date" },
    { name: "status", label: "Status", type: "select", options: ["Active", "Ended"] }
        ]
    });
}

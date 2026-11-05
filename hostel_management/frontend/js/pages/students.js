import { showRecordsPage } from "../logic/page-tools.js";

export function initPage() {
    showRecordsPage({
        title: "Students",
        description: "Register and manage hostel student records.",
        resource: "students",
        columns: [
            { key: "name", label: "Name" },
    { key: "email", label: "Email" },
    { key: "phone", label: "Phone" },
    { key: "course", label: "Course" },
    { key: "room", label: "Room" },
    { key: "status", label: "Status" }
        ],
        fields: [
            { name: "name", label: "Full name", type: "text" },
    { name: "email", label: "Email address", type: "email" },
    { name: "phone", label: "Phone number", type: "tel" },
    { name: "course", label: "Course", type: "text" },
    { name: "year", label: "Academic year", type: "text" },
    { name: "room", label: "Room number", type: "text" },
    { name: "status", label: "Status", type: "select", options: ["Active", "Inactive"] }
        ]
    });
}

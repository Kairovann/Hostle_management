import { showRecordsPage } from "../logic/page-tools.js";

export function initPage() {
    showRecordsPage({
        title: "Visitor management",
        description: "Record visitor details and visit timings.",
        resource: "visitors",
        columns: [
            { key: "visitorName", label: "Visitor" },
    { key: "student", label: "Visiting student" },
    { key: "relation", label: "Relation" },
    { key: "phone", label: "Phone" },
    { key: "visitDate", label: "Visit date" },
    { key: "inTime", label: "In time" },
    { key: "outTime", label: "Out time" }
        ],
        fields: [
            { name: "visitorName", label: "Visitor name", type: "text" },
    { name: "student", label: "Student name", type: "text" },
    { name: "relation", label: "Relation to student", type: "text" },
    { name: "phone", label: "Phone number", type: "tel" },
    { name: "visitDate", label: "Visit date", type: "date" },
    { name: "inTime", label: "In time", type: "time" },
    { name: "outTime", label: "Out time", type: "time" }
        ]
    });
}

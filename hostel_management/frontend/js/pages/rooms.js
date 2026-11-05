import { showRecordsPage } from "../logic/page-tools.js";

export function initPage() {
    showRecordsPage({
        title: "Rooms",
        description: "Manage room numbers, capacity and availability.",
        resource: "rooms",
        columns: [
            { key: "roomNumber", label: "Room" },
    { key: "building", label: "Block" },
    { key: "type", label: "Room type" },
    { key: "capacity", label: "Capacity" },
    { key: "occupied", label: "Occupied" },
    { key: "status", label: "Status" }
        ],
        fields: [
            { name: "roomNumber", label: "Room number", type: "text" },
    { name: "building", label: "Building / block", type: "text" },
    { name: "type", label: "Room type", type: "select", options: ["Single", "Double", "Triple"] },
    { name: "capacity", label: "Capacity", type: "number" },
    { name: "occupied", label: "Occupied beds", type: "number" },
    { name: "status", label: "Status", type: "select", options: ["Available", "Full", "Maintenance"] }
        ]
    });
}

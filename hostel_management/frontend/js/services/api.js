import { API_BASE_URL, USE_DEMO_DATA } from "../config/config.js";

// Demo data is stored in the browser so the pages work without FastAPI.
const demoData = {
    students: [
        { id: 1, name: "Aarav Sharma", email: "aarav@example.com", phone: "9876543210", course: "B.Tech CSE", year: "2nd Year", room: "A-101", status: "Active" },
        { id: 2, name: "Priya Das", email: "priya@example.com", phone: "9876543211", course: "B.Tech ECE", year: "3rd Year", room: "A-102", status: "Active" },
        { id: 3, name: "Rahul Roy", email: "rahul@example.com", phone: "9876543212", course: "BCA", year: "1st Year", room: "B-201", status: "Active" }
    ],
    rooms: [
        { id: 1, roomNumber: "A-101", building: "Block A", capacity: 2, occupied: 1, type: "Double", status: "Available" },
        { id: 2, roomNumber: "A-102", building: "Block A", capacity: 2, occupied: 2, type: "Double", status: "Full" },
        { id: 3, roomNumber: "B-201", building: "Block B", capacity: 3, occupied: 1, type: "Triple", status: "Available" }
    ],
    allocations: [
        { id: 1, student: "Aarav Sharma", room: "A-101", date: "2026-08-01", status: "Active" },
        { id: 2, student: "Priya Das", room: "A-102", date: "2026-07-15", status: "Active" }
    ],
    fees: [
        { id: 1, student: "Aarav Sharma", amount: 25000, dueDate: "2026-11-15", status: "Pending" },
        { id: 2, student: "Priya Das", amount: 25000, dueDate: "2026-10-15", status: "Paid" },
        { id: 3, student: "Rahul Roy", amount: 22000, dueDate: "2026-11-15", status: "Pending" }
    ],
    complaints: [
        { id: 1, student: "Aarav Sharma", subject: "Fan not working", description: "The ceiling fan is not working.", date: "2026-11-02", status: "In Progress" },
        { id: 2, student: "Priya Das", subject: "Water supply", description: "Water supply is irregular.", date: "2026-11-01", status: "Submitted" }
    ],
    visitors: [
        { id: 1, visitorName: "Rohan Sharma", student: "Aarav Sharma", relation: "Brother", phone: "9876500000", visitDate: "2026-11-05", inTime: "10:30", outTime: "11:15" }
    ],
    expenses: [
        { id: 1, title: "Electricity bill", category: "Utilities", amount: 12500, date: "2026-11-01", notes: "Monthly electricity bill" },
        { id: 2, title: "Plumbing repair", category: "Maintenance", amount: 3500, date: "2026-11-03", notes: "Bathroom repair" }
    ]
};

function readDemoData(key) {
    const savedData = localStorage.getItem("hostel_" + key);

    if (savedData) {
        return JSON.parse(savedData);
    }

    localStorage.setItem("hostel_" + key, JSON.stringify(demoData[key] || []));
    return demoData[key] || [];
}

function saveDemoData(key, records) {
    localStorage.setItem("hostel_" + key, JSON.stringify(records));
}

// This function is the one place where the frontend talks to the backend.
// Later, the service files can call this function with real API endpoints.
export async function apiRequest(endpoint, options = {}) {
    if (USE_DEMO_DATA) {
        throw new Error("Demo mode is enabled. Use the demo data functions for now.");
    }

    const response = await fetch(API_BASE_URL + endpoint, {
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        },
        ...options
    });

    if (!response.ok) {
        throw new Error("The server returned an error: " + response.status);
    }

    return response.json();
}

export async function getAll(key) {
    if (USE_DEMO_DATA) return readDemoData(key);
    return apiRequest("/" + key);
}

export async function createRecord(key, record) {
    if (USE_DEMO_DATA) {
        const records = readDemoData(key);
        const newRecord = { ...record, id: Date.now() };
        records.push(newRecord);
        saveDemoData(key, records);
        return newRecord;
    }

    return apiRequest("/" + key, {
        method: "POST",
        body: JSON.stringify(record)
    });
}

export async function updateRecord(key, id, updatedRecord) {
    if (USE_DEMO_DATA) {
        const records = readDemoData(key);
        const newRecords = records.map(record =>
            record.id === Number(id) ? { ...record, ...updatedRecord } : record
        );
        saveDemoData(key, newRecords);
        return updatedRecord;
    }

    return apiRequest("/" + key + "/" + id, {
        method: "PUT",
        body: JSON.stringify(updatedRecord)
    });
}

export async function deleteRecord(key, id) {
    if (USE_DEMO_DATA) {
        const records = readDemoData(key).filter(record => record.id !== Number(id));
        saveDemoData(key, records);
        return true;
    }

    return apiRequest("/" + key + "/" + id, { method: "DELETE" });
}

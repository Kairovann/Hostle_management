import { getAll, createRecord, updateRecord, deleteRecord } from "./api.js";

const resource = "complaints";

export function getComplaints() {
    return getAll(resource);
}

export function addComplaint(record) {
    return createRecord(resource, record);
}

export function editComplaint(id, record) {
    return updateRecord(resource, id, record);
}

export function removeComplaint(id) {
    return deleteRecord(resource, id);
}

import { getAll, createRecord, updateRecord, deleteRecord } from "./api.js";

const resource = "visitors";

export function getVisitors() {
    return getAll(resource);
}

export function addVisitor(record) {
    return createRecord(resource, record);
}

export function editVisitor(id, record) {
    return updateRecord(resource, id, record);
}

export function removeVisitor(id) {
    return deleteRecord(resource, id);
}

import { getAll, createRecord, updateRecord, deleteRecord } from "./api.js";

const resource = "allocations";

export function getAllocations() {
    return getAll(resource);
}

export function addAllocation(record) {
    return createRecord(resource, record);
}

export function editAllocation(id, record) {
    return updateRecord(resource, id, record);
}

export function removeAllocation(id) {
    return deleteRecord(resource, id);
}

import { getAll, createRecord, updateRecord, deleteRecord } from "./api.js";

const resource = "fees";

export function getFees() {
    return getAll(resource);
}

export function addFee(record) {
    return createRecord(resource, record);
}

export function editFee(id, record) {
    return updateRecord(resource, id, record);
}

export function removeFee(id) {
    return deleteRecord(resource, id);
}

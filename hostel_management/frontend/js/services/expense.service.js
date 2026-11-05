import { getAll, createRecord, updateRecord, deleteRecord } from "./api.js";

const resource = "expenses";

export function getExpenses() {
    return getAll(resource);
}

export function addExpense(record) {
    return createRecord(resource, record);
}

export function editExpense(id, record) {
    return updateRecord(resource, id, record);
}

export function removeExpense(id) {
    return deleteRecord(resource, id);
}

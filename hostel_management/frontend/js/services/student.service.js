import { getAll, createRecord, updateRecord, deleteRecord } from "./api.js";

const resource = "students";

export function getStudents() {
    return getAll(resource);
}

export function addStudent(record) {
    return createRecord(resource, record);
}

export function editStudent(id, record) {
    return updateRecord(resource, id, record);
}

export function removeStudent(id) {
    return deleteRecord(resource, id);
}

import { getAll, createRecord, updateRecord, deleteRecord } from "./api.js";

const resource = "rooms";

export function getRooms() {
    return getAll(resource);
}

export function addRoom(record) {
    return createRecord(resource, record);
}

export function editRoom(id, record) {
    return updateRecord(resource, id, record);
}

export function removeRoom(id) {
    return deleteRecord(resource, id);
}

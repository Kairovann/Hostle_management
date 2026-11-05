import { showNotification } from "../components/notification.js";
import { openModal, closeModal } from "../components/modal.js";
import { createTable } from "../components/table.js";
import { getAll, createRecord, updateRecord, deleteRecord } from "../services/api.js";

export async function showRecordsPage(settings) {
    const content = document.getElementById("page-content");
    let records = await getAll(settings.resource);

    function drawPage() {
        content.innerHTML = `
            <div class="page-heading">
                <div><p class="eyebrow">${settings.eyebrow || "HOSTEL MANAGEMENT"}</p><h1>${settings.title}</h1><p>${settings.description}</p></div>
                ${settings.allowAdd === false ? "" : '<button class="button button-primary" id="add-record">＋ Add new</button>'}
            </div>
            <section class="panel">
                <div class="panel-heading"><div><h2>${settings.listTitle || "All records"}</h2><p>${records.length} record(s)</p></div>
                    <input class="search-input" id="record-search" type="search" placeholder="Search records...">
                </div>
                <div id="records-table"></div>
            </section>
        `;

        drawTable(records);

        const searchInput = document.getElementById("record-search");
        searchInput.addEventListener("input", () => {
            const searchText = searchInput.value.toLowerCase();
            const filtered = records.filter(record =>
                Object.values(record).join(" ").toLowerCase().includes(searchText)
            );
            drawTable(filtered);
        });

        const addButton = document.getElementById("add-record");
        if (addButton) addButton.addEventListener("click", () => showForm());
    }

    function drawTable(rows) {
        const columns = settings.columns.map(column => ({
            ...column,
            render: column.render || (record => record[column.key] ?? "-")
        }));

        columns.push({
            label: "Actions",
            render: record => `
                <div class="table-actions">
                    <button class="text-button edit-record" data-id="${record.id}">Edit</button>
                    <button class="text-button danger delete-record" data-id="${record.id}">Delete</button>
                </div>
            `
        });

        document.getElementById("records-table").innerHTML = createTable(columns, rows);

        document.querySelectorAll(".edit-record").forEach(button => {
            button.addEventListener("click", () => {
                const record = records.find(item => item.id === Number(button.dataset.id));
                showForm(record);
            });
        });

        document.querySelectorAll(".delete-record").forEach(button => {
            button.addEventListener("click", async () => {
                if (!confirm("Delete this record? This cannot be undone.")) return;
                await deleteRecord(settings.resource, button.dataset.id);
                records = await getAll(settings.resource);
                drawPage();
                showNotification("Record deleted.");
            });
        });
    }

    function showForm(record = null) {
        const fieldsHTML = settings.fields.map(field => `
            <label class="form-field">
                <span>${field.label}</span>
                ${field.type === "select"
                    ? `<select name="${field.name}" ${field.required === false ? "" : "required"}>
                        ${field.options.map(option => `<option value="${option}" ${record && record[field.name] === option ? "selected" : ""}>${option}</option>`).join("")}
                       </select>`
                    : `<input name="${field.name}" type="${field.type || "text"}" value="${record ? (record[field.name] ?? "") : ""}" placeholder="${field.placeholder || ""}" ${field.required === false ? "" : "required"}>`
                }
            </label>
        `).join("");

        const overlay = openModal(record ? "Edit record" : settings.formTitle || "Add new record", `
            <form id="record-form" class="form-grid">
                ${fieldsHTML}
                <div class="form-actions">
                    <button type="button" class="button button-outline" id="cancel-form">Cancel</button>
                    <button type="submit" class="button button-primary">${record ? "Save changes" : "Add record"}</button>
                </div>
            </form>
        `);

        document.getElementById("cancel-form").addEventListener("click", closeModal);

        document.getElementById("record-form").addEventListener("submit", async event => {
            event.preventDefault();
            const formData = new FormData(event.target);
            const newRecord = {};

            settings.fields.forEach(field => {
                const value = formData.get(field.name);
                newRecord[field.name] = field.type === "number" ? Number(value) : value;
            });

            if (record) {
                await updateRecord(settings.resource, record.id, newRecord);
                showNotification("Record updated.");
            } else {
                await createRecord(settings.resource, newRecord);
                showNotification("Record added.");
            }

            records = await getAll(settings.resource);
            closeModal();
            drawPage();
        });
    }

    drawPage();
}

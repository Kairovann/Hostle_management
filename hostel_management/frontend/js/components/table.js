export function createTable(columns, rows) {
    if (!rows.length) {
        return `<div class="empty-state">No records found.</div>`;
    }

    const headings = columns.map(column => `<th>${column.label}</th>`).join("");

    const body = rows.map(row => `
        <tr>
            ${columns.map(column => `<td>${column.render ? column.render(row) : (row[column.key] ?? "-")}</td>`).join("")}
        </tr>
    `).join("");

    return `
        <div class="table-wrap">
            <table>
                <thead><tr>${headings}</tr></thead>
                <tbody>${body}</tbody>
            </table>
        </div>
    `;
}

export function openModal(title, bodyHTML) {
    closeModal();

    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";
    overlay.id = "active-modal";

    overlay.innerHTML = `
        <section class="modal">
            <div class="modal-header">
                <h2>${title}</h2>
                <button class="icon-button" id="close-modal" aria-label="Close">×</button>
            </div>
            <div class="modal-body">${bodyHTML}</div>
        </section>
    `;

    document.body.appendChild(overlay);

    document.getElementById("close-modal").addEventListener("click", closeModal);
    overlay.addEventListener("click", event => {
        if (event.target === overlay) closeModal();
    });

    return overlay;
}

export function closeModal() {
    const overlay = document.getElementById("active-modal");
    if (overlay) overlay.remove();
}

export function showNotification(message, type = "success") {
    let notification = document.querySelector(".notification");

    if (!notification) {
        notification = document.createElement("div");
        notification.className = "notification";
        document.body.appendChild(notification);
    }

    notification.textContent = message;
    notification.className = "notification " + type + " show";

    setTimeout(() => {
        notification.classList.remove("show");
    }, 2800);
}

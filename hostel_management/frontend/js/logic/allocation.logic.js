// Keep page-specific validation here as the project grows.
export function isRequired(value) {
    return String(value).trim().length > 0;
}

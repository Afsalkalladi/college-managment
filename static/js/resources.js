// File upload validation
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('id_file');
    const externalLinkInput = document.getElementById('id_external_link');
    
    if (fileInput && externalLinkInput) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                externalLinkInput.disabled = true;
                externalLinkInput.value = '';
            } else {
                externalLinkInput.disabled = false;
            }
        });
        
        externalLinkInput.addEventListener('input', function() {
            if (this.value.trim() !== '') {
                fileInput.disabled = true;
            } else {
                fileInput.disabled = false;
            }
        });
    }
});

// Confirm delete
function confirmDelete(resourceName) {
    return confirm(`Are you sure you want to delete "${resourceName}"?`);
}
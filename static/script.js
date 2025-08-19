// Clothing Store Inventory JavaScript

// Copy MCP URL to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        const button = event.target;
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('copied');
        
        setTimeout(function() {
            button.textContent = originalText;
            button.classList.remove('copied');
        }, 2000);
    }).catch(function(err) {
        console.error('Failed to copy text: ', err);
        alert('Failed to copy URL to clipboard');
    });
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Clothing Store Inventory MCP Server loaded');
    
    // Add click handlers for copy buttons
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const url = this.previousElementSibling.value;
            copyToClipboard(url);
        });
    });
});

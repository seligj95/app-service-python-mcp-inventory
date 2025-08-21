// Clothing Store Inventory JavaScript

// Copy MCP URL to clipboard
function copyToClipboard(text) {
    // If no text provided, try to get it from the input field
    if (!text) {
        const button = event.target;
        const inputField = button.previousElementSibling;
        if (inputField && inputField.value) {
            text = inputField.value;
        } else {
            console.error('No text to copy');
            alert('No URL found to copy');
            return;
        }
    }
    
    // Check if we're in a secure context (HTTPS or localhost)
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function() {
            showCopySuccess();
        }).catch(function(err) {
            console.error('Clipboard API failed: ', err);
            // Fallback for secure contexts where clipboard API fails
            fallbackCopyTextToClipboard(text);
        });
    } else {
        // Use fallback for non-secure contexts or when clipboard API is not available
        fallbackCopyTextToClipboard(text);
    }
}

function showCopySuccess() {
    const button = event.target;
    const originalText = button.textContent;
    button.textContent = 'Copied!';
    button.classList.add('copied');
    
    setTimeout(function() {
        button.textContent = originalText;
        button.classList.remove('copied');
    }, 2000);
}

// Fallback copy function for older browsers or non-secure contexts
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    textArea.style.opacity = "0";
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopySuccess();
        } else {
            // Show the URL in a modal or alert as final fallback
            showUrlModal(text);
        }
    } catch (err) {
        console.error('Fallback copy failed: ', err);
        // Final fallback - show URL in modal
        showUrlModal(text);
    }
    
    document.body.removeChild(textArea);
}

// Show URL in a modal when copying fails
function showUrlModal(url) {
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
        background: rgba(0,0,0,0.5); z-index: 1000; display: flex; 
        align-items: center; justify-content: center;
    `;
    
    const content = document.createElement('div');
    content.style.cssText = `
        background: white; padding: 2rem; border-radius: 8px; 
        max-width: 90%; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    `;
    
    content.innerHTML = `
        <h3 style="margin-bottom: 1rem; color: #333;">Copy MCP Server URL</h3>
        <p style="margin-bottom: 1rem; color: #666;">Please copy this URL manually:</p>
        <input type="text" value="${url}" readonly style="
            width: 100%; padding: 0.5rem; margin-bottom: 1rem; 
            border: 1px solid #ddd; border-radius: 4px; font-family: monospace;
        " onclick="this.select()">
        <button onclick="document.body.removeChild(this.parentElement.parentElement)" style="
            background: #2196f3; color: white; border: none; padding: 0.5rem 1rem; 
            border-radius: 4px; cursor: pointer;
        ">Close</button>
    `;
    
    modal.appendChild(content);
    document.body.appendChild(modal);
    
    // Select the URL text for easy copying
    content.querySelector('input').select();
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Clothing Store Inventory MCP Server loaded');
    
    // Add visual feedback for copy buttons on hover
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
        });
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

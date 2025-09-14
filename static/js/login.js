const loginForm = document.getElementById('login-form');
const loginBtn = document.getElementById('login-btn');
const passwordField = document.getElementById('password');
const suggestionsBox = document.getElementById('suggestions-box');

// Enable login button when fields filled
loginForm.addEventListener('input', () => {
    const inputs = loginForm.querySelectorAll('input');
    let allFilled = true;
    inputs.forEach(input => {
        if (!input.value.trim()) {
            allFilled = false;
        }
    });
    if (allFilled) {
        loginBtn.classList.add('enabled');
        loginBtn.removeAttribute('disabled');
    } else {
        loginBtn.classList.remove('enabled');
        loginBtn.setAttribute('disabled', true);
    }
});
// Toggle password suggestions like Google
function togglePasswordSuggestions() {
    if (suggestionsBox.style.display === 'block') {
        suggestionsBox.style.display = 'none';
    } else {
        suggestionsBox.style.display = 'block';
        suggestionsBox.innerHTML = generateSuggestions().map(p => `<div>${p}</div>`).join('');
    }
}

// Generate multiple strong passwords
function generateSuggestions() {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()";
    let suggestions = [];
    for (let j = 0; j < 3; j++) {
        let password = "";
        for (let i = 0; i < 12; i++) {
            password += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        suggestions.push(password);
    }
    return suggestions;
}

// Insert password on click
suggestionsBox.addEventListener('click', (e) => {
    if (e.target.tagName === 'DIV') {
        passwordField.value = e.target.textContent;
        suggestionsBox.style.display = 'none';
    }
});

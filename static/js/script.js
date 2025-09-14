// =================== SIDEBAR TOGGLE ===================
const menuToggle = document.getElementById('menu-toggle');
const sidebar = document.getElementById('sidebar');

menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('active');
});

// =================== DARK MODE TOGGLE ===================
document.getElementById('dark-mode-toggle').addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
});

// =================== CASE FILE POP-UP MODALS ===================
const modals = document.querySelectorAll('.modal');
const closeBtns = document.querySelectorAll('.close');
const caseBlocks = document.querySelectorAll('.case-block');

caseBlocks.forEach(block => {
    block.addEventListener('click', () => {
        const target = block.getAttribute('data-target');
        document.getElementById(target).style.display = 'block';
    });
});

closeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        btn.closest('.modal').style.display = 'none';
    });
});

window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }
});

// =================== CASE FILTERING ===================
const filterButtons = document.querySelectorAll('.filter-btn');
filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        const filterValue = button.getAttribute('data-filter');
        document.querySelectorAll('.case-block').forEach(block => {
            if (filterValue === 'all' || block.classList.contains(filterValue)) {
                block.style.display = 'block';
            } else {
                block.style.display = 'none';
            }
        });
    });
});

// =================== RANDOM CASE GENERATOR ===================
document.getElementById('random-case-btn').addEventListener('click', () => {
    const cases = document.querySelectorAll('.case-block');
    const randomIndex = Math.floor(Math.random() * cases.length);
    const randomCase = cases[randomIndex];
    const target = randomCase.getAttribute('data-target');
    document.getElementById(target).style.display = 'block';
});

// =================== LEADERBOARD SORTING ===================
document.getElementById('sort-leaderboard').addEventListener('click', () => {
    const leaderboard = document.querySelector('#leaderboard tbody');
    const rows = Array.from(leaderboard.querySelectorAll('tr'));
    rows.sort((a, b) => {
        return parseInt(b.querySelector('.score').textContent) - parseInt(a.querySelector('.score').textContent);
    });
    rows.forEach(row => leaderboard.appendChild(row));
});

// =================== USER FEEDBACK FORM ===================
document.getElementById('feedback-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const feedback = document.getElementById('feedback-input').value;
    if (feedback.trim() !== '') {
        alert('Thank you for your feedback!');
        document.getElementById('feedback-form').reset();
    }
});

// =================== USER-POSTED THEORIES ===================
document.getElementById('theory-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const theoryInput = document.getElementById('theory-input');
    const theoryText = theoryInput.value.trim();
    if (theoryText !== '') {
        const theoryList = document.getElementById('theory-list');
        const newItem = document.createElement('li');
        newItem.textContent = theoryText;
        theoryList.appendChild(newItem);
        theoryInput.value = '';
    }
});

// =================== SCROLL ANIMATION FOR CASE CARDS ===================
// Add "fade-in" animation when cards appear in viewport
const cards = document.querySelectorAll('.case-card');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible'); // Add class when visible
        }
    });
}, { threshold: 0.2 });

cards.forEach(card => observer.observe(card));
document.getElementById('login-btn').addEventListener('click', () => {
    window.location.href = 'login.html'; // your login page path
});


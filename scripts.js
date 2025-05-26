document.addEventListener('DOMContentLoaded', function() {
    const highlight = document.querySelector('.fade-in');
    setTimeout(() => {
        highlight.style.opacity = '1';
        highlight.style.transform = 'translateY(0)';
    }, 1500);
});



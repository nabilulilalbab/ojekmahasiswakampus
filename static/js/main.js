document.addEventListener('DOMContentLoaded', () => {
    // Dark Mode Toggle
    const darkModeToggle = document.createElement('button');
    darkModeToggle.id = 'dark-mode-toggle';
    darkModeToggle.className = 'p-2 rounded-lg bg-gray-200 dark:bg-gray-700 transition-colors';
    darkModeToggle.innerHTML = '🌓';
    document.querySelector('nav').appendChild(darkModeToggle);

    darkModeToggle.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark');
        localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
    });

    // Initialize dark mode
    if (localStorage.getItem('darkMode') === 'true') {
        document.documentElement.classList.add('dark');
    }

    // Mobile menu toggle
    const menuButton = document.querySelector('button.md\\:hidden');
    const navMenu = document.querySelector('.md\\:flex');
    
    menuButton?.addEventListener('click', () => {
        navMenu.classList.toggle('hidden');
    });

    // Form handling
    document.querySelector('form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const loading = document.getElementById('loading');
        loading.classList.remove('hidden');

        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 2000));
            alert('Pemesanan berhasil! Driver akan segera menghubungi Anda');
        } catch (error) {
            console.error('Error:', error);
            alert('Terjadi kesalahan, silakan coba lagi');
        } finally {
            loading.classList.add('hidden');
        }
    });
});

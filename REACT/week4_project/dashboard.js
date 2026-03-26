document.addEventListener('DOMContentLoaded', () => {
    const navButtons = document.querySelectorAll('.nav-btn');
    const iframe = document.getElementById('main-frame');
    const viewTitle = document.getElementById('view-title');
    const loadingOverlay = document.getElementById('loading-overlay');
    const reloadBtn = document.getElementById('reload-btn');
    const fullscreenBtn = document.getElementById('fullscreen-btn');

    // Handle Iframe Load
    iframe.addEventListener('load', () => {
        loadingOverlay.classList.remove('active');
        iframe.classList.add('ready');
    });

    // Handle Navigation Clicks
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Unset active class
            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update Header
            viewTitle.textContent = btn.getAttribute('data-title');

            // Trigger Transition
            iframe.classList.remove('ready');
            loadingOverlay.classList.add('active');

            // Small delay to allow fade out before changing src (smoother UX)
            setTimeout(() => {
                iframe.src = btn.getAttribute('data-target');
            }, 300);
        });
    });

    // Reload Button
    reloadBtn.addEventListener('click', () => {
        iframe.classList.remove('ready');
        loadingOverlay.classList.add('active');
        setTimeout(() => {
            iframe.contentWindow.location.reload();
        }, 150);
    });

    // Fullscreen Button
    fullscreenBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.log(`Error attempting to enable fullscreen: ${err.message}`);
            });
        } else {
            document.exitFullscreen();
        }
    });

    // Trigger initial load fade-in
    if(iframe.src) {
        // It might have loaded before event listener attached
        setTimeout(() => {
            loadingOverlay.classList.remove('active');
            iframe.classList.add('ready');
        }, 500);
    }
});

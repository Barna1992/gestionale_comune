// Gestionale Comune - Modern UI JavaScript

document.addEventListener('DOMContentLoaded', function () {

    // ── Auto-dismiss alerts after 5 seconds ──
    document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // ── Confirm dialogs for destructive actions ──
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(el.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // ── Counter Animation (stat cards) ──
    document.querySelectorAll('[data-counter]').forEach(function (el) {
        var target = parseInt(el.textContent, 10) || 0;
        if (target === 0) return;
        el.textContent = '0';
        var duration = 1000;
        var startTime = null;

        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            var progress = Math.min((timestamp - startTime) / duration, 1);
            // ease-out cubic
            var eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.round(eased * target);
            if (progress < 1) {
                requestAnimationFrame(step);
            }
        }
        requestAnimationFrame(step);
    });

    // ── Scroll Reveal (IntersectionObserver) ──
    var revealElements = document.querySelectorAll('.reveal');
    if (revealElements.length > 0 && 'IntersectionObserver' in window) {
        var revealObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        revealElements.forEach(function (el) {
            revealObserver.observe(el);
        });
    }

    // ── Bootstrap Tooltips ──
    var tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(function (el) {
        new bootstrap.Tooltip(el);
    });

    // ── Active nav link ──
    var currentPath = window.location.pathname;
    document.querySelectorAll('.navbar-custom .nav-link').forEach(function (link) {
        var href = link.getAttribute('href');
        if (href && currentPath === href) {
            link.classList.add('active');
        }
    });
});

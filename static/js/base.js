// ============================================
// BASE.JS - Shared JavaScript for all pages
// ============================================

// ============================================
// DISCLAIMER MODAL FUNCTIONS
// ============================================

function openDisclaimer() {
    var modal = document.getElementById('disclaimerModal');
    if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

function closeDisclaimer() {
    var modal = document.getElementById('disclaimerModal');
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = '';
    }
}

function acceptDisclaimer() {
    closeDisclaimer();
    sessionStorage.setItem('disclaimerAccepted', 'true');
    showToast('Thank you for reading the disclaimer.', 'success');
}

// ============================================
// SHOW DISCLAIMER ON LOGIN/SIGNUP
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    var justLoggedIn = sessionStorage.getItem('justLoggedIn');
    var justRegistered = sessionStorage.getItem('justRegistered');
    var disclaimerAccepted = sessionStorage.getItem('disclaimerAccepted');
    
    var isLoggedIn = false;
    var userEmailMeta = document.querySelector('meta[name="user-email"]');
    if (userEmailMeta && userEmailMeta.getAttribute('content')) {
        isLoggedIn = true;
    }
    
    if (isLoggedIn && !disclaimerAccepted) {
        if (justLoggedIn === 'true' || justRegistered === 'true') {
            setTimeout(function() {
                openDisclaimer();
            }, 800);
        }
    }
    
    sessionStorage.removeItem('justLoggedIn');
    sessionStorage.removeItem('justRegistered');
});

// Close modal when clicking outside
document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('disclaimerModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeDisclaimer();
            }
        });
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeDisclaimer();
    }
});

// ============================================
// MOBILE MENU TOGGLE
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    var menuBtn = document.getElementById('mobileMenuBtn');
    var navLinks = document.getElementById('navLinks');
    
    if (menuBtn) {
        menuBtn.addEventListener('click', function() {
            this.classList.toggle('active');
            navLinks.classList.toggle('active');
            if (navLinks.classList.contains('active')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });
    }
    
    var navLinkElements = document.querySelectorAll('.nav-link');
    navLinkElements.forEach(function(link) {
        link.addEventListener('click', function() {
            if (navLinks) {
                navLinks.classList.remove('active');
            }
            if (menuBtn) {
                menuBtn.classList.remove('active');
            }
            document.body.style.overflow = '';
        });
    });
});

// ============================================
// TOAST NOTIFICATION
// ============================================

function showToast(message, type) {
    type = type || 'success';
    var toast = document.createElement('div');
    toast.className = 'toast-notification';
    var iconClass = (type === 'success') ? 'fa-check-circle' : 'fa-exclamation-circle';
    toast.innerHTML = '<i class="fas ' + iconClass + '" style="margin-right: 8px;"></i> ' + message;
    document.body.appendChild(toast);
    setTimeout(function() {
        toast.remove();
    }, 3000);
}
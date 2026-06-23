document.addEventListener('DOMContentLoaded', () => {
  const drawer = document.getElementById('navDrawer');
  const toggleBtn = document.getElementById('menuToggleBtn');
  const closeBtn = document.getElementById('navDrawerCloseBtn');
  const overlay = drawer ? drawer.querySelector('.nav-drawer-overlay') : null;
  
  if (!drawer || !toggleBtn) return;
  
  let lastActiveElement = null;
  
  const focusableSelectors = 'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])';
  
  function getFocusableElements() {
    return Array.from(drawer.querySelectorAll(focusableSelectors));
  }
  
  function openDrawer() {
    lastActiveElement = document.activeElement;
    drawer.setAttribute('aria-hidden', 'false');
    toggleBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    
    const focusable = getFocusableElements();
    if (focusable.length > 0) {
      // Find the first element that isn't the close button, or just focus close button
      focusable[0].focus();
    }
  }
  
  function closeDrawer() {
    drawer.setAttribute('aria-hidden', 'true');
    toggleBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    
    if (lastActiveElement) {
      lastActiveElement.focus();
    }
  }
  
  toggleBtn.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (overlay) overlay.addEventListener('click', closeDrawer);
  
  // ESC key to close
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer.getAttribute('aria-hidden') === 'false') {
      closeDrawer();
    }
  });
  
  // Focus trap
  drawer.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;
    
    const focusable = getFocusableElements();
    if (focusable.length === 0) return;
    
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    
    if (e.shiftKey) {
      if (document.activeElement === first) {
        last.focus();
        e.preventDefault();
      }
    } else {
      if (document.activeElement === last) {
        first.focus();
        e.preventDefault();
      }
    }
  });
  
  // Theme Management Synchronization
  const docEl = document.documentElement;
  const headerThemeBtn = document.querySelector('[data-theme-toggle]') || document.getElementById('themeBtn');
  const drawerThemeBtn = document.getElementById('drawerThemeBtn');
  
  const sunIcon = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
  const moonIcon = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
  
  function applyTheme(theme) {
    docEl.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    if (headerThemeBtn) {
      if (headerThemeBtn.tagName === 'BUTTON' && (headerThemeBtn.querySelector('svg') || headerThemeBtn.classList.contains('theme-toggle'))) {
        headerThemeBtn.innerHTML = theme === 'dark' ? sunIcon : moonIcon;
      } else if (headerThemeBtn.id === 'themeBtn') {
        headerThemeBtn.textContent = '◐';
      }
    }
    
    if (drawerThemeBtn) {
      const iconSpan = drawerThemeBtn.querySelector('.theme-icon');
      if (iconSpan) {
        iconSpan.innerHTML = theme === 'dark' ? sunIcon : moonIcon;
      }
    }
  }
  
  function toggleTheme() {
    const currentTheme = docEl.getAttribute('data-theme') || 'light';
    const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(nextTheme);
  }
  
  // We use event capture to ensure our click overrides other inline scripts if possible, or just overrides them
  if (headerThemeBtn) {
    headerThemeBtn.addEventListener('click', (e) => {
      // If there is inline onclick, we will let it execute but then force our state sync,
      // or we can remove the onclick attribute to prevent double toggling.
      if (headerThemeBtn.getAttribute('onclick')) {
        headerThemeBtn.removeAttribute('onclick');
      }
      toggleTheme();
    });
  }
  
  if (drawerThemeBtn) {
    drawerThemeBtn.addEventListener('click', toggleTheme);
  }
  
  // Initial sync from document state
  const initialTheme = docEl.getAttribute('data-theme') || 'light';
  applyTheme(initialTheme);
});

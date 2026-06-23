function changeLanguage(lang) {
  localStorage.setItem('pref-lang', lang);
  
  const currentPath = window.location.pathname;
  let currentFile = currentPath.substring(currentPath.lastIndexOf('/') + 1);
  if (!currentFile || currentFile === '/') {
    currentFile = 'index.html';
  }
  
  // Check if we are currently in the /en/ directory
  // We check if the pathname contains '/en/' or if the folder before currentFile is 'en'
  const pathSegments = currentPath.split('/');
  const isEnglishDir = pathSegments.includes('en') || window.location.href.includes('/en/');
  
  if (lang === 'en') {
    if (!isEnglishDir) {
      window.location.href = 'en/' + currentFile;
    }
  } else if (lang === 'ko') {
    if (isEnglishDir) {
      window.location.href = '../' + currentFile;
    }
  }
}

// Automatic redirect based on preference on initial load
(function() {
  const prefLang = localStorage.getItem('pref-lang');
  if (prefLang === 'en') {
    const currentPath = window.location.pathname;
    const pathSegments = currentPath.split('/');
    const isEnglishDir = pathSegments.includes('en') || window.location.href.includes('/en/');
    if (!isEnglishDir) {
      let currentFile = currentPath.substring(currentPath.lastIndexOf('/') + 1);
      if (!currentFile || currentFile === '/') {
        currentFile = 'index.html';
      }
      // Only redirect if the file actually exists in the en/ folder.
      // We will perform a redirect since we build a complete mirror site.
      window.location.href = 'en/' + currentFile;
    }
  }
})();

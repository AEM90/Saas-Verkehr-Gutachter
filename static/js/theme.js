// theme.js - tiny theme toggler that stores choice in localStorage
// Usage: call themeToggle() or use get/setTheme preferences
(function () {
  var KEY = "sv_theme";

  function setTheme(name) {
    if (name) {
      document.documentElement.setAttribute("data-theme", name);
      localStorage.setItem(KEY, name);
    } else {
      document.documentElement.removeAttribute("data-theme");
      localStorage.removeItem(KEY);
    }
  }

  function getTheme() {
    return localStorage.getItem(KEY) || null;
  }

  function init() {
    var t = getTheme();
    if (t) setTheme(t);
  }

  function toggle() {
    var current = getTheme();
    if (current === "dark") setTheme(null);
    else setTheme("dark");
  }

  // Expose to window
  window.svTheme = {
    init: init,
    setTheme: setTheme,
    getTheme: getTheme,
    toggle: toggle,
  };

  // Auto-init on DOM ready
  document.addEventListener("DOMContentLoaded", function () {
    init();
  });
})();
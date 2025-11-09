// roleGuard.js

document.addEventListener("DOMContentLoaded", () => {
  const role = localStorage.getItem("role"); // 'referrer' or 'referee'
  const path = window.location.pathname;

  // --- Define page access mapping ---
  const referrerPages = ["/referer_home", "/my_tracker"];
  const refereePages = ["/active_referals", "/trending", "/tracker"];

  // --- Access logic ---
  if (role === "referrer") {
    // if referrer tries referee pages
    if (refereePages.some(page => path.startsWith(page))) {
      window.location.href = "/access_denied";
    }
  } 
  else if (role === "referee") {
    // if referee tries referrer pages
    if (referrerPages.some(page => path.startsWith(page))) {
      window.location.href = "/access_denied";
    }
  } 
  else {
    // no role (not logged in or corrupted localStorage)
    window.location.href = "/login";
  }
});

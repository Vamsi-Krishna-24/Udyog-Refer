document.addEventListener("DOMContentLoaded", () => {
  const role = localStorage.getItem("role");
  const path = window.location.pathname;

  console.log(`✅ roleGuard loaded | Role: ${role} | Path: ${path}`);

  const referrerPages = ["/referer_home", "/my_tracker"];
  const refereePages = ["/active_referals", "/trending", "/tracker"];

  if (!role) {
    console.warn("⚠️ No role found → redirecting to login");
    window.location.href = "/login";
    return;
  }

  if (role === "referrer" && refereePages.some(page => path.startsWith(page))) {
    console.warn(`🚫 Referrer tried to access Referee page (${path}) → redirecting`);
    window.location.href = "/access_denied";
  } 
  else if (role === "referee" && referrerPages.some(page => path.startsWith(page))) {
    console.warn(`🚫 Referee tried to access Referrer page (${path}) → redirecting`);
    window.location.href = "/access_denied";
  }
});

// auth.js
(function checkAuth() {
  const token = localStorage.getItem("access_token");

  if (!token) {
    window.location.href = "/no_token";
  } else {
    fetch("/api/protected-ping/", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).then((res) => {
      if (!res.ok) {
        localStorage.removeItem("access_token");
        window.location.href = "/no_token";
      }
    });
  }
})();

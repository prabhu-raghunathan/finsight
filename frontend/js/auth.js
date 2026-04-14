const TOKEN_KEY = "finsight_token";

function saveToken(token) { localStorage.setItem(TOKEN_KEY, token); }
function getToken()       { return localStorage.getItem(TOKEN_KEY); }
function removeToken()    { localStorage.removeItem(TOKEN_KEY); }

function requireAuth() {
  const token = getToken();
  if (!token) window.location.href = "index.html";
  return token;
}

function logout() {
  removeToken();
  window.location.href = "index.html";
}
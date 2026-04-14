if (getToken()) window.location.href = "dashboard.html";

const loginBtn = document.getElementById("loginBtn");
const errorMsg = document.getElementById("errorMsg");

// Allow Enter key on password field
document.getElementById("password").addEventListener("keydown", (e) => {
  if (e.key === "Enter") doLogin();
});

loginBtn.addEventListener("click", doLogin);

async function doLogin() {
  const email    = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  errorMsg.style.display = "none";

  if (!email || !password) {
    errorMsg.textContent   = "Please enter your email and password.";
    errorMsg.style.display = "block";
    return;
  }

  loginBtn.textContent = "Signing in...";
  loginBtn.disabled    = true;

  try {
    const data = await login(email, password);
    saveToken(data.token);
    window.location.href = "dashboard.html";
  } catch (error) {
    errorMsg.textContent   = "Invalid email or password.";
    errorMsg.style.display = "block";
    loginBtn.textContent   = "Sign In";
    loginBtn.disabled      = false;
  }
}
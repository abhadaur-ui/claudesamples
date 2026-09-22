// ponytail: routes assume an existing /api/login auth endpoint and /dashboard
// route (per spec, both already exist elsewhere) — point these at the real
// paths when wiring into the actual app.
const AUTH_ENDPOINT = "/api/login";
const DASHBOARD_ROUTE = "/dashboard";

function isFormValid(email, password) {
  return Boolean(email) && Boolean(password);
}

// ponytail: outcome-only (ok/not-ok) per spec's open question on error-message
// granularity — split into per-cause messages once the PO decides.
async function attemptLogin(email, password, fetchImpl) {
  const response = await fetchImpl(AUTH_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return response.ok;
}

if (typeof document !== "undefined") {
  const form = document.getElementById("login-form");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const errorMessage = document.getElementById("error-message");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    errorMessage.hidden = true;

    if (!isFormValid(emailInput.value, passwordInput.value)) {
      return;
    }

    const ok = await attemptLogin(emailInput.value, passwordInput.value, fetch);

    if (ok) {
      window.location.href = DASHBOARD_ROUTE;
    } else {
      errorMessage.hidden = false;
    }
  });
}

if (typeof module !== "undefined") {
  module.exports = { isFormValid, attemptLogin, AUTH_ENDPOINT, DASHBOARD_ROUTE };
}

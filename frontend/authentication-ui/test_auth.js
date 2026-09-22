const assert = require("assert");
const { isFormValid, attemptLogin, AUTH_ENDPOINT, DASHBOARD_ROUTE } = require("./auth.js");

assert.strictEqual(isFormValid("a@b.com", "secret"), true);
assert.strictEqual(isFormValid("", "secret"), false);
assert.strictEqual(isFormValid("a@b.com", ""), false);
assert.strictEqual(isFormValid("", ""), false);

async function run() {
  const okFetch = async (url) => {
    assert.strictEqual(url, AUTH_ENDPOINT);
    return { ok: true };
  };
  assert.strictEqual(await attemptLogin("a@b.com", "secret", okFetch), true);

  const failFetch = async () => ({ ok: false });
  assert.strictEqual(await attemptLogin("a@b.com", "wrong", failFetch), false);

  assert.strictEqual(DASHBOARD_ROUTE, "/dashboard");

  console.log("test_auth.js: all assertions passed");
}

run();

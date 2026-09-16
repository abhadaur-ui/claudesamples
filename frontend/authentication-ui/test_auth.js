const assert = require("assert");
const { isFormValid } = require("./auth.js");

assert.strictEqual(isFormValid("a@b.com", "secret"), true);
assert.strictEqual(isFormValid("", "secret"), false);
assert.strictEqual(isFormValid("a@b.com", ""), false);
assert.strictEqual(isFormValid("", ""), false);

console.log("test_auth.js: all assertions passed");

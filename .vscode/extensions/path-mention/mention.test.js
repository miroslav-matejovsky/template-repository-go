"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const { findMention, excludeGlob } = require("./mention");

test("findMention", () => {
  const cases = [
    { text: "", want: null },
    { text: "@", want: { start: 1, query: "" } },
    { text: "see @", want: { start: 5, query: "" } },
    { text: "see @int/app", want: { start: 5, query: "int/app" } },
    { text: "see\t@main.go", want: { start: 5, query: "main.go" } },
    { text: "see @main.go ", want: null },
    { text: "mail me@example.com", want: null },
    { text: "@a @b", want: { start: 4, query: "b" } },
    { text: "@@x", want: null },
  ];
  for (const c of cases) {
    assert.deepEqual(findMention(c.text), c.want, JSON.stringify(c.text));
  }
});

test("excludeGlob", () => {
  assert.equal(excludeGlob({}, {}), undefined);
  assert.equal(excludeGlob(undefined, undefined), undefined);
  assert.equal(
    excludeGlob({ "**/.git": true, "**/tmp": false }, { "vendor/**": true, "**/.git": true, "**/*.js": { when: "$(basename).ts" } }),
    "{**/.git,vendor/**}",
  );
});

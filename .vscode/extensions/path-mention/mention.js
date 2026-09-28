// Pure logic for "@" path mentions. No VS Code dependency, so it is unit tested with node:test.

"use strict";

// "@" at line start or after whitespace (so e-mail addresses do not trigger), followed by non-space text up to the cursor.
const MENTION = /(?:^|\s)@([^\s@]*)$/;

/**
 * Finds the "@" mention that ends at the cursor.
 * @param {string} textBeforeCursor line text from line start to the cursor
 * @returns {{start: number, query: string} | null} start is the column right after "@"; null when there is no mention
 */
function findMention(textBeforeCursor) {
  const m = MENTION.exec(textBeforeCursor);
  if (!m) return null;
  return { start: textBeforeCursor.length - m[1].length, query: m[1] };
}

/**
 * Builds one exclude glob for workspace.findFiles from the files.exclude and search.exclude settings,
 * because passing an explicit exclude disables the default files.exclude handling.
 * Only patterns set to true are used; conditional ({when: ...}) and false entries are skipped.
 * @param {Record<string, unknown>} filesExclude
 * @param {Record<string, unknown>} searchExclude
 * @returns {string | undefined} "{a,b}" glob, or undefined when nothing is excluded
 */
function excludeGlob(filesExclude, searchExclude) {
  const patterns = new Set();
  for (const settings of [filesExclude, searchExclude]) {
    for (const [pattern, enabled] of Object.entries(settings || {})) {
      if (enabled === true) patterns.add(pattern);
    }
  }
  if (patterns.size === 0) return undefined;
  return `{${[...patterns].join(",")}}`;
}

module.exports = { findMention, excludeGlob };

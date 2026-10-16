import { test } from 'node:test';
import assert from 'node:assert';
import { add } from './math.js';
test('1 + 2 = 3', () => {
assert.equal(add(1, 2), 3);
});
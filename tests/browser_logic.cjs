"use strict";
const assert = require("node:assert/strict");
const {evaluateDemo} = require("../web/app.js");

const base = {
  task_id: "SYNTH-1",
  target_identifier: "SPECIMEN-1",
  primary_metric: 10,
  secondary_metric: 5,
  status_descriptor: "NOMINAL",
  is_critical_flag: false,
};
const normal = evaluateDemo(base);
assert.equal(normal.overall_urgency, "ROUTINE");
assert.equal(normal.total_alerts, 0);

const high = evaluateDemo({...base, primary_metric: 26, secondary_metric: 13, status_descriptor: "DISCORDANT"});
assert.equal(high.total_alerts, 3);
assert.equal(high.overall_urgency, "ELEVATED_RISK");

const critical = evaluateDemo({...base, is_critical_flag: true});
assert.equal(critical.overall_urgency, "CRITICAL_STAT_PANIC");
assert.equal(critical.total_alerts, 1);

assert.throws(() => evaluateDemo({...base, task_id: "Not a synthetic ID!"}), /synthetic/);
assert.throws(() => evaluateDemo({...base, primary_metric: "abc"}), /finite/);
assert.throws(() => evaluateDemo({...base, secondary_metric: Infinity}), /finite/);
assert.throws(() => evaluateDemo({...base, is_critical_flag: "false"}), /boolean/);
console.log("Browser rule tests passed.");

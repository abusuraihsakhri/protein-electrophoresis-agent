"use strict";

/**
 * Deterministic browser demonstration of the generic rule set in
 * agents/workers.py. These numbers are NOT validated clinical cutoffs.
 */
function evaluateDemo(payload) {
  const taskId = String(payload.task_id || "").trim();
  const targetId = String(payload.target_identifier || "").trim();
  const descriptor = String(payload.status_descriptor || "").trim();
  const primary = Number(payload.primary_metric);
  const secondary = Number(payload.secondary_metric);
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/.test(taskId) ||
      !/^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/.test(targetId)) {
    throw new Error("Use a synthetic task and specimen ID (letters, digits, dots, underscores or hyphens; maximum 64 characters).");
  }
  if (descriptor.length > 120) {
    throw new Error("The descriptor must not exceed 120 characters.");
  }
  if (!Number.isFinite(primary) || !Number.isFinite(secondary)) {
    throw new Error("Both measurements must be finite numbers.");
  }
  if (typeof payload.is_critical_flag !== "boolean") {
    throw new Error("The critical flag must be a boolean.");
  }

  const alerts = [];
  if (primary > 25) {
    alerts.push({
      worker: "InvariantQCWorker", urgency: "ELEVATED_RISK",
      summary: "Primary demo threshold exceeded",
      details: "Primary measurement exceeds the illustrative threshold of 25.",
    });
  }
  if (payload.is_critical_flag || secondary > 12) {
    alerts.push({
      worker: "SafetyEscalationWorker",
      urgency: payload.is_critical_flag ? "CRITICAL_STAT_PANIC" : "ELEVATED_RISK",
      summary: "Demo escalation rule matched",
      details: payload.is_critical_flag
        ? "The critical flag was manually selected."
        : "Secondary measurement exceeds the illustrative threshold of 12.",
    });
  }
  if (["DISCORDANT", "ANOMALY", "MUTANT", "VIOLATION", "FAIL", "REJECT"].some(
    word => descriptor.toUpperCase().includes(word)
  )) {
    alerts.push({
      worker: "ProtocolConformanceWorker", urgency: "ELEVATED_RISK",
      summary: "Descriptor review flag",
      details: "The entered descriptor contains a configured review keyword.",
    });
  }
  const severity = alerts.some(a => a.urgency === "CRITICAL_STAT_PANIC")
    ? "CRITICAL_STAT_PANIC"
    : alerts.length ? "ELEVATED_RISK" : "ROUTINE";
  return {
    mode: "LOCAL_DEMONSTRATION",
    task_id: taskId,
    target_identifier: targetId,
    primary_metric: primary,
    secondary_metric: secondary,
    status_descriptor: descriptor,
    critical_flag: payload.is_critical_flag,
    overall_urgency: severity,
    total_alerts: alerts.length,
    alerts,
    clinical_validation: "NONE — do not use for diagnostic, treatment, or emergency decisions",
  };
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { evaluateDemo };
}

if (typeof document !== "undefined") {
  const form = document.getElementById("auditForm");
  const output = document.getElementById("outputConsole");
  const notice = document.getElementById("statusMessage");
  const processed = document.getElementById("m-tasks");
  const flagged = document.getElementById("m-flagged");
  const exportBtn = document.getElementById("exportBtn");
  let latest = null;
  let count = 0;
  let flaggedCount = 0;

  function showError(message) {
    notice.textContent = message;
    notice.className = "notice error";
  }
  function showSuccess(message) {
    notice.textContent = message;
    notice.className = "notice success";
  }

  form.addEventListener("submit", event => {
    event.preventDefault();
    try {
      const primaryRaw = document.getElementById("primary_metric").value;
      const secondaryRaw = document.getElementById("secondary_metric").value;
      if (primaryRaw.trim() === "" || secondaryRaw.trim() === "") {
        throw new Error("Enter both measurements.");
      }
      const result = evaluateDemo({
        task_id: document.getElementById("task_id").value,
        target_identifier: document.getElementById("target_id").value,
        primary_metric: primaryRaw,
        secondary_metric: secondaryRaw,
        status_descriptor: document.getElementById("status_descriptor").value,
        is_critical_flag: document.getElementById("is_critical").checked,
      });
      latest = result;
      count += 1;
      if (result.total_alerts) flaggedCount += 1;
      processed.textContent = String(count);
      flagged.textContent = String(flaggedCount);
      output.textContent = JSON.stringify(result, null, 2);
      exportBtn.disabled = false;
      showSuccess(result.total_alerts
        ? result.total_alerts + " demonstration rule(s) matched."
        : "No demonstration rules matched. This is not a clinical normality assessment.");
    } catch (error) {
      latest = null;
      exportBtn.disabled = true;
      output.textContent = "Evaluation not performed.";
      showError(error.message || "Unable to evaluate inputs.");
    }
  });

  exportBtn.addEventListener("click", () => {
    if (!latest) return;
    const blob = new Blob([JSON.stringify(latest, null, 2) + "\n"], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "electrophoresis-demo-result.json";
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  });
}

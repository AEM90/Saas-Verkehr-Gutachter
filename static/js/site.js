// site.js - small vanilla JS helpers (mobile nav toggle + polling helper)

document.addEventListener("DOMContentLoaded", function () {
  // Mobile nav toggle
  var toggle = document.getElementById("mobile-nav-toggle");
  var navLinks = document.getElementById("nav-links");
  if (toggle && navLinks) {
    toggle.addEventListener("click", function () {
      var expanded = this.getAttribute("aria-expanded") === "true";
      this.setAttribute("aria-expanded", String(!expanded));
      if (navLinks.style.display === "flex" || navLinks.style.display === "block") {
        navLinks.style.display = "";
      } else {
        navLinks.style.display = "flex";
      }
    });
  }

  // Optional: wire polling buttons with class "poll-report"
  // <button class="poll-report" data-report-id="3" data-target="#report-status-3">Check</button>
  document.querySelectorAll(".poll-report").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var id = this.dataset.reportId;
      var target = document.querySelector(this.dataset.target);
      if (!id || !target) return;
      pollReportStatus(id, function (status, data) {
        target.textContent = status;
        if (status === "done" && data && data.download_url) {
          var a = document.createElement("a");
          a.href = data.download_url;
          a.textContent = "Download";
          a.className = "greenbutton small";
          target.appendChild(document.createTextNode(" "));
          target.appendChild(a);
        }
      });
    });
  });
});

/**
 * Simple polling helper for report status.
 * Expects a backend endpoint at /reports/<id>/status/ returning JSON: {status: "pending"|"done"|"failed", download_url: "..."}
 *
 * Usage: pollReportStatus(reportId, callback)
 * callback(status, data)
 */
function pollReportStatus(reportId, callback, intervalMs = 1500, maxAttempts = 40) {
  var attempts = 0;
  var url = "/reports/" + encodeURIComponent(reportId) + "/status/";
  var timer = setInterval(function () {
    attempts++;
    fetch(url, { credentials: "same-origin" })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var status = data.status || "pending";
        callback(status, data);
        if (status === "done" || status === "failed" || attempts >= maxAttempts) {
          clearInterval(timer);
        }
      })
      .catch(function (err) {
        console.error("pollReportStatus error", err);
        if (attempts >= maxAttempts) clearInterval(timer);
      });
  }, intervalMs);
}
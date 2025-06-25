document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("dt.sig.sig-object.py").forEach(function (dt) {
    const id = dt.getAttribute("id");
    if (!id) return;
    const span = dt.querySelector("span.sig-name.descname");
    if (!span) return;

    // Check if it's already prefixed
    const existingPrefix = dt.querySelector("span.sig-prename");
    if (existingPrefix) return;

    // Extract the last part of the id (should match name)
    const lastDot = id.lastIndexOf(".");
    if (lastDot === -1) return;

    const prefix = id.slice(0, lastDot + 1); // Include trailing dot
    const prefixElement = document.createElement("span");
    prefixElement.classList.add("sig-prename", "descclassname");
    prefixElement.textContent = prefix;

    dt.insertBefore(prefixElement, span);
  });
});

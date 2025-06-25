document.addEventListener("DOMContentLoaded", () => {
  const rows = document.querySelectorAll("table.autosummary tbody tr");

  rows.forEach(row => {
    const link = row.querySelector("td:first-child a.reference.internal");
    if (!link) return;

    // Try to extract the FQN from the anchor's href attribute
    const href = link.getAttribute("href"); // e.g., "#abjad.bind.Wrapper.annotation"
    const match = href && href.match(/^#(.+)$/);
    if (!match) return;

    const fqn = match[1]; // "abjad.bind.Wrapper.annotation"

    // Find the element containing the name (inside <code><span class="pre">...</span></code>)
    const span = link.querySelector("span.pre");
    if (span) {
      span.textContent = fqn;
    }
  });
});

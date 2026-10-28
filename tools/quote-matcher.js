// Quote audit helper (MAINTAINING.md §7, step 4a).
// Paste into the browser console (or a browser tool) on the source page, then call
//   auditQuotes(["quote one", "quote two."])
// with the quotes that `python3 tools/check.py --quotes` lists for that page.
// Each quote must appear in the page word for word, including its ending: a quote that ends
// with a full stop only matches where the source has that full stop. "…" and [editorial]
// insertions split a quote into parts, which must appear in order.
// For pages split across several URLs (forum threads), pass the combined text as `text`.
function auditQuotes(quotes, text) {
  const norm = s => s.replace(/[‘’]/g, "'").replace(/[“”]/g, '"')
    .replace(/ /g, " ").replace(/\s+/g, " ").trim();
  const page = norm(text || document.body.textContent);
  return quotes.map(q => {
    const parts = norm(q).split(/…|\.\.\.(?!\))|\[[^\]]*\]/).map(p => p.trim()).filter(p => p.length);
    let pos = 0, missing = null;
    for (const p of parts) {
      const i = page.indexOf(p, pos);
      if (i < 0) { missing = p; break; }
      pos = i + p.length;
    }
    if (!missing) return { quote: q, ok: true, next: page.slice(pos, pos + 30) };
    // Show the nearest text so the reader can see what the source really says.
    const words = missing.split(" ");
    const probe = words.slice(0, Math.min(4, words.length)).join(" ");
    const j = page.indexOf(probe);
    return { quote: q, ok: false, missing, source: j < 0 ? "(start not found)" : page.slice(j, j + missing.length + 40) };
  });
}

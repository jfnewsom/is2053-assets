/* ============================================================
   worksheet-copy.js — Clipboard buttons for study worksheets
   ------------------------------------------------------------
   Three buttons live in the .ws-copy-bar at the top of every
   worksheet page:
     - Copy as Rich Text  → writes text/html to clipboard so
                            Word/Pages/Google Docs receive
                            formatted bullets, tables, headings
     - Copy as Plain Text → writes plain text, with fill-in
                            blanks rendered as underscore lines
     - Print              → window.print() (the print CSS in
                            labs.css strips chrome and reflows
                            for paper)

   For both copy paths, the .ws-copy-bar itself is removed from
   the cloned content before serialization. ws-blank spans
   (CSS-only underlined emptiness, doesn't survive paste) get
   transformed into actual underlined space (rich) or
   underscores (plain). Visual headings (.lc-topper-title and
   .lc-h3 divs) get promoted to real h1/h2/h3 tags so Word
   gets a proper outline.

   Uses modern Clipboard API where available, with a legacy
   execCommand fallback for older browsers.
   ============================================================ */
(function () {
  'use strict';

  /* ── DOM transforms shared between rich and plain ─────────── */

  function stripCopyBar(root) {
    var bar = root.querySelector('.ws-copy-bar');
    if (bar) bar.parentNode.removeChild(bar);
  }

  function promoteHeadings(root) {
    // First .lc-topper-title → h1 (page header); rest → h2 (section headers).
    var titles = root.querySelectorAll('.lc-topper-title');
    for (var i = 0; i < titles.length; i++) {
      var tag = (i === 0) ? 'h1' : 'h2';
      var el = titles[i];
      var newEl = document.createElement(tag);
      newEl.innerHTML = el.innerHTML;
      el.parentNode.replaceChild(newEl, el);
    }
    // .lc-h3 div → real h3.
    var subs = root.querySelectorAll('.lc-h3');
    for (var j = 0; j < subs.length; j++) {
      var s = subs[j];
      var h3 = document.createElement('h3');
      h3.innerHTML = s.innerHTML;
      s.parentNode.replaceChild(h3, s);
    }
  }

  function transformForRich(root) {
    stripCopyBar(root);
    promoteHeadings(root);

    // ws-blank spans → <u> with non-breaking spaces. Word renders <u>
    // as actual underline, which is what we want for a fill-in line.
    var blanks = root.querySelectorAll('.ws-blank');
    for (var i = 0; i < blanks.length; i++) {
      var u = document.createElement('u');
      u.innerHTML = '\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0';
      blanks[i].parentNode.replaceChild(u, blanks[i]);
    }

    // Empty .ws-answer-cell cells → cells with visible space so the row
    // doesn't collapse when pasted into Word.
    var cells = root.querySelectorAll('.ws-answer-cell');
    for (var j = 0; j < cells.length; j++) {
      var c = cells[j];
      if (!c.textContent.trim()) {
        c.innerHTML = '\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0';
      }
    }

    // Material Symbols icons → drop entirely (the font doesn't exist in
    // Word/Pages/etc, so they'd just paste as ugly text like "school").
    var icons = root.querySelectorAll('.material-symbols-outlined');
    for (var k = 0; k < icons.length; k++) {
      icons[k].parentNode.removeChild(icons[k]);
    }

    // Bat City logo → drop. Renders poorly in Word (sizing/positioning)
    // and isn't needed in a fill-in printable.
    var logos = root.querySelectorAll('img[alt="Bat City Collective"]');
    for (var L = 0; L < logos.length; L++) {
      logos[L].parentNode.removeChild(logos[L]);
    }
  }

  function transformForPlain(root) {
    stripCopyBar(root);
    promoteHeadings(root);

    var blanks = root.querySelectorAll('.ws-blank');
    for (var i = 0; i < blanks.length; i++) {
      blanks[i].textContent = '__________________';
    }
    var cells = root.querySelectorAll('.ws-answer-cell');
    for (var j = 0; j < cells.length; j++) {
      var c = cells[j];
      if (!c.textContent.trim()) {
        c.textContent = '__________';
      }
    }
    var icons = root.querySelectorAll('.material-symbols-outlined');
    for (var k = 0; k < icons.length; k++) {
      icons[k].parentNode.removeChild(icons[k]);
    }
    var logos = root.querySelectorAll('img[alt="Bat City Collective"]');
    for (var L = 0; L < logos.length; L++) {
      logos[L].parentNode.removeChild(logos[L]);
    }
  }

  /* ── Get a transformed clone of the worksheet content ─────── */

  function getCloneFor(mode) {
    var src = document.querySelector('.lc-wrapper');
    if (!src) return null;
    var clone = src.cloneNode(true);
    if (mode === 'rich') transformForRich(clone);
    else transformForPlain(clone);
    return clone;
  }

  /* ── Visual feedback on the button ────────────────────────── */

  function flashSuccess(button, msg) {
    var original = button.textContent;
    button.textContent = msg;
    button.classList.add('ws-copy-btn--success');
    setTimeout(function () {
      button.textContent = original;
      button.classList.remove('ws-copy-btn--success');
    }, 1800);
  }

  function flashError(button) {
    var original = button.textContent;
    button.textContent = 'Copy failed — select and Ctrl+C';
    setTimeout(function () { button.textContent = original; }, 2400);
  }

  /* ── Clipboard writers (modern + legacy) ──────────────────── */

  function copyRichModern(html, text) {
    if (!navigator.clipboard || !window.ClipboardItem) return Promise.reject();
    var item = new ClipboardItem({
      'text/html':  new Blob([html], { type: 'text/html' }),
      'text/plain': new Blob([text], { type: 'text/plain' })
    });
    return navigator.clipboard.write([item]);
  }

  function copyTextModern(text) {
    if (!navigator.clipboard) return Promise.reject();
    return navigator.clipboard.writeText(text);
  }

  function copyHtmlLegacy(html) {
    var container = document.createElement('div');
    container.contentEditable = 'true';
    container.style.position = 'fixed';
    container.style.left = '-9999px';
    container.innerHTML = html;
    document.body.appendChild(container);
    var range = document.createRange();
    range.selectNodeContents(container);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    sel.removeAllRanges();
    document.body.removeChild(container);
    return ok;
  }

  function copyTextLegacy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    return ok;
  }

  /* ── Button handlers ──────────────────────────────────────── */

  function handleRich(button) {
    var clone = getCloneFor('rich');
    if (!clone) return;
    var html = clone.outerHTML;
    var text = clone.innerText || clone.textContent || '';

    copyRichModern(html, text).then(
      function () { flashSuccess(button, 'Copied! Paste into Word'); },
      function () {
        if (copyHtmlLegacy(html)) flashSuccess(button, 'Copied! Paste into Word');
        else flashError(button);
      }
    );
  }

  function handlePlain(button) {
    var clone = getCloneFor('plain');
    if (!clone) return;
    var text = clone.innerText || clone.textContent || '';

    copyTextModern(text).then(
      function () { flashSuccess(button, 'Copied!'); },
      function () {
        if (copyTextLegacy(text)) flashSuccess(button, 'Copied!');
        else flashError(button);
      }
    );
  }

  function handlePrint() {
    window.print();
  }

  /* ── Init ─────────────────────────────────────────────────── */

  function init() {
    var buttons = document.querySelectorAll('.ws-copy-btn');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener('click', function (e) {
        var btn = e.currentTarget;
        var mode = btn.getAttribute('data-ws-copy');
        if (mode === 'rich')  handleRich(btn);
        else if (mode === 'plain') handlePlain(btn);
        else if (mode === 'print') handlePrint();
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

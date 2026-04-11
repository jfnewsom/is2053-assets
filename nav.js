/**
 * nav.js — IS2053 Programming I
 * Top horizontal navigation bar with dropdown menus.
 *
 * Context is determined by the ?context= query parameter in the URL:
 *
 *   No parameter (direct open)   → full nav (all sections + assignments)
 *   ?context=support             → slim nav (Course, Bat City only)
 *   ?context=assignment          → no nav rendered at all
 *
 * This means the same HTML file behaves correctly whether opened
 * directly by a student or embedded in a Canvas iframe.
 */

(function () {
  'use strict';

  /* ── Context detection ──────────────────────────────────── */
  const inIframe = window.self !== window.top;
  const params   = new URLSearchParams(window.location.search);
  const ctx      = params.get('context'); // null | 'support'

  if (inIframe && ctx !== 'support') return; // assignment iframes: no nav

  const showFull = !inIframe; // direct open = full nav; support iframe = slim nav
  const suffix   = inIframe ? '?context=support' : '';

  /* ── Base URLs ──────────────────────────────────────────── */
  const BASE = 'https://jfnewsom.github.io/is2053-assets';
  const S    = BASE + '/pages/support/';
  const SC   = BASE + '/pages/scenario/';
  const L    = BASE + '/pages/labs/';
  const BX   = BASE + '/pages/bookex/';

  /* ── Fonts ──────────────────────────────────────────────── */
  if (!document.querySelector('link[href*="Roboto+Slab"]') &&
      !document.querySelector('link[href*="fonts.googleapis"]')) {
    const f = document.createElement('link');
    f.rel  = 'stylesheet';
    f.href = 'https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@700&family=Roboto:wght@400;500;700&display=swap';
    document.head.prepend(f);
  }

  /* ── Styles ─────────────────────────────────────────────── */
  const css = `
    #is2053-nav {
      position: sticky;
      top: 0;
      z-index: 9999;
      background: #0d0d0d;
      border-bottom: 1px solid #1e1e1e;
      font-family: 'Roboto', sans-serif;
      font-size: 13px;
      user-select: none;
    }
    #is2053-nav a { text-decoration: none; }

    #is2053-nav .nav-inner {
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 0 20px;
      height: 42px;
    }

    /* Logo */
    #is2053-nav .nav-logo {
      display: flex;
      align-items: center;
      gap: 10px;
      padding-right: 16px;
      margin-right: 6px;
      border-right: 1px solid #222;
      flex-shrink: 0;
      white-space: nowrap;
    }
    #is2053-nav .nav-logo-label {
      font-family: 'Roboto Slab', serif;
      font-size: 13px;
      font-weight: 700;
      color: #FFCC00;
      letter-spacing: 0.03em;
    }
    #is2053-nav .nav-logo:hover .nav-logo-label { color: #ffe033; }

    /* Dropdown menus */
    #is2053-nav .nav-menu {
      display: flex;
      align-items: center;
      gap: 2px;
      flex: 1;
    }
    #is2053-nav .nav-item { position: relative; }
    #is2053-nav .nav-trigger {
      display: flex;
      align-items: center;
      gap: 5px;
      color: #778087;
      padding: 0 10px;
      height: 42px;
      cursor: pointer;
      font-weight: 500;
      white-space: nowrap;
      transition: color 0.12s, background 0.12s;
      border-radius: 3px;
    }
    #is2053-nav .nav-trigger:hover {
      color: #F5F5F5;
      background: rgba(255,255,255,0.04);
    }
    #is2053-nav .nav-caret {
      font-size: 8px;
      opacity: 0.35;
      transition: transform 0.12s, opacity 0.12s;
    }
    #is2053-nav .nav-item:hover .nav-caret {
      transform: rotate(180deg);
      opacity: 0.7;
    }

    /* Dropdown panel */
    #is2053-nav .nav-dropdown {
      display: none;
      position: absolute;
      top: calc(100% + 1px);
      left: 0;
      min-width: 220px;
      background: #111;
      border: 1px solid #222;
      border-top: 2px solid #FFCC00;
      padding: 6px 0;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }
    #is2053-nav .nav-item:hover .nav-dropdown { display: block; }

    #is2053-nav .nav-dropdown a {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 16px;
      color: #778087;
      font-size: 13px;
      transition: color 0.1s, background 0.1s;
      line-height: 1.3;
    }
    #is2053-nav .nav-dropdown a:hover {
      color: #F5F5F5;
      background: rgba(255,255,255,0.04);
    }
    #is2053-nav .nav-dropdown a:hover .drop-dot { opacity: 1; }

    #is2053-nav .drop-dot {
      width: 5px;
      height: 5px;
      border-radius: 50%;
      flex-shrink: 0;
      opacity: 0.6;
    }
    #is2053-nav .drop-label {
      font-family: 'Roboto Slab', serif;
      font-size: 9px;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #FFCC00;
      padding: 8px 16px 3px 16px;
    }
    #is2053-nav .drop-divider {
      border: none;
      border-top: 1px solid #1a1a1a;
      margin: 4px 0;
    }
    #is2053-nav .drop-sub {
      font-size: 9px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: #FFCC00;
      padding: 6px 16px 2px 16px;
    }

    /* Right-side actions */
    #is2053-nav .nav-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }
    #is2053-nav .nav-zoom-btn {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(57,255,20,0.08);
      color: #39FF14 !important;
      border: 1px solid rgba(57,255,20,0.25);
      padding: 5px 12px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      white-space: nowrap;
      transition: background 0.12s;
      flex-shrink: 0;
    }
    #is2053-nav .nav-zoom-btn:hover {
      background: rgba(57,255,20,0.15);
      text-decoration: none !important;
    }

    /* Discord button */
    #is2053-nav .nav-discord {
      display: flex;
      align-items: center;
      gap: 6px;
      background: #FFCC00;
      color: #000000 !important;
      padding: 5px 12px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      white-space: nowrap;
      transition: background 0.12s;
      flex-shrink: 0;
      border-radius: 3px;
    }
    #is2053-nav .nav-discord:hover { background: #ffe033; }

    /* Dot color variants */
    .dd-yellow { background: #FFCC00; }
    .dd-green  { background: #39FF14; }
    .dd-cyan   { background: #00FFFF; }
    .dd-purple { background: #BF40FF; }
    .dd-orange { background: #FF6B1A; }

    /* ── Injected footer ─────────────────────────────────── */
    .site-footer {
      border-top: 1px solid #e0e4ef;
      padding: 24px 40px 20px 40px;
      margin-top: 0;
      text-align: center;
      background: #fff;
    }
    .site-footer__logo {
      height: 48px;
      display: block;
      margin: 0 auto 16px auto;
    }
    .site-footer__citation {
      display: inline-flex;
      align-items: baseline;
      gap: 10px;
      border: 1px solid #2a2a2a;
      border-left: 3px solid #BF40FF;
      padding: 6px 14px;
      margin-bottom: 14px;
    }
    .site-footer__citation-label {
      font-family: 'Roboto', sans-serif;
      font-size: 9px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: #BF40FF;
      white-space: nowrap;
    }
    .site-footer__citation-text {
      font-family: 'Roboto', sans-serif;
      font-size: 11px;
      color: #555;
    }
    .site-footer__copyright {
      font-family: 'Roboto', sans-serif;
      font-size: 11px;
      color: #888;
    }
  `;

  /* ── Helper: dropdown link ──────────────────────────────── */
  function link(label, url, dotClass, external) {
    const ext = external ? ' target="_blank" rel="noopener"' : '';
    return `<a href="${url}"${ext}>
      <span class="drop-dot ${dotClass}"></span>${label}
    </a>`;
  }

  /* ── Nav HTML ───────────────────────────────────────────── */
  const modulesDropdown = showFull ? `
    <div class="nav-item">
      <div class="nav-trigger">Modules <span class="nav-caret">&#9660;</span></div>
      <div class="nav-dropdown">
        <div class="drop-label">Module Overviews</div>
        <div class="drop-sub">Module 1 &mdash; Getting Started</div>
        ${link('Overview',         S + 'module-1-overview.html' + suffix,         'dd-yellow')}
        ${link('Study Worksheet',  S + 'module-1-study-worksheet.html' + suffix,  'dd-yellow')}
        <div class="drop-sub">Module 2 &mdash; The Journey Begins</div>
        ${link('Overview',         S + 'module-2-overview.html' + suffix,         'dd-yellow')}
        ${link('Study Worksheet',  S + 'module-2-study-worksheet.html' + suffix,  'dd-yellow')}
        <div class="drop-sub">Module 3 &mdash; Keeping Track</div>
        ${link('Overview',         S + 'module-3-overview.html' + suffix,         'dd-yellow')}
        ${link('Study Worksheet',  S + 'module-3-study-worksheet.html' + suffix,  'dd-yellow')}
        <div class="drop-sub">Module 4 &mdash; Smarter Code</div>
        ${link('Overview',         S + 'module-4-overview.html' + suffix,         'dd-yellow')}
        ${link('Study Worksheet',  S + 'module-4-study-worksheet.html' + suffix,  'dd-yellow')}
        <div class="drop-sub">Module 5 &mdash; Ship It</div>
        ${link('Overview',         S + 'module-5-overview.html' + suffix,         'dd-yellow')}
        ${link('Study Worksheet',  S + 'module-5-study-worksheet.html' + suffix,  'dd-yellow')}
      </div>
    </div>` : '';

  const labsDropdown = showFull ? `
    <div class="nav-item">
      <div class="nav-trigger">Labs <span class="nav-caret">&#9660;</span></div>
      <div class="nav-dropdown">
        <div class="drop-label">Assignment Sheets</div>
        <div class="drop-sub">Module 1</div>
        ${link('Lab 1-1', L + 'lab-1-1.html' + suffix, 'dd-cyan')}
        ${link('Lab 1-2', L + 'lab-1-2.html' + suffix, 'dd-cyan')}
        ${link('Lab 1-3', L + 'lab-1-3.html' + suffix, 'dd-cyan')}
        <div class="drop-sub">Module 2</div>
        ${link('Lab 2-1', L + 'lab-2-1.html' + suffix, 'dd-cyan')}
        ${link('Lab 2-2', L + 'lab-2-2.html' + suffix, 'dd-cyan')}
        ${link('Lab 2-3', L + 'lab-2-3.html' + suffix, 'dd-cyan')}
        <div class="drop-sub">Module 3</div>
        ${link('Lab 3-1', L + 'lab-3-1.html' + suffix, 'dd-cyan')}
        ${link('Lab 3-2', L + 'lab-3-2.html' + suffix, 'dd-cyan')}
        ${link('Lab 3-3', L + 'lab-3-3.html' + suffix, 'dd-cyan')}
        <div class="drop-sub">Module 4</div>
        ${link('Lab 4-1', L + 'lab-4-1.html' + suffix, 'dd-cyan')}
        ${link('Lab 4-2', L + 'lab-4-2.html' + suffix, 'dd-cyan')}
        ${link('Lab 4-3', L + 'lab-4-3.html' + suffix, 'dd-cyan')}
        <div class="drop-sub">Module 5</div>
        ${link('Lab 5-1', L + 'lab-5-1.html' + suffix, 'dd-cyan')}
        ${link('Lab 5-2', L + 'lab-5-2.html' + suffix, 'dd-cyan')}
      </div>
    </div>` : '';

  const bookexDropdown = showFull ? `
    <div class="nav-item">
      <div class="nav-trigger">BookEx <span class="nav-caret">&#9660;</span></div>
      <div class="nav-dropdown">
        <div class="drop-label">Book Exercises</div>
        ${link('BookEx Overview', S + 'bookex-overview.html' + suffix, 'dd-purple')}
        <div class="drop-sub">Module 1 &mdash; Ch. 2&ndash;3</div>
        ${link('Chapter 2',  BX + 'BookExCH02.html' + suffix, 'dd-purple')}
        ${link('Chapter 3',  BX + 'BookExCH03.html' + suffix, 'dd-purple')}
        <div class="drop-sub">Module 2 &mdash; Ch. 4&ndash;5</div>
        ${link('Chapter 4',  BX + 'BookExCH04.html' + suffix, 'dd-purple')}
        ${link('Chapter 5',  BX + 'BookExCH05.html' + suffix, 'dd-purple')}
        <div class="drop-sub">Module 3 &mdash; Ch. 6&ndash;7</div>
        ${link('Chapter 6',  BX + 'BookExCH06.html' + suffix, 'dd-purple')}
        ${link('Chapter 7',  BX + 'BookExCH07.html' + suffix, 'dd-purple')}
        <div class="drop-sub">Module 4 &mdash; Ch. 8&ndash;9</div>
        ${link('Chapter 8',  BX + 'BookExCH08.html' + suffix, 'dd-purple')}
        ${link('Chapter 9',  BX + 'BookExCH09.html' + suffix, 'dd-purple')}
        <div class="drop-sub">Module 5 &mdash; Ch. 10</div>
        ${link('Chapter 10', BX + 'BookExCH10.html' + suffix, 'dd-purple')}
      </div>
    </div>` : '';

  const navHTML = `
    <div class="nav-inner">
      <a class="nav-logo" href="${S}home.html">
        <span class="nav-logo-label">IS2053</span>
      </a>

      <div class="nav-menu">

        <div class="nav-item">
          <div class="nav-trigger">Course <span class="nav-caret">&#9660;</span></div>
          <div class="nav-dropdown">
            <div class="drop-label">Course Info</div>
            ${link('Home',            S + 'home.html' + suffix,            'dd-yellow')}
            ${link('Start Here',      S + 'start-here.html' + suffix,      'dd-yellow')}
            ${link('Syllabus',        'https://utsa.simplesyllabus.com/doc/xvcdfi182/Spring-2026-IS-2053-ON1-Programming-I?mode=view', 'dd-yellow', true)}
            ${link('Grading Info',    S + 'grading-info.html' + suffix,    'dd-yellow')}
            ${link('Course Schedule', S + 'course-schedule.html' + suffix, 'dd-yellow')}
            ${link('Zoom Sessions',   S + 'zoom-sessions.html' + suffix,   'dd-yellow')}
            <div class="drop-label">Support Resources</div>
            ${link('Assignment Overview', S + 'assignment-overview.html' + suffix, 'dd-green')}
            ${link('CodeGrade Guide',     S + 'codegrade-guide.html' + suffix,     'dd-green')}
            ${link('Flake8 Guide',        S + 'flake8-guide.html' + suffix,        'dd-green')}
            ${link('How To Get Help',     S + 'how-to-get-help.html' + suffix,     'dd-green')}
            ${link('Discord',             S + 'discord.html' + suffix,             'dd-green')}
            ${link('Stretch Goals',       S + 'stretch-goals.html' + suffix,       'dd-green')}
            ${link('AI Policy',           S + 'ai-policy.html' + suffix,           'dd-green')}
            ${link('Practice Archive',    S + 'practice-archive.html' + suffix,    'dd-green')}
            <div class="drop-label">External Tools</div>
            ${link('Python Docs', 'https://www.python.org/downloads/',                    'dd-cyan', true)}
            ${link('VS Code',     'https://code.visualstudio.com/download',               'dd-cyan', true)}
            ${link('Calendly',    'https://calendly.com/john-newsom-utsa/student-meeting', 'dd-cyan', true)}
          </div>
        </div>

        <div class="nav-item">
          <div class="nav-trigger">Bat City <span class="nav-caret">&#9660;</span></div>
          <div class="nav-dropdown">
            <div class="drop-label">Game World</div>
            ${link('The Scenario',      SC + 'the-scenario.html' + suffix,      'dd-orange')}
            ${link('Texas Highway Map', SC + 'texas-highway-map.html' + suffix, 'dd-orange')}
          </div>
        </div>

        ${modulesDropdown}
        ${labsDropdown}
        ${bookexDropdown}

        <div class="nav-item">
          <div class="nav-trigger">Reading <span class="nav-caret">&#9660;</span></div>
          <div class="nav-dropdown">
            <div class="drop-label">Reading Guide</div>
            <div class="drop-sub">Module 1 &mdash; Ch. 2&ndash;3</div>
            ${link('Chapter 2',  S + 'reading-ch02.html' + suffix, 'dd-orange')}
            ${link('Chapter 3',  S + 'reading-ch03.html' + suffix, 'dd-orange')}
            <div class="drop-sub">Module 2 &mdash; Ch. 4&ndash;5</div>
            ${link('Chapter 4',  S + 'reading-ch04.html' + suffix, 'dd-orange')}
            ${link('Chapter 5',  S + 'reading-ch05.html' + suffix, 'dd-orange')}
            <div class="drop-sub">Module 3 &mdash; Ch. 6&ndash;7</div>
            ${link('Chapter 6',  S + 'reading-ch06.html' + suffix, 'dd-orange')}
            ${link('Chapter 7',  S + 'reading-ch07.html' + suffix, 'dd-orange')}
            <div class="drop-sub">Module 4 &mdash; Ch. 8&ndash;9</div>
            ${link('Chapter 8',  S + 'reading-ch08.html' + suffix, 'dd-orange')}
            ${link('Chapter 9',  S + 'reading-ch09.html' + suffix, 'dd-orange')}
            <div class="drop-sub">Module 5 &mdash; Ch. 10</div>
            ${link('Chapter 10', S + 'reading-ch10.html' + suffix, 'dd-orange')}
          </div>
        </div>

      </div>

      <div class="nav-actions" id="is2053-nav-actions"></div>
      <a class="nav-discord" href="${S}discord.html">Discord</a>
    </div>`;

  /* ── Zoom session time check ────────────────────────────── */
  function checkZoomActive() {
    try {
      const ct   = new Date(new Date().toLocaleString('en-US', { timeZone: 'America/Chicago' }));
      const day  = ct.getDay();
      const mins = ct.getHours() * 60 + ct.getMinutes();
      const active = day === 2 && mins >= 1065 && mins <= 1155;
      const el = document.getElementById('is2053-nav-actions');
      if (el && active) {
        el.innerHTML =
          '<a class="nav-zoom-btn" href="https://utsa.zoom.us/j/97617245124"' +
          ' target="_blank" rel="noopener">&#9679; Join Zoom</a>';
      }
    } catch(e) {}
  }

  /* ── Inject styles + nav ────────────────────────────────── */
  function mount() {
    const style = document.createElement('style');
    style.id = 'is2053-nav-styles';
    style.textContent = css;
    document.head.appendChild(style);

    // Apple Touch Icon for Safari bookmarks/favorites
    if (!document.querySelector('link[rel="apple-touch-icon"]')) {
      const ati = document.createElement('link');
      ati.rel = 'apple-touch-icon';
      ati.setAttribute('sizes', '180x180');
      ati.href = 'https://jfnewsom.github.io/is2053-assets/apple-touch-icon.png';
      document.head.appendChild(ati);
    }

    const nav = document.createElement('nav');
    nav.id = 'is2053-nav';
    nav.setAttribute('aria-label', 'Course navigation');
    nav.innerHTML = navHTML;
    document.body.insertBefore(nav, document.body.firstChild);

    checkZoomActive();

    const footer = document.createElement('footer');
    footer.className = 'site-footer';
    footer.innerHTML =
      '<img class="site-footer__logo"' +
      ' src="https://jfnewsom.github.io/is2053-assets/branding/UTSanAntonio_H_Logo_Dual_TM_RGB.png"' +
      ' alt="UT San Antonio">' +
      '<div class="site-footer__citation">' +
      '<span class="site-footer__citation-label">Textbook</span>' +
      '<span class="site-footer__citation-text"><em>Starting Out with Python</em>, 6th Edition' +
      ' &middot; Tony Gaddis &middot; Pearson &middot; ISBN 978-0-13-787120-9</span>' +
      '</div>' +
      '<div class="site-footer__copyright">' +
      '&copy; 2026 The University of Texas at San Antonio. Developed by John Newsom' +
      ' for IS2053: Programming I (Python). All rights reserved.' +
      '</div>';
    document.body.appendChild(footer);
  }

  if (document.body) {
    mount();
  } else {
    document.addEventListener('DOMContentLoaded', mount);
  }

})();
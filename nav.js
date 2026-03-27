/**
 * nav.js — IS2053 Programming I
 * Injects shared sidebar navigation into all course pages.
 *
 * Behavior:
 *   Standalone (direct link)               → full nav (all sections)
 *   In iframe + site-context="support"     → slim nav (support + scenario only)
 *   In iframe + site-context="assignment"  → no nav rendered
 */

(function () {
  'use strict';

  /* ── Context detection ──────────────────────────────────── */
  const inIframe = window.self !== window.top;
  const ctxMeta  = document.querySelector('meta[name="site-context"]');
  const ctx      = ctxMeta ? ctxMeta.getAttribute('content') : 'support';

  if (inIframe && ctx === 'assignment') return;

  /* ── Base URLs ──────────────────────────────────────────── */
  const BASE = 'https://jfnewsom.github.io/is2053-assets';
  const S    = BASE + '/pages/support/';
  const SC   = BASE + '/pages/scenario/';
  const L    = BASE + '/pages/labs/';
  const BX   = BASE + '/pages/bookex/';

  /* ── Helpers ────────────────────────────────────────────── */
  const here = window.location.href;

  function isActive(url) {
    if (!url) return false;
    return here.includes(url.replace(BASE, '').replace(/^\//, ''));
  }

  function li(label, url, external) {
    const cls = isActive(url) ? ' class="nav-active"' : '';
    const ext = external ? ' target="_blank" rel="noopener"' : '';
    const arr = external ? ' <span class="nav-ext">&#8599;</span>' : '';
    return `<li><a href="${url}"${ext}${cls}>${label}${arr}</a></li>`;
  }

  function group(label, items) {
    return `<div class="nav-group">
      <div class="nav-group__label">${label}</div>
      <ul>${items}</ul>
    </div>`;
  }

  /* ── Nav sections ───────────────────────────────────────── */
  const courseLinks = group('Course', [
    li('Home',            S + 'home.html'),
    li('Start Here',      S + 'start-here.html'),
    li('Syllabus',        'https://utsa.simplesyllabus.com/doc/xvcdfi182/Spring-2026-IS-2053-ON1-Programming-I?mode=view', true),
    li('Grading Info',    S + 'grading-info.html'),
    li('Course Schedule', S + 'course-schedule.html'),
    li('Zoom Sessions',   S + 'zoom-sessions.html'),
  ].join(''));

  const resourceLinks = group('Resources', [
    li('Assignment Overview', S + 'assignment-overview.html'),
    li('CodeGrade Guide',     S + 'codegrade-guide.html'),
    li('Discord',             S + 'discord.html'),
    li('Flake8 Guide',        S + 'flake8-guide.html'),
    li('How To Get Help',     S + 'how-to-get-help.html'),
    li('Stretch Goals',       S + 'stretch-goals.html'),
  ].join(''));

  const gameLinks = group('The Game', [
    li('The Scenario',      SC + 'the-scenario.html'),
    li('Texas Highway Map', SC + 'texas-highway-map.html'),
  ].join(''));

  const labLinks = group('Labs', [
    '<li class="nav-sub">Module 1</li>',
    li('Lab 1-1', L + 'lab-1-1.html'),
    li('Lab 1-2', L + 'lab-1-2.html'),
    li('Lab 1-3', L + 'lab-1-3.html'),
    '<li class="nav-sub">Module 2</li>',
    li('Lab 2-1', L + 'lab-2-1.html'),
    li('Lab 2-2', L + 'lab-2-2.html'),
    li('Lab 2-3', L + 'lab-2-3.html'),
    '<li class="nav-sub">Module 3</li>',
    li('Lab 3-1', L + 'lab-3-1.html'),
    li('Lab 3-2', L + 'lab-3-2.html'),
    li('Lab 3-3', L + 'lab-3-3.html'),
    '<li class="nav-sub">Module 4</li>',
    li('Lab 4-1', L + 'lab-4-1.html'),
    li('Lab 4-2', L + 'lab-4-2.html'),
    li('Lab 4-3', L + 'lab-4-3.html'),
    '<li class="nav-sub">Module 5</li>',
    li('Lab 5-1', L + 'lab-5-1.html'),
    li('Lab 5-2', L + 'lab-5-2.html'),
    li('Lab 5-3', L + 'lab-5-3.html'),
  ].join(''));

  const bookexLinks = group('BookEx', [
    li('Chapter 2',  BX + 'BookExCH02.html'),
    li('Chapter 3',  BX + 'BookExCH03.html'),
    li('Chapter 4',  BX + 'BookExCH04.html'),
    li('Chapter 5',  BX + 'BookExCH05.html'),
    li('Chapter 6',  BX + 'BookExCH06.html'),
    li('Chapter 7',  BX + 'BookExCH07.html'),
    li('Chapter 8',  BX + 'BookExCH08.html'),
    li('Chapter 9',  BX + 'BookExCH09.html'),
    li('Chapter 10', BX + 'BookExCH10.html'),
    li('Chapter 11', BX + 'BookExCH11.html'),
  ].join(''));

  const toolLinks = group('Tools', [
    li('Python Docs', 'https://www.python.org/downloads/', true),
    li('VS Code',     'https://code.visualstudio.com/download', true),
    li('Calendly',    'https://calendly.com/john-newsom-utsa/student-meeting', true),
  ].join(''));

  const showFull = !inIframe;

  const navHTML = `
    <nav class="site-nav" aria-label="Course navigation">
      <div class="site-nav__logo-wrap">
        <a href="${S}home.html">
          <img src="${BASE}/branding/BatCity-logo-on-black.svg"
               alt="Bat City Collective" class="site-nav__logo">
        </a>
        <div class="site-nav__course-label">IS2053 &mdash; Spring 2026</div>
      </div>
      <div class="site-nav__links">
        ${courseLinks}
        ${resourceLinks}
        ${gameLinks}
        ${showFull ? labLinks  : ''}
        ${showFull ? bookexLinks : ''}
        ${toolLinks}
      </div>
    </nav>`;

  /* ── Injected styles ────────────────────────────────────── */
  const css = `
    body.has-nav {
      display: flex;
      flex-direction: row;
      min-height: 100vh;
      background: #0a0a0a;
    }

    .site-nav {
      width: 200px;
      min-width: 200px;
      background: #0d0d0d;
      border-right: 1px solid #1e1e1e;
      min-height: 100vh;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
      overflow-x: hidden;
      flex-shrink: 0;
      z-index: 50;
      scrollbar-width: thin;
      scrollbar-color: #222 #0d0d0d;
    }
    .site-nav::-webkit-scrollbar { width: 3px; }
    .site-nav::-webkit-scrollbar-thumb { background: #222; }

    .site-nav__logo-wrap {
      padding: 16px 14px 12px 14px;
      border-bottom: 1px solid #1a1a1a;
      margin-bottom: 8px;
    }
    .site-nav__logo {
      width: 120px;
      height: auto;
      display: block;
      margin-bottom: 8px;
      opacity: 0.85;
    }
    .site-nav__course-label {
      font-family: 'Roboto', sans-serif;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: #3a3a3a;
    }

    .site-nav__links { padding: 0 0 40px 0; }

    .nav-group { margin-bottom: 2px; }

    .nav-group__label {
      font-family: 'Roboto Slab', serif;
      font-weight: 700;
      font-size: 10px;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: #FFCC00;
      padding: 10px 14px 4px 14px;
    }

    .nav-group ul {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    .nav-group ul li a {
      display: block;
      padding: 5px 14px;
      font-family: 'Roboto', sans-serif;
      font-size: 12px;
      font-weight: 400;
      color: #778087;
      text-decoration: none;
      border-left: 2px solid transparent;
      transition: color 0.12s, background 0.12s;
      line-height: 1.4;
    }
    .nav-group ul li a:hover {
      color: #F5F5F5;
      background: rgba(255,204,0,0.05);
      border-left-color: #FFCC00;
      text-decoration: none;
    }
    .nav-group ul li a.nav-active {
      color: #FFCC00;
      border-left-color: #FFCC00;
      background: rgba(255,204,0,0.07);
      font-weight: 700;
    }

    li.nav-sub {
      font-family: 'Roboto', sans-serif;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: #2a2a2a;
      padding: 7px 14px 2px 14px;
      list-style: none;
    }

    .nav-ext {
      font-size: 10px;
      opacity: 0.4;
      margin-left: 2px;
    }

    .site-content {
      flex: 1;
      min-width: 0;
      overflow-x: hidden;
    }
  `;

  /* ── Inject on DOMContentLoaded ─────────────────────────── */
  function inject() {
    const style = document.createElement('style');
    style.id = 'nav-js-styles';
    style.textContent = css;
    document.head.appendChild(style);

    // Ensure Roboto Slab is available if labs.css isn't already loaded
    if (!document.querySelector('link[href*="Roboto+Slab"]') &&
        !document.querySelector('link[href*="fonts.googleapis"]')) {
      const font = document.createElement('link');
      font.rel  = 'stylesheet';
      font.href = 'https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@700&family=Roboto:wght@400;700&display=swap';
      document.head.prepend(font);
    }

    // Wrap existing body children in .site-content
    const content = document.createElement('div');
    content.className = 'site-content';
    while (document.body.firstChild) {
      content.appendChild(document.body.firstChild);
    }

    const wrap = document.createElement('div');
    wrap.innerHTML = navHTML.trim();
    const navEl = wrap.firstChild;

    document.body.appendChild(navEl);
    document.body.appendChild(content);
    document.body.classList.add('has-nav');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }

})();

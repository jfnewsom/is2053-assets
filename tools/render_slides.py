"""
render_slides.py — Bat City Noir PNG Renderer Engine
IS2053 Programming I | UT San Antonio

Generates 1736x648 RGBA code and output PNGs for Keynote slide decks.
Fonts are fetched automatically from the course GitHub repo if not found locally.

PUBLIC API
----------
    render_code(code, label, filename, out_dir)
    render_output(text, label, filename, out_dir)

USAGE IN A WEEK SCRIPT
----------------------
    import sys
    sys.path.insert(0, '/path/to/tools')   # or fetch render_slides.py from repo first
    from render_slides import render_code, render_output

    OUT = '/home/claude/week11_pngs'

    render_code(
        code=\"\"\"print('Hello, Texas!')\"\"\",
        label='Slide 3 – Hello World',
        filename='slide03_hello.png',
        out_dir=OUT
    )

    render_output(
        text='Hello, Texas!',
        label='Slide 3b – Expected Output',
        filename='slide03b_hello_output.png',
        out_dir=OUT
    )
"""

import os
import re
import base64
import urllib.request
import json

from PIL import Image, ImageDraw, ImageFont
from pygments import lex
from pygments.lexers import Python3Lexer
from pygments.token import Token

# ── Canvas constants ──────────────────────────────────────────────
W, H       = 1736, 648
PAD_X      = 44
PAD_Y      = 32
BORDER     = 2
RADIUS     = 14
FONT_SIZE  = 27
LINE_H     = 40

# ── Bat City Noir palette ─────────────────────────────────────────
BG         = (0,   0,   0,   255)
BORDER_CLR = (255, 204, 0,   255)   # #FFCC00
DEFAULT    = (245, 245, 245)         # #F5F5F5
COMMENT    = (106, 115, 125)         # #6A737D
KEYWORD    = (255, 107, 26)          # #FF6B1A
STRING     = (57,  255, 20)          # #39FF14
BUILTIN    = (0,   255, 255)         # #00FFFF
FUNCTION   = (255, 204, 0)           # #FFCC00
NUMBER     = (191, 64,  255)         # #BF40FF
FSTRING_I  = (0,   255, 255)         # #00FFFF
LABEL_CLR  = (106, 115, 125)         # #6A737D

# ── Repo font paths ───────────────────────────────────────────────
_REPO      = "jfnewsom/is2053-assets"
_FONT_REG_REPO  = "tools/fonts/RobotoMono.ttf"
_FONT_ITAL_REPO = "tools/fonts/RobotoMono-Italic.ttf"

# Local cache (same directory as this script)
_SCRIPT_DIR     = os.path.dirname(os.path.abspath(__file__))
_FONT_REG_LOCAL  = os.path.join(_SCRIPT_DIR, "fonts", "RobotoMono.ttf")
_FONT_ITAL_LOCAL = os.path.join(_SCRIPT_DIR, "fonts", "RobotoMono-Italic.ttf")


# ── Font bootstrap ────────────────────────────────────────────────

def _fetch_font_from_repo(repo_path, local_path):
    """Fetch a binary file from GitHub via the API and save it locally."""
    url = f"https://api.github.com/repos/{_REPO}/contents/{repo_path}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(base64.b64decode(data["content"]))
    print(f"  fetched {os.path.basename(local_path)} from repo")


def _ensure_fonts():
    """Return (font_reg_path, font_ital_path), fetching from repo if needed."""
    for local, repo in [
        (_FONT_REG_LOCAL,  _FONT_REG_REPO),
        (_FONT_ITAL_LOCAL, _FONT_ITAL_REPO),
    ]:
        if not os.path.exists(local):
            print(f"  Font not found locally, fetching from repo: {repo}")
            _fetch_font_from_repo(repo, local)
    return _FONT_REG_LOCAL, _FONT_ITAL_LOCAL


# ── Internal helpers ──────────────────────────────────────────────

def _token_color(ttype):
    checks = [
        (Token.Comment,                COMMENT),
        (Token.Keyword,                KEYWORD),
        (Token.Keyword.Namespace,      KEYWORD),
        (Token.Name.Builtin,           BUILTIN),
        (Token.Name.Builtin.Pseudo,    BUILTIN),
        (Token.Name.Function,          FUNCTION),
        (Token.Name.Function.Magic,    FUNCTION),
        (Token.Name.Decorator,         FUNCTION),
        (Token.Name.Class,             FUNCTION),
        (Token.Literal.String,         STRING),
        (Token.Literal.String.Affix,   STRING),
        (Token.Literal.String.Interpol, FSTRING_I),
        (Token.Literal.Number,         NUMBER),
        (Token.Operator,               BUILTIN),
    ]
    for base, color in checks:
        if ttype is base or ttype in base:
            return color
    return DEFAULT


def _add_scanlines(img):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for y in range(0, H, 2):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 5))
    return Image.alpha_composite(img, overlay)


def _make_canvas():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, W-1, H-1], radius=RADIUS, fill=BG)
    d.rounded_rectangle(
        [BORDER//2, BORDER//2, W-1-BORDER//2, H-1-BORDER//2],
        radius=RADIUS, outline=BORDER_CLR, width=BORDER,
    )
    return img


def _draw_label(d, label, font_label):
    tw = d.textlength(label, font=font_label)
    d.text((W - PAD_X - tw, PAD_Y - 12), label, font=font_label, fill=LABEL_CLR)


def _colorize_output_line(text):
    """Return list of (color, segment) for one line of program output."""
    if re.match(r"^\s*[=\-]{3,}\s*$", text):
        return [(BUILTIN, text)]
    segments = []
    pos = 0
    leading_dash = re.match(r"^(\s*-\s)", text)
    if leading_dash:
        segments.append((BUILTIN, leading_dash.group(1)))
        pos = leading_dash.end()
    for m in re.finditer(r"\d+\.?\d*", text[pos:]):
        abs_start = pos + m.start()
        abs_end   = pos + m.end()
        if abs_start > pos:
            segments.append((DEFAULT, text[pos:abs_start]))
        segments.append((NUMBER, m.group()))
        pos = abs_end
    if pos < len(text):
        segments.append((DEFAULT, text[pos:]))
    return segments if segments else [(DEFAULT, text)]


# ── Public API ────────────────────────────────────────────────────

def render_code(code, label, filename, out_dir):
    """
    Render a Python code string to a Bat City Noir PNG.

    Parameters
    ----------
    code     : str   — Python source code to highlight
    label    : str   — Slide label shown top-right (e.g. 'Slide 4a – .upper()')
    filename : str   — Output filename (e.g. 'slide04a_upper.png')
    out_dir  : str   — Directory to write the PNG into
    """
    os.makedirs(out_dir, exist_ok=True)
    font_reg_path, font_ital_path = _ensure_fonts()

    font_reg   = ImageFont.truetype(font_reg_path,   FONT_SIZE)
    font_ital  = ImageFont.truetype(font_ital_path,  FONT_SIZE)
    font_label = ImageFont.truetype(font_reg_path,   16)

    img = _make_canvas()
    d   = ImageDraw.Draw(img)
    _draw_label(d, label, font_label)

    x, y = PAD_X, PAD_Y + 18
    for ttype, value in lex(code, Python3Lexer()):
        if value == "\n":
            x  = PAD_X
            y += LINE_H
            continue
        value = value.replace("\t", "    ")
        font  = font_ital if ttype in Token.Comment else font_reg
        color = _token_color(ttype)
        parts = value.split("\n")
        for i, part in enumerate(parts):
            if part:
                d.text((x, y), part, font=font, fill=color)
                x += d.textlength(part, font=font)
            if i < len(parts) - 1:
                x  = PAD_X
                y += LINE_H

    _add_scanlines(img).save(os.path.join(out_dir, filename), "PNG")
    print(f"  OK  {filename}")


def render_output(text, label, filename, out_dir):
    """
    Render plain program output to a Bat City Noir PNG.
    Numbers are highlighted purple; separator lines and bullets are cyan.

    Parameters
    ----------
    text     : str   — Program output text (newline-separated lines)
    label    : str   — Slide label shown top-right
    filename : str   — Output filename
    out_dir  : str   — Directory to write the PNG into
    """
    os.makedirs(out_dir, exist_ok=True)
    font_reg_path, _ = _ensure_fonts()

    font_reg   = ImageFont.truetype(font_reg_path, FONT_SIZE)
    font_label = ImageFont.truetype(font_reg_path, 16)

    img = _make_canvas()
    d   = ImageDraw.Draw(img)
    _draw_label(d, label, font_label)

    y = PAD_Y + 18
    for line in text.split("\n"):
        x = PAD_X
        for color, seg in _colorize_output_line(line):
            d.text((x, y), seg, font=font_reg, fill=color)
            x += d.textlength(seg, font=font_reg)
        y += LINE_H

    _add_scanlines(img).save(os.path.join(out_dir, filename), "PNG")
    print(f"  OK  {filename}")

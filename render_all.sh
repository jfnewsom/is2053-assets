#!/bin/bash
# render_all.sh - Render the whole IS2053 site, then guard it.
#
# Matches the IS3513 render_all.sh idiom so the two courses work the same way.
# Two steps exist here that 3513 does not need:
#   render_variant.py  builds the face-to-face mirror, and must run LAST so it
#                      copies final pages/ output
#   check_style.py     measures RENDERED html, so it must run after everything
#
# Created 2026-08-08. Before this, 2053 had twenty renderers and no single
# command. Three separate defects that day traced to rendered output that did
# not match its source.
#
#   ./render_all.sh              render everything, then guard
#   ./render_all.sh --no-guard   skip check_style.py

cd "$(dirname "$0")"

FAILED=0
note() { if [ $? -eq 0 ]; then echo "  ✓ $1"; else echo "  ✗ $1"; FAILED=1; fi; }

echo "Re-rendering labs..."
for f in pages/labs/json/lab-*.json; do
    python3 render_lab.py "$f" > /dev/null; note "$f"
done

echo ""
echo "Re-rendering BookEx pages..."
for f in pages/bookex/json/bookex-ch*.json; do
    python3 render_bookex.py "$f" > /dev/null; note "$f"
done

echo ""
echo "Re-rendering study worksheets..."
for f in pages/support/json/study_worksheets/module_*_worksheet.json; do
    n=$(basename "$f" | cut -d_ -f2)
    python3 render_study_worksheet.py "$f" "pages/support/module-${n}-study-worksheet.html" > /dev/null
    note "module ${n} worksheet"
done

echo ""
echo "Re-rendering reading pages..."
python3 render_reading.py > /dev/null; note "all reading pages"

echo ""
echo "Re-rendering exam header pages..."
python3 render_exam_header.py > /dev/null; note "5 exam header pages"

echo ""
echo "Re-rendering support and scenario pages..."
# render_support_page.py is FIRST on purpose. It writes home.html whole, and
# render_modules.py then injects the Recordings card between that page's
# sentinels. Reverse them and the injection is overwritten, so home.html loses
# its recordings on every build.
for s in render_support_page.py \
         render_ai_policy.py render_all_my_eggses.py render_assignment_overview.py \
         render_bat_city.py render_bookex_overview.py render_codegrade_guide.py \
         render_course_schedule.py render_discord.py render_flake8_guide.py \
         render_grading_info.py render_how_to_get_help.py render_modules.py \
         render_project_plan.py render_scenario.py render_start_here.py; do
    python3 "$s" > /dev/null; note "$s"
done

# Safety net: a renderer added later but never wired in here is invisible
# otherwise. That is the exact failure this script exists to prevent.
echo ""
echo "Checking for unwired renderers..."
UNWIRED=0
for s in render_*.py; do
    case "$s" in
        render_variant.py|render_lab.py|render_bookex.py|render_study_worksheet.py) continue ;;
    esac
    if ! grep -q "$s" "$0"; then
        echo "  ✗ $s exists but is NOT in render_all.sh — add it"
        UNWIRED=1; FAILED=1
    fi
done
[ $UNWIRED -eq 0 ] && echo "  ✓ every renderer is wired in"

echo ""
echo "Building modality variants (must be last)..."
python3 render_variant.py; note "variant trees"

if [ "$1" != "--no-guard" ]; then
    echo ""
    echo "Running style guard..."
    python3 check_style.py || FAILED=1

    echo ""
    echo "Running lab consistency lint..."
    # Capture, do not pipe: a pipeline reports the LAST command's status, so
    # `lab_lint.py | tail` would report tail's success and swallow the failure.
    LINT_OUT=$(python3 lab_lint.py) || FAILED=1
    echo "$LINT_OUT" | tail -n 1

    echo ""
    echo "Checking dates..."
    python3 check_dates.py || FAILED=1

    echo ""
    echo "Checking syllabus links..."
    python3 check_syllabus_links.py || FAILED=1

    echo ""
    echo "Checking nav.js modality registry..."
    python3 check_nav_modality.py || FAILED=1

    echo ""
    echo "Checking the Zoom room..."
    python3 check_zoom_room.py || FAILED=1

    # Runs CodeGrade's own Scope Compliance rules against the solutions, here,
    # before anything reaches CodeGrade. Skips cleanly without a solutions tree.
    echo ""
    echo "Checking technique scope..."
    python3 check_scope.py || FAILED=1

    echo ""
    echo "Checking pending placeholders..."
    python3 check_pending.py || FAILED=1

    # The starter zip is GENERATED, so it can silently fall behind its
    # sources the moment a data file or a sheet's file list changes. This
    # runs before check_provided_files.py on purpose: a stale zip should be
    # reported as "rebuild it", not as unexplained drift between channels.
    echo ""
    echo "Checking starter zip is current..."
    python3 build_starter_zip.py --check | tail -n 2
    [ ${PIPESTATUS[0]} -eq 0 ] || FAILED=1

    # Execute each lab solution and diff it against the sheet's sample run.
    # The solutions live outside this repo, so this is the one guard that can
    # be unavailable. Skipping is announced loudly rather than passing quietly:
    # a check you think ran and did not is worse than no check.
    echo ""
    echo "Checking provided files..."
    if [ -d "${IS2053_SOLUTIONS:-$HOME/Library/CloudStorage/OneDrive-UniversityofTexasatSanAntonio/UTSA-Prof-Current/2026-3-Fall/IS2053/code/Modules}" ]; then
        python3 check_provided_files.py --solutions "${IS2053_SOLUTIONS:-$HOME/Library/CloudStorage/OneDrive-UniversityofTexasatSanAntonio/UTSA-Prof-Current/2026-3-Fall/IS2053/code/Modules}" | tail -n 3 
        [ ${PIPESTATUS[0]} -eq 0 ] || FAILED=1
    else
        python3 check_provided_files.py | tail -n 3
        [ ${PIPESTATUS[0]} -eq 0 ] || FAILED=1
    fi

    echo ""
    echo "Verifying sheets against the solutions..."
    SOLUTIONS="${IS2053_SOLUTIONS:-$HOME/Library/CloudStorage/OneDrive-UniversityofTexasatSanAntonio/UTSA-Prof-Current/2026-3-Fall/IS2053/code/Modules}"
    if [ -d "$SOLUTIONS" ]; then
        VERIFY_OUT=$(python3 verify_output.py --solutions "$SOLUTIONS") || FAILED=1
        echo "$VERIFY_OUT" | grep -E '^[A-Z][A-Z-]*=[0-9]' | sed 's/^/  /'
        # Only DIFFERS proves a disagreement; the rest are harness limits.
        echo "$VERIFY_OUT" | grep -E '^lab-\S+ +DIFFERS' | sed 's/^/  /' || true
    else
        echo "  SKIPPED: solutions tree not found at $SOLUTIONS"
        echo "  Set IS2053_SOLUTIONS to run it. Sheets were NOT checked against the code."
    fi
fi

echo ""
if [ $FAILED -ne 0 ]; then
    echo "FAILED. Fix the errors above before pushing."
    exit 1
fi
echo "Done. Push via GitHub Desktop."

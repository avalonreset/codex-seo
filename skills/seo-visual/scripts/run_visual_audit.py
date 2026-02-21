#!/usr/bin/env python3
"""Deterministic visual specialist runner for full SEO audits."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


VIEWPORTS = {
    "desktop": {"width": 1920, "height": 1080},
    "laptop": {"width": 1366, "height": 768},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 812},
}


def normalize_url(raw: str) -> str:
    value = raw.strip()
    if not value.startswith(("http://", "https://")):
        value = f"https://{value}"
    return value


def write_outputs(output_dir: Path, summary: dict[str, Any]) -> tuple[Path, Path]:
    report_path = output_dir / "VISUAL-AUDIT-REPORT.md"
    summary_path = output_dir / "SUMMARY.json"

    findings = [
        f"H1 visible above fold: {summary.get('h1_visible_above_fold')}",
        f"CTA visible above fold: {summary.get('cta_visible_above_fold')}",
        f"Viewport meta present: {summary.get('viewport_meta_present')}",
        f"Horizontal scroll on mobile: {summary.get('horizontal_scroll_mobile')}",
        f"Touch targets <48px: {summary.get('mobile_touch_targets_small')}/{summary.get('mobile_touch_targets_total')}",
        f"Minimum mobile font size: {summary.get('mobile_min_font_px')}",
        f"Desktop overlap signals: {summary.get('desktop_overlap_issues')}",
        f"Desktop overflow signals: {summary.get('desktop_overflow_issues')}",
        f"Layout shift events: {summary.get('layout_shift_count')} (value={summary.get('layout_shift_value')})",
        f"Responsive breakpoint failures: {summary.get('responsive_breakpoint_failures')}",
    ]

    report_path.write_text(
        "\n".join(
            [
                "# Visual Audit Report",
                "",
                f"- URL: `{summary.get('url')}`",
                f"- Generated: `{summary.get('generated_at')}`",
                f"- Status: `{summary.get('status')}`",
                "",
                "## Findings",
                "",
                *[f"- {line}" for line in findings],
                "",
                "## Screenshots",
                "",
                *[f"- `{path}`" for path in summary.get("screenshots", [])],
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return report_path, summary_path


def run_visual(url: str, output_dir: Path, timeout: int, mode: str) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "url": url,
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "skipped",
        "reason": "",
        "h1_visible_above_fold": None,
        "cta_visible_above_fold": None,
        "viewport_meta_present": None,
        "horizontal_scroll_mobile": None,
        "mobile_touch_targets_small": 0,
        "mobile_touch_targets_total": 0,
        "mobile_min_font_px": None,
        "hero_media_visible_above_fold": None,
        "desktop_overlap_issues": None,
        "desktop_overflow_issues": None,
        "layout_shift_count": None,
        "layout_shift_value": None,
        "responsive_breakpoint_failures": 0,
        "viewport_diagnostics": {},
        "screenshots": [],
        "issues": [],
    }

    if mode == "off":
        summary["reason"] = "Visual analysis disabled by mode=off."
        return summary

    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        if mode == "auto":
            summary["reason"] = f"Playwright unavailable: {exc}"
            return summary
        summary["status"] = "failed"
        summary["reason"] = f"Playwright unavailable: {exc}"
        return summary

    shots_dir = output_dir / "screenshots"
    shots_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        overlap_probe_js = """
        () => {
            const isVisible = (node) => {
                const style = window.getComputedStyle(node);
                if (!style) return false;
                if (style.display === 'none' || style.visibility === 'hidden' || parseFloat(style.opacity || '1') === 0) return false;
                return true;
            };
            const selectors = 'a, button, input, textarea, select, [role="button"], h1, h2, h3, p, img';
            const nodes = Array.from(document.querySelectorAll(selectors)).slice(0, 260);
            let overlaps = 0;
            for (const node of nodes) {
                if (!isVisible(node)) continue;
                const r = node.getBoundingClientRect();
                if (!r || r.width < 8 || r.height < 8) continue;
                if (r.bottom <= 0 || r.right <= 0 || r.top >= window.innerHeight || r.left >= window.innerWidth) continue;
                const cx = Math.min(window.innerWidth - 1, Math.max(0, r.left + (r.width / 2)));
                const cy = Math.min(window.innerHeight - 1, Math.max(0, r.top + (r.height / 2)));
                const topNode = document.elementFromPoint(cx, cy);
                if (!topNode) continue;
                if (topNode === node || node.contains(topNode) || topNode.contains(node)) continue;
                overlaps += 1;
                if (overlaps >= 40) break;
            }
            return {
                overlap_count: overlaps,
                horizontal_scroll: document.documentElement.scrollWidth > window.innerWidth,
            };
        }
        """
        cls_probe_js = """
        (() => {
            window.__codexLayoutShiftCount = 0;
            window.__codexLayoutShiftValue = 0;
            try {
                const obs = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (!entry.hadRecentInput) {
                            window.__codexLayoutShiftCount += 1;
                            window.__codexLayoutShiftValue += Number(entry.value || 0);
                        }
                    }
                });
                obs.observe({ type: 'layout-shift', buffered: true });
            } catch (err) {}
        })();
        """
        viewport_diagnostics: dict[str, dict[str, Any]] = {}

        # Capture screenshots in standard viewports.
        for label, viewport in VIEWPORTS.items():
            context = browser.new_context(viewport=viewport)
            page = context.new_page()
            page.goto(url, wait_until="networkidle", timeout=timeout * 1000)
            page.wait_for_timeout(500)
            shot_path = shots_dir / f"homepage-{label}.png"
            page.screenshot(path=str(shot_path), full_page=False)
            summary["screenshots"].append(str(shot_path))
            diag = page.evaluate(overlap_probe_js)
            viewport_diagnostics[label] = {
                "horizontal_scroll": bool((diag or {}).get("horizontal_scroll")),
                "overlap_count": int((diag or {}).get("overlap_count") or 0),
            }
            context.close()
        summary["viewport_diagnostics"] = viewport_diagnostics

        # Desktop signal checks.
        desktop = browser.new_context(viewport=VIEWPORTS["desktop"])
        dpage = desktop.new_page()
        dpage.add_init_script(cls_probe_js)
        dpage.goto(url, wait_until="networkidle", timeout=timeout * 1000)
        dpage.wait_for_timeout(1200)

        h1_visible = False
        h1 = dpage.query_selector("h1")
        if h1:
            box = h1.bounding_box()
            h1_visible = bool(box and box.get("y", 10_000) < VIEWPORTS["desktop"]["height"])
        summary["h1_visible_above_fold"] = h1_visible

        cta_visible = False
        selectors = [
            "a[href*='signup']",
            "a[href*='demo']",
            "a[href*='contact']",
            "button",
            ".cta",
            "[class*='cta']",
        ]
        for selector in selectors:
            try:
                node = dpage.query_selector(selector)
            except Exception:
                node = None
            if not node:
                continue
            box = node.bounding_box()
            if box and box.get("y", 10_000) < VIEWPORTS["desktop"]["height"]:
                cta_visible = True
                break
        summary["cta_visible_above_fold"] = cta_visible

        hero_signal = dpage.evaluate(
            """
            () => {
                const selectors = ['main img', 'header img', 'section img', '[class*="hero"] img', 'video'];
                for (const selector of selectors) {
                    const node = document.querySelector(selector);
                    if (!node) continue;
                    const rect = node.getBoundingClientRect();
                    if (!rect || rect.width <= 0 || rect.height <= 0) continue;
                    return {
                        found: true,
                        visible: rect.top < window.innerHeight && rect.bottom > 0,
                    };
                }
                return { found: false, visible: false };
            }
            """
        )
        if isinstance(hero_signal, dict) and hero_signal.get("found"):
            summary["hero_media_visible_above_fold"] = bool(hero_signal.get("visible"))

        desktop_diag = dpage.evaluate(overlap_probe_js)
        summary["desktop_overlap_issues"] = int((desktop_diag or {}).get("overlap_count") or 0)
        summary["desktop_overflow_issues"] = 1 if bool((desktop_diag or {}).get("horizontal_scroll")) else 0
        cls_stats = dpage.evaluate(
            "() => ({count: Number(window.__codexLayoutShiftCount || 0), value: Number(window.__codexLayoutShiftValue || 0)})"
        )
        summary["layout_shift_count"] = int((cls_stats or {}).get("count") or 0)
        summary["layout_shift_value"] = round(float((cls_stats or {}).get("value") or 0.0), 4)
        desktop.close()

        # Mobile checks.
        mobile = browser.new_context(viewport=VIEWPORTS["mobile"])
        mpage = mobile.new_page()
        mpage.goto(url, wait_until="networkidle", timeout=timeout * 1000)

        summary["viewport_meta_present"] = mpage.query_selector("meta[name='viewport']") is not None
        scroll_width = mpage.evaluate("document.documentElement.scrollWidth")
        inner_width = mpage.evaluate("window.innerWidth")
        summary["horizontal_scroll_mobile"] = bool(scroll_width > inner_width)

        min_font_px = mpage.evaluate(
            """
            () => {
              const nodes = Array.from(document.querySelectorAll('body *'));
              let min = 999;
              for (const node of nodes) {
                const s = window.getComputedStyle(node);
                if (!s) continue;
                const size = parseFloat(s.fontSize || '0');
                if (!Number.isFinite(size) || size <= 0) continue;
                min = Math.min(min, size);
              }
              return min === 999 ? null : min;
            }
            """
        )
        summary["mobile_min_font_px"] = min_font_px

        touch_stats = mpage.evaluate(
            """
            () => {
              const selectors = 'a, button, input, textarea, select, [role="button"]';
              const nodes = Array.from(document.querySelectorAll(selectors));
              let total = 0;
              let small = 0;
              for (const node of nodes) {
                const r = node.getBoundingClientRect();
                if (r.width <= 0 || r.height <= 0) continue;
                total += 1;
                if (r.width < 48 || r.height < 48) small += 1;
              }
              return { total, small };
            }
            """
        )
        summary["mobile_touch_targets_total"] = int((touch_stats or {}).get("total") or 0)
        summary["mobile_touch_targets_small"] = int((touch_stats or {}).get("small") or 0)

        mobile.close()
        browser.close()

    responsive_failures = 0
    for label in ("laptop", "tablet", "mobile"):
        diag = (summary.get("viewport_diagnostics") or {}).get(label) or {}
        if bool(diag.get("horizontal_scroll")) or int(diag.get("overlap_count") or 0) >= 6:
            responsive_failures += 1
    summary["responsive_breakpoint_failures"] = responsive_failures

    summary["status"] = "ok"

    if summary["horizontal_scroll_mobile"]:
        summary["issues"].append(
            {
                "priority": "High",
                "title": "Horizontal scrolling on mobile viewport",
                "detail": "Layout exceeds viewport width on mobile.",
                "recommendation": "Constrain overflowing elements and review fixed-width blocks.",
            }
        )
    if summary["mobile_min_font_px"] is not None and float(summary["mobile_min_font_px"]) < 16:
        summary["issues"].append(
            {
                "priority": "Medium",
                "title": "Mobile font size below readability baseline",
                "detail": f"Minimum detected mobile font size is {summary['mobile_min_font_px']}px.",
                "recommendation": "Increase base text size to at least 16px for body copy.",
            }
        )
    if summary["mobile_touch_targets_total"] > 0 and summary["mobile_touch_targets_small"] > 0:
        summary["issues"].append(
            {
                "priority": "Medium",
                "title": "Small touch targets detected",
                "detail": f"{summary['mobile_touch_targets_small']}/{summary['mobile_touch_targets_total']} targets are below 48px.",
                "recommendation": "Increase tap areas for links/buttons used in primary navigation and CTAs.",
            }
        )
    if summary["hero_media_visible_above_fold"] is False:
        summary["issues"].append(
            {
                "priority": "Medium",
                "title": "Hero media is not visible above the fold",
                "detail": "Detected hero media appears below the initial viewport.",
                "recommendation": "Reposition critical hero media/content so primary context loads in the first viewport.",
            }
        )
    overlap_count = int(summary.get("desktop_overlap_issues") or 0)
    if overlap_count >= 8:
        summary["issues"].append(
            {
                "priority": "High",
                "title": "Overlapping desktop elements detected",
                "detail": f"Detected {overlap_count} potential overlap intersections in the desktop viewport.",
                "recommendation": "Resolve stacking/positioning conflicts and verify key CTAs/text are unobstructed.",
            }
        )
    elif overlap_count >= 3:
        summary["issues"].append(
            {
                "priority": "Medium",
                "title": "Potential desktop overlap risk",
                "detail": f"Detected {overlap_count} overlap intersections in the desktop viewport sample.",
                "recommendation": "Review component spacing and z-index rules across major sections.",
            }
        )
    if int(summary.get("desktop_overflow_issues") or 0) > 0:
        summary["issues"].append(
            {
                "priority": "Medium",
                "title": "Desktop horizontal overflow detected",
                "detail": "Desktop viewport shows content width overflow.",
                "recommendation": "Constrain wide components and avoid fixed-width blocks beyond viewport bounds.",
            }
        )
    layout_shift_value = float(summary.get("layout_shift_value") or 0.0)
    layout_shift_count = int(summary.get("layout_shift_count") or 0)
    if layout_shift_value > 0.25:
        summary["issues"].append(
            {
                "priority": "High",
                "title": "High layout shift instability detected",
                "detail": f"Layout shift value sampled at {layout_shift_value} with {layout_shift_count} shift events.",
                "recommendation": "Reserve dimensions for late-loading elements and stabilize dynamic inserts/fonts.",
            }
        )
    elif layout_shift_value > 0.1 or layout_shift_count >= 8:
        summary["issues"].append(
            {
                "priority": "Medium",
                "title": "Moderate layout shift risk detected",
                "detail": f"Layout shift value sampled at {layout_shift_value} with {layout_shift_count} shift events.",
                "recommendation": "Audit late-rendering UI blocks and add dimension placeholders for media/embeds.",
            }
        )
    if int(summary.get("responsive_breakpoint_failures") or 0) > 0:
        summary["issues"].append(
            {
                "priority": "Medium",
                "title": "Responsive breakpoint layout stress",
                "detail": f"{summary['responsive_breakpoint_failures']} non-desktop breakpoints showed overflow or overlap stress.",
                "recommendation": "Test laptop/tablet/mobile breakpoints and adjust layout rules where overflow or overlap occurs.",
            }
        )

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic visual specialist audit.")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")
    parser.add_argument("--visual", choices=["on", "off", "auto"], default="auto", help="Visual analysis mode")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    args = parser.parse_args()

    target_url = normalize_url(args.url)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = run_visual(target_url, output_dir, timeout=args.timeout, mode=args.visual)
    report_path, summary_path = write_outputs(output_dir, summary)

    print(f"URL: {target_url}")
    print(f"Visual status: {summary.get('status')}")
    print(f"Issues: {len(summary.get('issues') or [])}")
    print(f"Report: {report_path}")
    print(f"Summary: {summary_path}")
    return 0 if summary.get("status") != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

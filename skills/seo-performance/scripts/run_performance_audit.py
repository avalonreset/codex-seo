#!/usr/bin/env python3
"""Deterministic performance specialist runner for full SEO audits."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urljoin, urlparse

import requests

PSI_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CodexSEO/1.0; +https://github.com/avalonreset/codex-seo)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.8",
}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def normalize_url(raw: str) -> str:
    value = raw.strip()
    if not value.startswith(("http://", "https://")):
        value = f"https://{value}"
    return value


def _dig(payload: dict[str, Any], path: list[str], default: Any = None) -> Any:
    node: Any = payload
    for part in path:
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node


def summarize_pagespeed_reason(reason: Any) -> str:
    text = " ".join(str(reason or "").split())
    if not text:
        return "PageSpeed request failed"
    lower = text.lower()
    if "quota" in lower and ("exceeded" in lower or "limit" in lower):
        return "PageSpeed API quota exceeded"
    if "api key" in lower or "key invalid" in lower:
        return "PageSpeed API key missing or invalid"
    match = re.search(r"http\s*(\d{3})", lower)
    if match:
        code = match.group(1)
        if code == "429":
            return "PageSpeed API rate limit reached"
        if code == "403":
            return "PageSpeed API access denied"
        if code == "400":
            return "PageSpeed API request invalid"
        return f"HTTP {code} from PageSpeed API"
    return text[:160]


def _is_expected_unavailable(reason: str, key_provided: bool) -> bool:
    if key_provided:
        return False
    lower = reason.lower()
    return ("api key" in lower) or ("quota" in lower) or ("http 429" in lower) or ("http 403" in lower)


def fetch_pagespeed(url: str, strategy: str, timeout: int, api_key: str) -> dict[str, Any]:
    params = {
        "url": url,
        "strategy": strategy,
        "category": "performance",
    }
    if api_key:
        params["key"] = api_key
    endpoint = f"{PSI_ENDPOINT}?{urlencode(params, doseq=True)}"
    try:
        response = requests.get(endpoint, timeout=timeout)
    except requests.RequestException as exc:
        raw_reason = str(exc)
        return {"status": "error", "reason": summarize_pagespeed_reason(raw_reason), "reason_raw": raw_reason, "payload": {}}

    if response.status_code >= 400:
        raw_reason = f"HTTP {response.status_code}"
        try:
            payload = response.json()
            err = payload.get("error", {}) if isinstance(payload, dict) else {}
            msg = err.get("message") if isinstance(err, dict) else None
            if msg:
                raw_reason = f"{raw_reason}: {msg}"
        except Exception:
            text = (response.text or "").strip()
            if text:
                raw_reason = f"{raw_reason}: {text[:160]}"
        return {
            "status": "error",
            "reason": summarize_pagespeed_reason(raw_reason),
            "reason_raw": raw_reason,
            "payload": {},
            "http_status": response.status_code,
        }

    try:
        payload = response.json()
    except ValueError:
        raw_reason = "Invalid JSON response"
        return {"status": "error", "reason": summarize_pagespeed_reason(raw_reason), "reason_raw": raw_reason, "payload": {}}

    score = _dig(payload, ["lighthouseResult", "categories", "performance", "score"])
    audits = _dig(payload, ["lighthouseResult", "audits"], {})
    field_source = ""
    field_block: dict[str, Any] = {}
    for source_key in ("loadingExperience", "originLoadingExperience"):
        source = _dig(payload, [source_key], {})
        metrics = source.get("metrics") if isinstance(source, dict) else {}
        if isinstance(metrics, dict) and metrics:
            field_source = source_key
            field_block = source
            break

    field_metrics = field_block.get("metrics") if isinstance(field_block.get("metrics"), dict) else {}
    field_lcp = _dig(field_metrics, ["LARGEST_CONTENTFUL_PAINT_MS", "percentile"])
    field_inp = _dig(field_metrics, ["INTERACTION_TO_NEXT_PAINT", "percentile"])
    field_cls_raw = _dig(field_metrics, ["CUMULATIVE_LAYOUT_SHIFT_SCORE", "percentile"])
    field_cls: float | None = None
    if isinstance(field_cls_raw, (int, float)):
        field_cls = float(field_cls_raw)
        if field_cls > 1:
            field_cls = field_cls / 100.0
    metrics = {
        "score": (float(score) * 100.0) if isinstance(score, (int, float)) else None,
        "lcp_ms": _dig(audits, ["largest-contentful-paint", "numericValue"]),
        "inp_ms": _dig(audits, ["interaction-to-next-paint", "numericValue"]),
        "cls": _dig(audits, ["cumulative-layout-shift", "numericValue"]),
        "field_source": field_source or None,
        "field_overall_category": str(field_block.get("overall_category") or "").lower() or None,
        "field_lcp_ms": field_lcp if isinstance(field_lcp, (int, float)) else None,
        "field_inp_ms": field_inp if isinstance(field_inp, (int, float)) else None,
        "field_cls": field_cls,
    }
    return {"status": "ok", "reason": "", "reason_raw": "", "payload": payload, "metrics": metrics}


def analyze_html_fallback(url: str, timeout: int) -> dict[str, Any]:
    script_re = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.IGNORECASE | re.DOTALL)
    img_re = re.compile(r"<img\b([^>]*)>", re.IGNORECASE)
    tag_re = re.compile(r"<[a-zA-Z][^>]*>")
    stylesheet_re = re.compile(r"<link\b[^>]*rel=[\"'][^\"']*stylesheet[^\"']*[\"'][^>]*>", re.IGNORECASE)
    preload_re = re.compile(r"<link\b[^>]*rel=[\"'][^\"']*preload[^\"']*[\"'][^>]*>", re.IGNORECASE)
    src_attr_re = re.compile(r"\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
    async_re = re.compile(r"\b(async|defer)\b", re.IGNORECASE)
    module_re = re.compile(r"type=[\"']module[\"']", re.IGNORECASE)
    width_re = re.compile(r"\bwidth\s*=", re.IGNORECASE)
    height_re = re.compile(r"\bheight\s*=", re.IGNORECASE)

    try:
        response = requests.get(url, timeout=timeout, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as exc:
        return {"status": "error", "reason": str(exc)}

    html_text = response.text or ""
    html_bytes = len(response.content or b"")
    dom_node_estimate = len(tag_re.findall(html_text))
    stylesheet_count = len(stylesheet_re.findall(html_text))
    preload_count = len(preload_re.findall(html_text))

    external_scripts = 0
    sync_external_scripts = 0
    third_party_scripts = 0
    inline_script_bytes = 0
    page_host = (urlparse(response.url).hostname or "").lower()

    for attrs, body in script_re.findall(html_text):
        src_match = src_attr_re.search(attrs)
        if src_match:
            external_scripts += 1
            src = src_match.group(1).strip()
            absolute = urljoin(response.url, src)
            src_host = (urlparse(absolute).hostname or "").lower()
            if src_host and page_host and src_host != page_host:
                third_party_scripts += 1
            if not async_re.search(attrs) and not module_re.search(attrs):
                sync_external_scripts += 1
        else:
            inline_script_bytes += len((body or "").encode("utf-8", errors="ignore"))

    total_images = 0
    images_missing_dimensions = 0
    for attrs in img_re.findall(html_text):
        total_images += 1
        if not width_re.search(attrs) or not height_re.search(attrs):
            images_missing_dimensions += 1

    issues: list[dict[str, str]] = []
    if html_bytes > 250_000:
        issues.append(
            {
                "priority": "High",
                "title": "Large HTML payload from source inspection",
                "detail": f"Document size is {html_bytes} bytes, which can increase parse and hydration cost.",
                "recommendation": "Reduce inline payloads and move heavy JSON/script data to cacheable external assets.",
            }
        )
    if sync_external_scripts >= 2:
        issues.append(
            {
                "priority": "High",
                "title": "Render-blocking script risk detected",
                "detail": f"{sync_external_scripts} external script tags appear without async/defer/module hints.",
                "recommendation": "Defer non-critical scripts and split route-specific bundles to reduce main-thread blocking.",
            }
        )
    if external_scripts >= 25:
        issues.append(
            {
                "priority": "High" if external_scripts >= 35 else "Medium",
                "title": "High JavaScript request volume detected",
                "detail": f"{external_scripts} external script references were found in source inspection.",
                "recommendation": "Audit bundle splitting and lazy-load below-the-fold features.",
            }
        )
    if inline_script_bytes > 100_000:
        issues.append(
            {
                "priority": "High",
                "title": "Large inline script payload detected",
                "detail": f"Inline script payload is approximately {inline_script_bytes} bytes.",
                "recommendation": "Move large serialized data blocks to external JSON/script resources with caching.",
            }
        )
    if dom_node_estimate > 1500:
        issues.append(
            {
                "priority": "Medium",
                "title": "Large DOM footprint risk",
                "detail": f"Approximate DOM node count is {dom_node_estimate}, which can increase interaction latency.",
                "recommendation": "Reduce deep DOM trees and simplify repeated component markup on key templates.",
            }
        )
    if images_missing_dimensions > 0:
        issues.append(
            {
                "priority": "High",
                "title": "Images missing explicit dimensions",
                "detail": (
                    f"{images_missing_dimensions}/{max(total_images, 1)} images are missing width/height attributes, "
                    "increasing CLS risk."
                ),
                "recommendation": "Add explicit width/height or reserve aspect-ratio space for all critical images.",
            }
        )
    if stylesheet_count >= 3:
        issues.append(
            {
                "priority": "Medium",
                "title": "Multiple stylesheet requests detected",
                "detail": f"{stylesheet_count} stylesheet links were detected in source inspection.",
                "recommendation": "Trim unused CSS and prioritize critical CSS for above-the-fold content.",
            }
        )
    if third_party_scripts >= 3:
        issues.append(
            {
                "priority": "Medium",
                "title": "Third-party script load pressure",
                "detail": f"{third_party_scripts} third-party script references were found.",
                "recommendation": "Delay non-essential third-party scripts until after primary content is interactive.",
            }
        )

    estimated_score = 82.0
    if html_bytes > 250_000:
        estimated_score -= 10.0
    elif html_bytes > 150_000:
        estimated_score -= 5.0
    estimated_score -= min(12.0, sync_external_scripts * 4.0)
    if external_scripts > 35:
        estimated_score -= 8.0
    elif external_scripts > 25:
        estimated_score -= 5.0
    if inline_script_bytes > 120_000:
        estimated_score -= 8.0
    elif inline_script_bytes > 70_000:
        estimated_score -= 4.0
    if dom_node_estimate > 2500:
        estimated_score -= 12.0
    elif dom_node_estimate > 1500:
        estimated_score -= 8.0
    if images_missing_dimensions > 0:
        estimated_score -= min(12.0, images_missing_dimensions * 1.5)
    if stylesheet_count >= 3:
        estimated_score -= 4.0
    if third_party_scripts >= 3:
        estimated_score -= 3.0

    return {
        "status": "ok",
        "method": "html_source_inspection",
        "final_url": response.url,
        "http_status": response.status_code,
        "estimated_score": round(clamp(estimated_score, 30.0, 95.0), 1),
        "signals": {
            "html_bytes": html_bytes,
            "dom_node_estimate": dom_node_estimate,
            "external_script_count": external_scripts,
            "sync_external_script_count": sync_external_scripts,
            "third_party_script_count": third_party_scripts,
            "inline_script_bytes": inline_script_bytes,
            "stylesheet_count": stylesheet_count,
            "preload_count": preload_count,
            "images_total": total_images,
            "images_missing_dimensions": images_missing_dimensions,
        },
        "issues": issues,
    }


def summarize(
    mobile: dict[str, Any],
    desktop: dict[str, Any],
    *,
    key_provided: bool,
    fallback: dict[str, Any] | None = None,
) -> tuple[float | None, list[dict[str, str]], str]:
    issues: list[dict[str, str]] = []
    unavailable_notes: list[str] = []

    scores = []
    for source in (mobile, desktop):
        value = (source.get("metrics") or {}).get("score")
        if isinstance(value, (int, float)):
            scores.append(float(value))
    perf_score = round(sum(scores) / len(scores), 1) if scores else None

    for label, source in (("Mobile", mobile), ("Desktop", desktop)):
        if source.get("status") != "ok":
            reason = str(source.get("reason") or "Unable to fetch PageSpeed data.")
            if _is_expected_unavailable(reason, key_provided):
                unavailable_notes.append(reason)
                continue
            issues.append(
                {
                    "priority": "Low",
                    "title": f"{label} CWV API data unavailable",
                    "detail": reason,
                    "recommendation": (
                        "Check PageSpeed API key quota/billing and rerun this specialist."
                        if key_provided
                        else "Optional: provide `PAGESPEED_API_KEY` to fetch live PageSpeed metrics."
                    ),
                }
            )
            continue
        metrics = source.get("metrics") or {}
        lcp = metrics.get("lcp_ms")
        inp = metrics.get("inp_ms")
        cls = metrics.get("cls")
        field_lcp = metrics.get("field_lcp_ms")
        field_inp = metrics.get("field_inp_ms")
        field_cls = metrics.get("field_cls")
        if isinstance(lcp, (int, float)) and float(lcp) > 2500:
            issues.append(
                {
                    "priority": "High",
                    "title": f"{label} LCP exceeds good threshold",
                    "detail": f"LCP is {round(float(lcp), 1)}ms (good <= 2500ms).",
                    "recommendation": "Prioritize hero element delivery, reduce render-blocking resources, and preload LCP assets.",
                }
            )
        if isinstance(inp, (int, float)) and float(inp) > 200:
            issues.append(
                {
                    "priority": "High",
                    "title": f"{label} INP exceeds good threshold",
                    "detail": f"INP is {round(float(inp), 1)}ms (good <= 200ms).",
                    "recommendation": "Break up long tasks, trim main-thread JavaScript, and defer non-critical handlers.",
                }
            )
        if isinstance(cls, (int, float)) and float(cls) > 0.1:
            issues.append(
                {
                    "priority": "High",
                    "title": f"{label} CLS exceeds good threshold",
                    "detail": f"CLS is {round(float(cls), 3)} (good <= 0.1).",
                    "recommendation": "Reserve layout space for media/embeds and stabilize font/layout shifts.",
                }
            )
        if isinstance(field_lcp, (int, float)) and float(field_lcp) > 2500:
            issues.append(
                {
                    "priority": "High",
                    "title": f"{label} field LCP p75 exceeds threshold",
                    "detail": f"Field LCP p75 is {round(float(field_lcp), 1)}ms (good <= 2500ms).",
                    "recommendation": "Improve TTFB and prioritize above-the-fold rendering for real-user sessions.",
                }
            )
        if isinstance(field_inp, (int, float)) and float(field_inp) > 200:
            issues.append(
                {
                    "priority": "High",
                    "title": f"{label} field INP p75 exceeds threshold",
                    "detail": f"Field INP p75 is {round(float(field_inp), 1)}ms (good <= 200ms).",
                    "recommendation": "Reduce long tasks and defer non-critical JavaScript to improve interaction responsiveness.",
                }
            )
        if isinstance(field_cls, (int, float)) and float(field_cls) > 0.1:
            issues.append(
                {
                    "priority": "High",
                    "title": f"{label} field CLS p75 exceeds threshold",
                    "detail": f"Field CLS p75 is {round(float(field_cls), 3)} (good <= 0.1).",
                    "recommendation": "Reserve image/embed dimensions and stabilize dynamic content placement.",
                }
            )

    if perf_score is not None:
        if perf_score < 70:
            issues.append(
                {
                    "priority": "High",
                    "title": "Average Lighthouse performance score is low",
                    "detail": f"Average score is {perf_score}/100.",
                    "recommendation": "Target critical-path CSS/JS reduction and improve cache hit rate for primary templates.",
                }
            )
        elif perf_score < 80:
            issues.append(
                {
                    "priority": "Medium",
                    "title": "Average Lighthouse performance score needs improvement",
                    "detail": f"Average score is {perf_score}/100.",
                    "recommendation": "Address highest-impact audit opportunities on mobile first.",
                }
            )

    fallback_used = False
    if perf_score is None and isinstance(fallback, dict):
        est = fallback.get("estimated_score")
        if isinstance(est, (int, float)):
            perf_score = round(float(est), 1)

    if isinstance(fallback, dict) and fallback.get("status") == "ok":
        fallback_issues = fallback.get("issues") if isinstance(fallback.get("issues"), list) else []
        if fallback_issues and (mobile.get("status") != "ok" or desktop.get("status") != "ok"):
            issues.extend([item for item in fallback_issues if isinstance(item, dict)])
            fallback_used = True

    if isinstance(fallback, dict) and fallback.get("status") == "error" and perf_score is None:
        fallback_reason = str(fallback.get("reason") or "Fallback source inspection failed.")
        issues.append(
            {
                "priority": "Low",
                "title": "Fallback source inspection unavailable",
                "detail": fallback_reason,
                "recommendation": "Retry performance audit after confirming the page is reachable from this environment.",
            }
        )

    note = ""
    if fallback_used:
        note = "PageSpeed API unavailable; source-code fallback profiling used."
    elif unavailable_notes:
        note = summarize_pagespeed_reason(unavailable_notes[0])
    return perf_score, issues, note


def write_outputs(
    output_dir: Path,
    url: str,
    score: float | None,
    mobile: dict[str, Any],
    desktop: dict[str, Any],
    issues: list[dict[str, str]],
    api_note: str = "",
    fallback: dict[str, Any] | None = None,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "PERFORMANCE-AUDIT-REPORT.md"
    summary_path = output_dir / "SUMMARY.json"

    def metric_row(source: dict[str, Any], label: str) -> str:
        metrics = source.get("metrics") or {}
        return (
            f"| {label} | {source.get('status', 'unknown')} | "
            f"{metrics.get('score', 'n/a')} | {metrics.get('lcp_ms', 'n/a')} | "
            f"{metrics.get('inp_ms', 'n/a')} | {metrics.get('cls', 'n/a')} | "
            f"{metrics.get('field_lcp_ms', 'n/a')} | {metrics.get('field_inp_ms', 'n/a')} | "
            f"{metrics.get('field_cls', 'n/a')} | {metrics.get('field_source', 'n/a')} |"
        )

    has_unavailable = (mobile.get("status") != "ok") or (desktop.get("status") != "ok")
    if api_note:
        note_line = f"- PageSpeed note: {api_note}"
    elif has_unavailable:
        note_line = "- PageSpeed note: live API data unavailable; fallback profiling used."
    else:
        note_line = "- PageSpeed note: live API data available."

    issue_lines = "\n".join(
        f"- **{item['priority']}**: {item['title']} - {item['detail']}\n  - Action: {item['recommendation']}"
        for item in issues
    )
    if not issue_lines:
        issue_lines = "- No significant performance risks detected from available data."

    fallback_block = ""
    if isinstance(fallback, dict) and fallback.get("status") == "ok":
        signals = fallback.get("signals") if isinstance(fallback.get("signals"), dict) else {}
        fallback_block = "\n".join(
            [
                "## Source Inspection Snapshot",
                "",
                "| Signal | Value |",
                "|---|---:|",
                f"| HTML bytes | {signals.get('html_bytes', 'n/a')} |",
                f"| DOM node estimate | {signals.get('dom_node_estimate', 'n/a')} |",
                f"| External scripts | {signals.get('external_script_count', 'n/a')} |",
                f"| Synchronous external scripts | {signals.get('sync_external_script_count', 'n/a')} |",
                f"| Third-party scripts | {signals.get('third_party_script_count', 'n/a')} |",
                f"| Inline script bytes | {signals.get('inline_script_bytes', 'n/a')} |",
                f"| Stylesheets | {signals.get('stylesheet_count', 'n/a')} |",
                f"| Images missing width/height | {signals.get('images_missing_dimensions', 'n/a')} |",
                "",
            ]
        )
    elif isinstance(fallback, dict) and fallback.get("status") == "error":
        fallback_block = "\n".join(
            [
                "## Source Inspection Snapshot",
                "",
                f"- Fallback status: error ({fallback.get('reason', 'unknown')})",
                "",
            ]
        )

    report_path.write_text(
        "\n".join(
            [
                "# Performance Audit Report",
                "",
                f"- URL: `{url}`",
                f"- Generated: `{datetime.now(UTC).isoformat()}`",
                f"- Performance score: **{score if score is not None else 'n/a'}/100**",
                note_line,
                "",
                "## Core Web Vitals Snapshot",
                "",
                "| Strategy | Status | Score | Lab LCP (ms) | Lab INP (ms) | Lab CLS | Field LCP p75 (ms) | Field INP p75 (ms) | Field CLS p75 | Field Source |",
                "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
                metric_row(mobile, "Mobile"),
                metric_row(desktop, "Desktop"),
                "",
                fallback_block,
                "## Findings",
                "",
                issue_lines,
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    priority_counts: dict[str, int] = {}
    for item in issues:
        priority = str(item.get("priority") or "Low")
        priority_counts[priority] = int(priority_counts.get(priority, 0)) + 1

    summary = {
        "url": url,
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "ok",
        "performance_score": score,
        "api_note": api_note,
        "mobile": mobile,
        "desktop": desktop,
        "fallback": fallback or {},
        "issues_count": len(issues),
        "priority_counts": priority_counts,
        "issues": issues,
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return report_path, summary_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic performance specialist audit.")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds")
    parser.add_argument("--pagespeed-key", default=os.getenv("PAGESPEED_API_KEY", ""), help="Optional PSI API key")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    args = parser.parse_args()

    target_url = normalize_url(args.url)
    output_dir = Path(args.output_dir).resolve()
    key_value = str(args.pagespeed_key or "").strip()
    key_provided = bool(key_value)

    mobile = fetch_pagespeed(target_url, "mobile", timeout=args.timeout, api_key=key_value)
    desktop = fetch_pagespeed(target_url, "desktop", timeout=args.timeout, api_key=key_value)
    fallback: dict[str, Any] | None = None
    if mobile.get("status") != "ok" and desktop.get("status") != "ok":
        fallback = analyze_html_fallback(target_url, timeout=args.timeout)

    score, issues, api_note = summarize(mobile, desktop, key_provided=key_provided, fallback=fallback)
    report_path, summary_path = write_outputs(
        output_dir,
        target_url,
        score,
        mobile,
        desktop,
        issues,
        api_note=api_note,
        fallback=fallback,
    )

    print(f"URL: {target_url}")
    print(f"Performance score: {score if score is not None else 'n/a'}/100")
    print(f"Issues: {len(issues)}")
    print(f"Report: {report_path}")
    print(f"Summary: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

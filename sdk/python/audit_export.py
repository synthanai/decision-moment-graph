"""
Audit Export Module

Generates compliance-ready reports from DMG files.

Usage:
    from audit_export import AuditExporter
    
    exporter = AuditExporter()
    html = exporter.to_html(dmg)
    exporter.to_file(dmg, "report.html")
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import json


@dataclass
class AuditSection:
    """A section of the audit report."""
    title: str
    content: str
    status: str = "info"  # info, success, warning, error


class AuditExporter:
    """
    Export DMG files to compliance-ready audit reports.
    
    Supports: HTML, Markdown, JSON
    """
    
    def __init__(self):
        self.template_html = self._get_html_template()
    
    def to_html(self, dmg: Dict[str, Any]) -> str:
        """Export DMG to HTML audit report."""
        sections = self._build_sections(dmg)
        
        sections_html = ""
        for section in sections:
            status_class = f"status-{section.status}"
            sections_html += f"""
            <div class="section {status_class}">
                <h2>{section.title}</h2>
                <div class="content">{section.content}</div>
            </div>
            """
        
        memo = dmg.get("memo", {})
        merit_score = dmg.get("merit_score", self._calculate_merit(dmg))
        
        return self.template_html.format(
            title=memo.get("title", "Decision Audit"),
            memo_id=memo.get("memo_id", "N/A"),
            generated_at=datetime.now().isoformat(),
            merit_score=merit_score,
            merit_level=self._merit_level(merit_score),
            sections=sections_html
        )
    
    def to_markdown(self, dmg: Dict[str, Any]) -> str:
        """Export DMG to Markdown audit report."""
        memo = dmg.get("memo", {})
        objects = dmg.get("objects", {})
        moment = dmg.get("moment", {})
        
        lines = [
            f"# Decision Audit: {memo.get('title', 'Untitled')}",
            "",
            f"**Memo ID**: {memo.get('memo_id', 'N/A')}",
            f"**Generated**: {datetime.now().isoformat()}",
            f"**MERIT Score**: {dmg.get('merit_score', 'N/A')}/5",
            "",
            "---",
            "",
            "## Decision Summary",
            "",
            f"**Decision**: {memo.get('decision', 'N/A')}",
            "",
            f"**Recommendation**: {memo.get('recommendation', 'N/A')}",
            "",
            f"**RAMP Level**: {memo.get('ramp', {}).get('level', 'N/A')}",
            "",
        ]
        
        # Options
        options = memo.get("options", [])
        if options:
            lines.append("## Options Considered")
            lines.append("")
            for i, opt in enumerate(options, 1):
                lines.append(f"### Option {i}: {opt.get('name', 'Unnamed')}")
                lines.append(f"{opt.get('description', '')}")
                if opt.get('pros'):
                    lines.append(f"- Pros: {', '.join(opt['pros'])}")
                lines.append("")
        
        # DOORS
        doors = objects.get("doors", {})
        if doors:
            lines.append("## Reversibility (DOORS)")
            lines.append("")
            lines.append(f"**Owner**: {doors.get('own', {}).get('name', 'Not assigned')}")
            lines.append(f"**Rollback Plan**: {doors.get('ready', 'Not defined')}")
            if doors.get("signals"):
                lines.append("**Reversal Signals**:")
                for sig in doors["signals"]:
                    lines.append(f"- {sig.get('metric', 'N/A')}: {sig.get('threshold', 'N/A')}")
            lines.append("")
        
        # Dissents
        dissents = objects.get("dissents", [])
        if dissents:
            lines.append("## Dissenting Views")
            lines.append("")
            for d in dissents:
                status = "✅ Resolved" if d.get("resolution") else "⚠️ Unresolved"
                lines.append(f"### {d.get('author', 'Unknown')} {status}")
                lines.append(f"**Claim**: {d.get('claim', '')}")
                if d.get("resolution"):
                    lines.append(f"**Resolution**: {d['resolution'].get('response', '')}")
                lines.append("")
        
        # Outcome
        outcome = objects.get("outcome", {})
        checks = outcome.get("checks", [])
        if checks:
            lines.append("## Outcome Tracking")
            lines.append("")
            for i, check in enumerate(checks, 1):
                lines.append(f"### Check {i} ({check.get('check_date', 'N/A')})")
                lines.append(f"**Verdict**: {check.get('verdict', 'N/A')}")
                lines.append(f"**Result**: {check.get('actual_result', 'N/A')}")
                lines.append("")
        
        # Audit Trail
        events = moment.get("events", [])
        if events:
            lines.append("## Audit Trail")
            lines.append("")
            lines.append("| Seq | Type | Actor | Timestamp |")
            lines.append("|-----|------|-------|-----------|")
            for e in events[:20]:  # Limit to 20
                lines.append(f"| {e.get('seq', '')} | {e.get('type', '')} | {e.get('actor', '')} | {e.get('ts', '')} |")
            if len(events) > 20:
                lines.append(f"| ... | ({len(events) - 20} more events) | ... | ... |")
            lines.append("")
        
        # MERIT Summary
        lines.append("## MERIT Compliance")
        lines.append("")
        merit = self._check_merit_detailed(dmg)
        for principle, status in merit.items():
            icon = "✅" if status["satisfied"] else "❌"
            lines.append(f"- {icon} **{principle}**: {status['reason']}")
        lines.append("")
        
        return "\n".join(lines)
    
    def to_json(self, dmg: Dict[str, Any]) -> str:
        """Export audit summary as JSON."""
        memo = dmg.get("memo", {})
        objects = dmg.get("objects", {})
        
        summary = {
            "audit_generated_at": datetime.now().isoformat(),
            "memo_id": memo.get("memo_id"),
            "title": memo.get("title"),
            "decision": memo.get("decision"),
            "ramp_level": memo.get("ramp", {}).get("level"),
            "merit_score": dmg.get("merit_score", self._calculate_merit(dmg)),
            "merit_compliance": self._check_merit_detailed(dmg),
            "options_count": len(memo.get("options", [])),
            "dissents_count": len(objects.get("dissents", [])),
            "dissents_unresolved": len([
                d for d in objects.get("dissents", [])
                if not d.get("resolution")
            ]),
            "outcome_checks": len(objects.get("outcome", {}).get("checks", [])),
            "audit_events": len(dmg.get("moment", {}).get("events", []))
        }
        
        return json.dumps(summary, indent=2)
    
    def to_file(self, dmg: Dict[str, Any], path: str) -> str:
        """Export to file, format determined by extension."""
        path = Path(path)
        
        if path.suffix == ".html":
            content = self.to_html(dmg)
        elif path.suffix == ".md":
            content = self.to_markdown(dmg)
        elif path.suffix == ".json":
            content = self.to_json(dmg)
        else:
            raise ValueError(f"Unsupported format: {path.suffix}")
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        
        return str(path)
    
    def _build_sections(self, dmg: Dict[str, Any]) -> List[AuditSection]:
        """Build audit sections from DMG."""
        sections = []
        memo = dmg.get("memo", {})
        objects = dmg.get("objects", {})
        
        # Summary
        sections.append(AuditSection(
            title="Decision Summary",
            content=f"""
            <p><strong>Decision:</strong> {memo.get('decision', 'N/A')}</p>
            <p><strong>Recommendation:</strong> {memo.get('recommendation', 'N/A')}</p>
            <p><strong>RAMP Level:</strong> {memo.get('ramp', {}).get('level', 'N/A')}</p>
            """,
            status="info"
        ))
        
        # Governance
        doors = objects.get("doors", {})
        if doors.get("own", {}).get("name"):
            sections.append(AuditSection(
                title="Governance & Reversibility",
                content=f"""
                <p><strong>Owner:</strong> {doors.get('own', {}).get('name')}</p>
                <p><strong>Rollback Plan:</strong> {doors.get('ready', 'Not defined')}</p>
                """,
                status="success"
            ))
        else:
            sections.append(AuditSection(
                title="Governance & Reversibility",
                content="<p>⚠️ DOORS owner not assigned</p>",
                status="warning"
            ))
        
        # Dissents
        dissents = objects.get("dissents", [])
        unresolved = [d for d in dissents if not d.get("resolution")]
        if unresolved:
            content = "<ul>"
            for d in unresolved:
                content += f"<li><strong>{d.get('author', 'Unknown')}:</strong> {d.get('claim', '')}</li>"
            content += "</ul>"
            sections.append(AuditSection(
                title=f"Unresolved Dissents ({len(unresolved)})",
                content=content,
                status="warning"
            ))
        
        return sections
    
    def _check_merit_detailed(self, dmg: Dict[str, Any]) -> Dict[str, Dict]:
        """Check each MERIT principle with details."""
        objects = dmg.get("objects", {})
        memo = dmg.get("memo", {})
        moment = dmg.get("moment", {})
        
        return {
            "Measured": {
                "satisfied": bool(objects.get("outcome", {}).get("checks")),
                "reason": "Outcome checks recorded" if objects.get("outcome", {}).get("checks") else "No outcome tracking"
            },
            "Evidenced": {
                "satisfied": bool(objects.get("traces")),
                "reason": f"{len(objects.get('traces', []))} traces linked" if objects.get("traces") else "No evidence traces"
            },
            "Reversible": {
                "satisfied": bool(objects.get("doors", {}).get("ready")),
                "reason": "Rollback plan defined" if objects.get("doors", {}).get("ready") else "No rollback plan"
            },
            "Inspectable": {
                "satisfied": bool(moment.get("events")),
                "reason": f"{len(moment.get('events', []))} audit events" if moment.get("events") else "No audit trail"
            },
            "Traceable": {
                "satisfied": len(moment.get("events", [])) > 1,
                "reason": "Hash chain established" if len(moment.get("events", [])) > 1 else "Incomplete chain"
            }
        }
    
    def _calculate_merit(self, dmg: Dict[str, Any]) -> int:
        """Calculate MERIT score."""
        detailed = self._check_merit_detailed(dmg)
        return sum(1 for v in detailed.values() if v["satisfied"])
    
    def _merit_level(self, score: int) -> str:
        """Get MERIT level from score."""
        if score >= 5:
            return "MERIT-Valid"
        elif score >= 3:
            return "MERIT-Partial"
        else:
            return "MERIT-None"
    
    def _get_html_template(self) -> str:
        """Get HTML report template."""
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title} - Audit Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               max-width: 900px; margin: 40px auto; padding: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0 0 10px 0; }}
        .meta {{ opacity: 0.9; font-size: 14px; }}
        .merit-badge {{ display: inline-block; padding: 5px 15px; border-radius: 20px; 
                       background: rgba(255,255,255,0.2); margin-top: 10px; }}
        .section {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 15px;
                   box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .section h2 {{ margin-top: 0; color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        .status-success {{ border-left: 4px solid #10b981; }}
        .status-warning {{ border-left: 4px solid #f59e0b; }}
        .status-error {{ border-left: 4px solid #ef4444; }}
        .status-info {{ border-left: 4px solid #3b82f6; }}
        .content {{ color: #555; line-height: 1.6; }}
        .footer {{ text-align: center; color: #888; font-size: 12px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <div class="meta">
            Memo ID: {memo_id}<br>
            Generated: {generated_at}
        </div>
        <div class="merit-badge">MERIT Score: {merit_score}/5 ({merit_level})</div>
    </div>
    
    {sections}
    
    <div class="footer">
        Generated by DMG Audit Export • RESOLVE Loop Infrastructure
    </div>
</body>
</html>"""


if __name__ == "__main__":
    # Demo
    sample_dmg = {
        "dmg_version": "0.1",
        "memo": {
            "memo_id": "demo-001",
            "title": "API Migration Decision",
            "decision": "Proceed with GraphQL migration",
            "recommendation": "Migrate top 5 endpoints as pilot phase",
            "ramp": {"level": 3},
            "options": [
                {"name": "Full Migration", "description": "Migrate all endpoints"},
                {"name": "Pilot First", "description": "Start with 5 endpoints"},
                {"name": "Wait", "description": "Gather more data"}
            ]
        },
        "objects": {
            "doors": {
                "own": {"name": "API Team Lead"},
                "ready": "Rollback to REST within 1 hour"
            },
            "dissents": [
                {"author": "SRE Lead", "claim": "Performance risk", "resolution": None}
            ],
            "outcome": {
                "checks": [{"verdict": "keep", "actual_result": "Pilot succeeded"}]
            }
        },
        "moment": {
            "events": [
                {"seq": 1, "type": "MEMO_CREATED", "actor": "system", "ts": "2026-01-26T00:00:00Z"}
            ]
        }
    }
    
    exporter = AuditExporter()
    
    # Generate reports
    print("Generating audit reports...")
    print(exporter.to_markdown(sample_dmg))

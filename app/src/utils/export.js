/**
 * Export Utilities
 */

export function exportMemo(memo) {
    // Create full DMG object
    const dmg = {
        dmg_version: '0.1',
        memo: {
            memo_id: memo.memo_id,
            title: memo.title,
            decision: memo.decision,
            options: memo.options,
            recommendation: memo.recommendation,
            ramp: memo.ramp,
            owners: memo.owners,
            review_date: memo.review_date,
            version: memo.version,
            created_at: memo.created_at,
            updated_at: memo.updated_at
        },
        moment: {
            moment_id: 'moment-' + memo.memo_id,
            memo_id: memo.memo_id,
            events: []
        },
        objects: {
            dissents: [],
            traces: [],
            commit: { state: 'Draft' },
            outcome: {}
        }
    };

    // Download as JSON
    const blob = new Blob([JSON.stringify(dmg, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `${sanitizeFilename(memo.title || 'decision')}.dmg.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

export function exportAsMarkdown(memo) {
    const rampLabels = ['', 'Minutes', 'Hours', 'Weeks', 'Months', 'Years'];
    const rampLevel = memo.ramp?.level || 3;

    let md = `# MEMO: ${memo.title}\n\n`;
    md += `**RAMP Level**: L${rampLevel} (${rampLabels[rampLevel]} to undo)\n\n`;
    md += `## Decision\n\n${memo.decision || 'Not specified'}\n\n`;

    md += `## Options Considered\n\n`;
    (memo.options || []).forEach((opt, i) => {
        md += `### Option ${String.fromCharCode(65 + i)}: ${opt.name}\n`;
        md += `${opt.description || ''}\n\n`;
    });

    md += `## Recommendation\n\n${memo.recommendation || 'Not specified'}\n\n`;

    if (memo.owners && memo.owners.length > 0) {
        md += `## Owners\n\n`;
        memo.owners.forEach(o => {
            md += `- **${o.name}** — ${o.role}\n`;
        });
        md += '\n';
    }

    md += `---\n\n`;
    md += `*Created: ${new Date(memo.created_at).toLocaleDateString()} | `;
    md += `Updated: ${new Date(memo.updated_at).toLocaleDateString()} | `;
    md += `Version: ${memo.version || 1}*\n`;

    // Download as MD
    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `${sanitizeFilename(memo.title || 'decision')}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function sanitizeFilename(name) {
    return name
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '')
        .substring(0, 50);
}

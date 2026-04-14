/**
 * DMG-Kit MCP Apps: Decision Flow Visualizer
 * 
 * Interactive UI for visualizing the 7-step Heptagon lifecycle:
 * FRAME → SPAR → GATE → COMMIT → ENACT → YIELD → GAUGE
 * 
 * @see https://modelcontextprotocol.github.io/ext-apps/api/
 */

/**
 * Generate the Decision Flow Visualizer HTML
 */
export function generateDecisionFlowUI(options = {}) {
    const {
        decisionId = '',
        currentPhase = 'frame',
        phases = ['FRAME', 'SPAR', 'GATE', 'COMMIT', 'ENACT', 'YIELD', 'GAUGE']
    } = options;

    const phaseColors = {
        FRAME: '#3b82f6',
        SPAR: '#8b5cf6',
        GATE: '#f59e0b',
        COMMIT: '#10b981',
        ENACT: '#06b6d4',
        YIELD: '#ec4899',
        GAUGE: '#6366f1'
    };

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DMG Decision Flow</title>
    <style>
        :root {
            --bg-primary: #1e1e1e;
            --bg-secondary: #252526;
            --text-primary: #ffffff;
            --text-muted: #858585;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            padding: 16px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        
        .header-icon { font-size: 1.5rem; }
        
        .header-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #8b5cf6;
        }
        
        .decision-id {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 4px;
            font-family: monospace;
        }
        
        .heptagon-container {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin: 20px 0;
        }
        
        .phase-row {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 12px;
            background: var(--bg-secondary);
            border-radius: 8px;
            border-left: 4px solid;
            transition: all 0.3s;
            cursor: pointer;
        }
        
        .phase-row:hover {
            transform: translateX(4px);
        }
        
        .phase-row.active {
            box-shadow: none;
        }
        
        .phase-row.complete {
            opacity: 0.6;
        }
        
        .phase-number {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 700;
            color: white;
        }
        
        .phase-name {
            font-weight: 600;
            font-size: 0.85rem;
            flex: 1;
        }
        
        .phase-status {
            font-size: 0.7rem;
            padding: 2px 8px;
            border-radius: 10px;
            background: transparent;
        }
        
        .phase-status.pending { color: var(--text-muted); }
        .phase-status.active { color: #10b981; background: rgba(16,185,129,0.2); }
        .phase-status.complete { color: #6366f1; }
        
        .merit-badge {
            margin-top: 16px;
            padding: 12px;
            background: transparent;
            border: 1px solid  transparent;
            border-radius: 8px;
            text-align: center;
        }
        
        .merit-title {
            font-size: 0.8rem;
            font-weight: 600;
            color: #8b5cf6;
            margin-bottom: 4px;
        }
        
        .merit-values {
            display: flex;
            justify-content: center;
            gap: 8px;
            font-size: 0.7rem;
            color: var(--text-muted);
        }
        
        .footer {
            margin-top: 16px;
            text-align: center;
            font-size: 0.7rem;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="header">
        <span class="header-icon">⬡</span>
        <div class="header-title">Decision Moment Graph</div>
        <div class="decision-id" id="decision-id">${decisionId || 'Awaiting decision...'}</div>
    </div>
    
    <div class="heptagon-container" id="phases">
        ${phases.map((phase, i) => `
        <div class="phase-row ${currentPhase.toUpperCase() === phase ? 'active' : ''}" 
             data-phase="${phase.toLowerCase()}"
             style="border-color: ${phaseColors[phase]}">
            <div class="phase-number" style="background: ${phaseColors[phase]}">${i + 1}</div>
            <span class="phase-name">${phase}</span>
            <span class="phase-status ${i < phases.indexOf(currentPhase.toUpperCase()) ? 'complete' : (currentPhase.toUpperCase() === phase ? 'active' : 'pending')}">
                ${i < phases.indexOf(currentPhase.toUpperCase()) ? '✓ Done' : (currentPhase.toUpperCase() === phase ? '● Active' : '○ Pending')}
            </span>
        </div>
        `).join('')}
    </div>
    
    <div class="merit-badge">
        <div class="merit-title">MERIT Compliance</div>
        <div class="merit-values">
            <span>M·Measured</span>
            <span>E·Evidenced</span>
            <span>R·Reversible</span>
            <span>I·Inclusive</span>
            <span>T·Transparent</span>
        </div>
    </div>
    
    <div class="footer">DMG v0.2 — 7-Step Heptagon Lifecycle</div>
    
    <script>
        // MCP Apps communication
        function sendMessage(text) {
            window.parent.postMessage({
                jsonrpc: '2.0',
                id: Date.now(),
                method: 'ui/message',
                params: { content: [{ type: 'text', text }] }
            }, '*');
        }
        
        // Handle tool input notifications
        window.addEventListener('message', (event) => {
            const { data } = event;
            if (data.method === 'ui/notifications/tool-input') {
                const args = data.params?.arguments || {};
                if (args.decisionId) {
                    document.getElementById('decision-id').textContent = args.decisionId;
                }
                if (args.currentPhase) {
                    updateActivePhase(args.currentPhase);
                }
            }
        });
        
        function updateActivePhase(phase) {
            document.querySelectorAll('.phase-row').forEach(row => {
                row.classList.remove('active');
                if (row.dataset.phase === phase.toLowerCase()) {
                    row.classList.add('active');
                }
            });
        }
        
        // Click to advance phase
        document.querySelectorAll('.phase-row').forEach(row => {
            row.addEventListener('click', () => {
                sendMessage('Advance to ' + row.dataset.phase + ' phase');
            });
        });
    </script>
</body>
</html>`;
}

/**
 * Register DMG MCP Apps resources
 */
export function registerDmgAppsResources(server) {
    server.resource(
        "decision-flow",
        "ui://dmg-kit/decision-flow",
        {
            description: "7-step Heptagon decision lifecycle visualizer",
            mimeType: "text/html;profile=mcp-app"
        },
        async () => ({
            contents: [{
                mimeType: "text/html;profile=mcp-app",
                text: generateDecisionFlowUI()
            }]
        })
    );
}

export default { generateDecisionFlowUI, registerDmgAppsResources };

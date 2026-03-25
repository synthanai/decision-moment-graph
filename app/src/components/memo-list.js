/**
 * MEMO List & Editor Components
 */

export function renderMemoCard(memo) {
    const rampLevel = memo.ramp?.level || 3;
    const date = new Date(memo.updated_at).toLocaleDateString();

    return `
    <div class="memo-card" data-id="${memo.memo_id}">
      <div class="memo-card-title">${memo.title || 'Untitled Decision'}</div>
      <div class="memo-card-meta">
        <span class="ramp-badge l${rampLevel}">L${rampLevel}</span>
        <span>${date}</span>
      </div>
    </div>
  `;
}

export function renderMemoList(container, memos) {
    if (memos.length === 0) {
        container.innerHTML = `
      <div class="empty-state">
        <p>No decisions yet.</p>
        <p class="empty-hint">Click "+ New MEMO" to start.</p>
      </div>
    `;
        return;
    }

    container.innerHTML = memos
        .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
        .map(memo => renderMemoCard(memo))
        .join('');
}

export function renderMemoEditor(container, memo) {
    const rampLevel = memo.ramp?.level || 3;
    const rampLabels = ['', 'Minutes', 'Hours', 'Weeks', 'Months', 'Years'];

    container.innerHTML = `
    <div class="memo-editor">
      <div class="memo-header">
        <h1 class="memo-title-display">${memo.title || 'Untitled Decision'}</h1>
        <div class="memo-meta">
          <span class="ramp-badge l${rampLevel}">RAMP L${rampLevel} — ${rampLabels[rampLevel]} to undo</span>
          <span class="memo-date">Updated: ${new Date(memo.updated_at).toLocaleString()}</span>
        </div>
      </div>
      
      <div class="memo-section">
        <h2>📋 Decision</h2>
        <p class="memo-text">${memo.decision || 'No decision statement yet.'}</p>
      </div>
      
      <div class="memo-section">
        <h2>🔀 Options Considered</h2>
        <div class="options-grid">
          ${(memo.options || []).map((opt, i) => `
            <div class="option-card">
              <div class="option-name">${opt.name || `Option ${String.fromCharCode(65 + i)}`}</div>
              <div class="option-desc">${opt.description || ''}</div>
            </div>
          `).join('')}
        </div>
      </div>
      
      <div class="memo-section">
        <h2>✅ Recommendation</h2>
        <p class="memo-text">${memo.recommendation || 'No recommendation yet.'}</p>
      </div>
      
      ${memo.owners && memo.owners.length > 0 ? `
        <div class="memo-section">
          <h2>👤 Owners</h2>
          <ul class="owners-list">
            ${memo.owners.map(o => `<li><strong>${o.name}</strong> — ${o.role}</li>`).join('')}
          </ul>
        </div>
      ` : ''}
      
      <div class="memo-footer">
        <span>Version ${memo.version || 1}</span>
        <span>Created: ${new Date(memo.created_at).toLocaleDateString()}</span>
      </div>
    </div>
  `;

    // Add editor-specific styles
    addEditorStyles();
}

function addEditorStyles() {
    if (document.getElementById('memo-editor-styles')) return;

    const style = document.createElement('style');
    style.id = 'memo-editor-styles';
    style.textContent = `
    .memo-editor {
      animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    .memo-header {
      margin-bottom: var(--space-xl);
      padding-bottom: var(--space-lg);
      border-bottom: 1px solid var(--border);
    }
    
    .memo-title-display {
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: var(--space-md);
      background: linear-gradient(135deg, var(--text-primary), var(--text-secondary));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    .memo-meta {
      display: flex;
      gap: var(--space-md);
      color: var(--text-muted);
      font-size: 0.875rem;
    }
    
    .memo-section {
      margin-bottom: var(--space-xl);
    }
    
    .memo-section h2 {
      font-size: 1rem;
      font-weight: 600;
      color: var(--text-secondary);
      margin-bottom: var(--space-md);
    }
    
    .memo-text {
      color: var(--text-primary);
      line-height: 1.8;
      background: var(--bg-secondary);
      padding: var(--space-md);
      border-radius: var(--radius-md);
      border: 1px solid var(--border);
    }
    
    .options-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: var(--space-md);
    }
    
    .option-card {
      background: var(--bg-secondary);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: var(--space-md);
      transition: all 0.2s ease;
    }
    
    .option-card:hover {
      border-color: var(--accent-primary);
      transform: translateY(-2px);
    }
    
    .option-name {
      font-weight: 600;
      margin-bottom: var(--space-xs);
      color: var(--accent-secondary);
    }
    
    .option-desc {
      font-size: 0.875rem;
      color: var(--text-secondary);
    }
    
    .owners-list {
      list-style: none;
      padding: 0;
    }
    
    .owners-list li {
      padding: var(--space-sm) 0;
      border-bottom: 1px solid var(--border);
    }
    
    .memo-footer {
      display: flex;
      justify-content: space-between;
      color: var(--text-muted);
      font-size: 0.75rem;
      padding-top: var(--space-lg);
      border-top: 1px solid var(--border);
    }
  `;
    document.head.appendChild(style);
}

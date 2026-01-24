/**
 * Outcome Tracking Service
 * 
 * Manages outcome checks, audits, and learning loops.
 */

import { DMGStore } from '../stores/dmg-store.js';

/**
 * Get all upcoming outcome checks
 * @param {DMGStore} store 
 * @returns {Promise<Array>} Sorted list of upcoming checks
 */
export async function getUpcomingOutcomes(store) {
    const memos = await store.getAllMemos();
    const today = new Date().toISOString().split('T')[0];

    const upcoming = memos
        .filter(memo => {
            const nextCheck = memo.outcome?.next_check_date;
            return nextCheck && memo.commit?.state !== 'Reversed';
        })
        .map(memo => ({
            memo_id: memo.memo_id,
            title: memo.title,
            next_check_date: memo.outcome.next_check_date,
            ramp_level: memo.ramp?.level || 3,
            status: getOutcomeStatus(memo.outcome.next_check_date, today)
        }))
        .sort((a, b) => new Date(a.next_check_date) - new Date(b.next_check_date));

    return upcoming;
}

/**
 * Get outcome status
 */
function getOutcomeStatus(checkDate, today) {
    if (checkDate < today) return 'overdue';

    const daysUntil = Math.ceil(
        (new Date(checkDate) - new Date(today)) / (1000 * 60 * 60 * 24)
    );

    if (daysUntil <= 7) return 'due-soon';
    return 'upcoming';
}

/**
 * Prepare outcome check form data
 * @param {Object} memo 
 * @returns {Object} Form data for outcome check
 */
export function prepareOutcomeCheck(memo) {
    // Get assumptions from context
    const assumptions = (memo.context?.assumptions || []).map((a, i) => ({
        id: `assumption-${i}`,
        text: a,
        accurate: null,
        learning: ''
    }));

    // Get dissents
    const dissents = (memo.dissents || []).map(d => ({
        id: d.dissent_id,
        author: d.author,
        claim: d.claim,
        vindicated: null,
        notes: ''
    }));

    // Get expected outcomes for comparison
    const expectations = (memo.expected_outcomes || []).map((e, i) => ({
        id: `expectation-${i}`,
        metric: e.metric,
        expected: e.expected,
        confidence: e.confidence,
        actual: '',
        delta: ''
    }));

    return {
        memo_id: memo.memo_id,
        title: memo.title,
        check_date: new Date().toISOString().split('T')[0],
        assumptions,
        dissents,
        expectations,
        actual_result: '',
        verdict: null,
        next_action: '',
        next_check_date: null
    };
}

/**
 * Save outcome check
 * @param {DMGStore} store 
 * @param {string} memoId 
 * @param {Object} checkData 
 */
export async function saveOutcomeCheck(store, memoId, checkData) {
    const memo = await store.getMemo(memoId);
    if (!memo) throw new Error('Memo not found');

    // Initialize outcome if needed
    if (!memo.outcome) {
        memo.outcome = {
            outcome_id: `outcome-${memoId}`,
            checks: []
        };
    }

    // Add the check
    const check = {
        check_date: checkData.check_date,
        actual_result: checkData.actual_result,
        assumptions_audit: checkData.assumptions.map(a => ({
            assumption: a.text,
            accurate: a.accurate,
            learning: a.learning
        })),
        dissent_audit: checkData.dissents.map(d => ({
            dissent_id: d.id,
            vindicated: d.vindicated,
            notes: d.notes
        })),
        expected_outcomes_audit: checkData.expectations.map(e => ({
            metric: e.metric,
            predicted: e.expected,
            confidence: e.confidence,
            actual: e.actual,
            delta: e.delta
        })),
        verdict: checkData.verdict,
        next_action: checkData.next_action
    };

    memo.outcome.checks.push(check);

    // Update next check date
    memo.outcome.next_check_date = checkData.next_check_date || null;

    // Update commit state if reversed
    if (checkData.verdict === 'reverse') {
        memo.commit = {
            ...memo.commit,
            state: 'Reversed',
            changed_at: new Date().toISOString(),
            changed_by: 'outcome-check'
        };
    }

    // Save
    await store.updateMemo(memo);

    // Add MOMENT event
    await store.addMomentEvent(memoId, 'OUTCOME_RECORDED', {
        verdict: checkData.verdict,
        actual_result: checkData.actual_result?.substring(0, 100)
    });

    return memo;
}

/**
 * Render the upcoming outcomes panel
 */
export function renderUpcomingPanel(container, outcomes, onItemClick) {
    if (!outcomes || outcomes.length === 0) {
        container.style.display = 'none';
        return;
    }

    container.style.display = 'block';

    const listContainer = container.querySelector('#upcoming-list') || container;
    listContainer.innerHTML = outcomes.slice(0, 5).map(outcome => `
    <div class="upcoming-item" data-id="${outcome.memo_id}">
      <span class="upcoming-item-title">${outcome.title}</span>
      <span class="upcoming-item-date ${outcome.status}">${formatRelativeDate(outcome.next_check_date)}</span>
    </div>
  `).join('');

    // Attach click handlers
    listContainer.querySelectorAll('.upcoming-item').forEach(item => {
        item.addEventListener('click', () => {
            onItemClick(item.dataset.id);
        });
    });
}

/**
 * Render the outcome check form
 */
export function renderOutcomeForm(container, checkData, onVerdictSelect) {
    // Render assumptions audit
    const assumptionsContainer = container.querySelector('#assumptions-audit');
    if (assumptionsContainer) {
        if (checkData.assumptions.length === 0) {
            assumptionsContainer.innerHTML = '<p class="text-muted">No assumptions recorded</p>';
        } else {
            assumptionsContainer.innerHTML = checkData.assumptions.map(a => `
        <div class="audit-item" data-id="${a.id}">
          <input type="checkbox" class="assumption-check" ${a.accurate ? 'checked' : ''}>
          <div class="audit-item-text">
            <div class="audit-item-label">${a.text}</div>
            <div class="audit-item-status">${a.accurate === null ? 'Check if accurate' : a.accurate ? '✓ Accurate' : '✗ Inaccurate'}</div>
          </div>
        </div>
      `).join('');
        }
    }

    // Render dissent audit
    const dissentContainer = container.querySelector('#dissent-audit');
    if (dissentContainer) {
        if (checkData.dissents.length === 0) {
            dissentContainer.innerHTML = '<p class="text-muted">No dissents recorded</p>';
        } else {
            dissentContainer.innerHTML = checkData.dissents.map(d => `
        <div class="audit-item" data-id="${d.id}">
          <input type="checkbox" class="dissent-check" ${d.vindicated ? 'checked' : ''}>
          <div class="audit-item-text">
            <div class="audit-item-label">${d.author}</div>
            <div class="audit-item-status">${d.claim}</div>
          </div>
        </div>
      `).join('');
        }
    }

    // Setup verdict buttons
    const verdictBtns = container.querySelectorAll('.verdict-btn');
    verdictBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            verdictBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            onVerdictSelect(btn.dataset.verdict);
        });

        // Pre-select if verdict exists
        if (checkData.verdict === btn.dataset.verdict) {
            btn.classList.add('active');
        }
    });
}

/**
 * Format relative date
 */
function formatRelativeDate(dateString) {
    const date = new Date(dateString);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    date.setHours(0, 0, 0, 0);

    const diff = Math.ceil((date - today) / (1000 * 60 * 60 * 24));

    if (diff < 0) return `${Math.abs(diff)}d overdue`;
    if (diff === 0) return 'Today';
    if (diff === 1) return 'Tomorrow';
    if (diff <= 7) return `In ${diff}d`;
    return date.toLocaleDateString();
}

/**
 * DMG App — Main Entry Point
 * Decision Moment Graph: Store decision moments, not raw chats, objects or data.
 */

import { DMGStore } from './stores/dmg-store.js';
import { renderMemoList, renderMemoEditor } from './components/memo-list.js';
import { showModal, hideModal } from './components/modal.js';
import { exportMemo } from './utils/export.js';
import { runSPAR, sparToDMG } from './services/spar-service.js';
import {
    getUpcomingOutcomes,
    prepareOutcomeCheck,
    saveOutcomeCheck,
    renderUpcomingPanel,
    renderOutcomeForm
} from './services/outcome-service.js';

// Initialize the store
const store = new DMGStore();

// DOM Elements
const newMemoBtn = document.getElementById('new-memo-btn');
const sparBtn = document.getElementById('spar-btn');
const editorNewBtn = document.getElementById('editor-new-btn');
const exportBtn = document.getElementById('export-btn');
const memoModal = document.getElementById('memo-modal');
const sparModal = document.getElementById('spar-modal');
const outcomeModal = document.getElementById('outcome-modal');
const closeModalBtn = document.getElementById('close-modal');
const cancelMemoBtn = document.getElementById('cancel-memo');
const saveMemoBtn = document.getElementById('save-memo');
const addOptionBtn = document.getElementById('add-option');
const memoList = document.getElementById('memo-list');
const memoCount = document.getElementById('memo-count');
const rightPanel = document.getElementById('right-panel');
const editorContent = document.getElementById('editor-content');
const rampSelector = document.getElementById('ramp-selector');
const upcomingPanel = document.getElementById('upcoming-outcomes');
const outcomeDate = document.getElementById('outcome-date');

// State
let currentMemoId = null;
let currentSparResult = null;
let currentOutcomeCheck = null;

// Initialize app
async function init() {
    await store.init();
    await refreshMemoList();
    await refreshUpcomingOutcomes();
    setupEventListeners();
    console.log('📋 DMG App initialized');
}

// Refresh the memo list
async function refreshMemoList() {
    const memos = await store.getAllMemos();
    memoCount.textContent = memos.length;

    if (memos.length === 0) {
        memoList.innerHTML = `
      <div class="empty-state">
        <p>No decisions yet.</p>
        <p class="empty-hint">Click "+ New MEMO" to start.</p>
      </div>
    `;
    } else {
        memoList.innerHTML = memos
            .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
            .map(memo => renderMemoCard(memo))
            .join('');

        // Attach click handlers
        memoList.querySelectorAll('.memo-card').forEach(card => {
            card.addEventListener('click', () => selectMemo(card.dataset.id));
        });
    }
}

// Render a single memo card
function renderMemoCard(memo) {
    const rampLevel = memo.ramp?.level || 3;
    const date = new Date(memo.updated_at).toLocaleDateString();
    const hasOutcome = memo.outcome?.next_check_date;

    return `
    <div class="memo-card ${memo.memo_id === currentMemoId ? 'active' : ''}" data-id="${memo.memo_id}">
      <div class="memo-card-title">${memo.title || 'Untitled Decision'}</div>
      <div class="memo-card-meta">
        <span class="ramp-badge l${rampLevel}">L${rampLevel}</span>
        <span>${date}</span>
        ${hasOutcome ? '<span>📅</span>' : ''}
      </div>
    </div>
  `;
}

// Select a memo
async function selectMemo(memoId) {
    currentMemoId = memoId;
    const memo = await store.getMemo(memoId);

    if (memo) {
        renderMemoEditor(editorContent, memo);
        rightPanel.style.display = 'block';
        updateRampSelector(memo.ramp?.level || 3);

        // Update outcome date picker
        if (outcomeDate && memo.outcome?.next_check_date) {
            outcomeDate.value = memo.outcome.next_check_date;
        }

        await refreshMemoList();
    }
}

// Update RAMP selector
function updateRampSelector(level) {
    rampSelector.querySelectorAll('.ramp-btn').forEach(btn => {
        btn.classList.toggle('active', parseInt(btn.dataset.level) === level);
    });
}

// Refresh upcoming outcomes
async function refreshUpcomingOutcomes() {
    const upcoming = await getUpcomingOutcomes(store);
    renderUpcomingPanel(upcomingPanel, upcoming, openOutcomeCheck);
}

// Open new memo modal
function openNewMemoModal() {
    // Clear form
    document.getElementById('memo-title').value = '';
    document.getElementById('memo-decision').value = '';
    document.getElementById('memo-recommendation').value = '';
    document.getElementById('memo-owner').value = '';
    document.getElementById('memo-ramp').value = '3';

    // Reset options to 3
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = `
    <div class="option-row">
      <input type="text" class="option-input" placeholder="Option A">
    </div>
    <div class="option-row">
      <input type="text" class="option-input" placeholder="Option B">
    </div>
    <div class="option-row">
      <input type="text" class="option-input" placeholder="Option C (or Do Nothing)">
    </div>
  `;

    showModal(memoModal);
}

// Save new memo
async function saveNewMemo() {
    const title = document.getElementById('memo-title').value;
    const decision = document.getElementById('memo-decision').value;
    const recommendation = document.getElementById('memo-recommendation').value;
    const owner = document.getElementById('memo-owner').value;
    const rampLevel = parseInt(document.getElementById('memo-ramp').value);

    // Get options
    const optionInputs = document.querySelectorAll('.option-input');
    const options = Array.from(optionInputs)
        .map((input, i) => ({
            name: input.value || `Option ${String.fromCharCode(65 + i)}`,
            description: input.value
        }))
        .filter(opt => opt.description);

    // Validate
    if (!title) {
        alert('Please enter a title');
        return;
    }

    if (options.length < 3) {
        alert('Please add at least 3 options');
        return;
    }

    // Create memo
    const memo = {
        title,
        decision,
        options,
        recommendation,
        ramp: { level: rampLevel },
        owners: owner ? [{ name: owner, role: 'Decision Owner' }] : [],
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
    };

    const savedMemo = await store.createMemo(memo);
    hideModal(memoModal);
    await refreshMemoList();
    await selectMemo(savedMemo.memo_id);
}

// Add option input
function addOptionInput() {
    const container = document.getElementById('options-container');
    const optionCount = container.querySelectorAll('.option-row').length;
    const letter = String.fromCharCode(65 + optionCount); // A, B, C, D...

    const row = document.createElement('div');
    row.className = 'option-row';
    row.innerHTML = `<input type="text" class="option-input" placeholder="Option ${letter}">`;
    container.appendChild(row);
}

// ===== SPAR Integration =====

function openSPARModal() {
    currentSparResult = null;
    document.getElementById('spar-question').value = '';
    document.getElementById('spar-context').value = '';
    document.getElementById('spar-status').style.display = 'none';
    document.getElementById('spar-result').style.display = 'none';
    document.getElementById('run-spar').style.display = '';
    document.getElementById('spar-to-memo').style.display = 'none';

    // Reset mode buttons
    document.querySelectorAll('.spar-mode-btn').forEach((btn, i) => {
        btn.classList.toggle('active', i === 0);
    });

    showModal(sparModal);
}

async function handleRunSPAR() {
    const question = document.getElementById('spar-question').value;
    const context = document.getElementById('spar-context').value;
    const activeMode = document.querySelector('.spar-mode-btn.active');
    const mode = activeMode?.dataset.mode || 'quick';

    if (!question) {
        alert('Please enter a decision question');
        return;
    }

    // Show status
    document.getElementById('spar-status').style.display = 'flex';
    document.getElementById('run-spar').style.display = 'none';

    try {
        // Run SPAR
        const result = await runSPAR(question, context, mode, (progress) => {
            document.getElementById('spar-status-text').textContent = progress.message;
        });

        currentSparResult = result;

        // Show result
        document.getElementById('spar-status').style.display = 'none';
        document.getElementById('spar-result').style.display = 'block';
        document.getElementById('spar-to-memo').style.display = '';

        // Render recommendation
        document.getElementById('spar-recommendation').textContent =
            result.synthesis.recommendation + '. ' + result.synthesis.rationale;

        // Render options
        document.getElementById('spar-options').innerHTML = result.positions
            .slice(0, 4)
            .map((pos, i) => `
        <div class="spar-option">
          <span class="spar-option-label">${String.fromCharCode(65 + i)}.</span>
          ${pos.position}
        </div>
      `).join('');

    } catch (error) {
        console.error('SPAR error:', error);
        document.getElementById('spar-status-text').textContent = 'Error: ' + error.message;
    }
}

async function handleSPARToMemo() {
    if (!currentSparResult) return;

    // Convert SPAR to DMG format
    const memoData = sparToDMG(currentSparResult);

    // Create the memo
    const memo = {
        ...memoData,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
    };

    const savedMemo = await store.createMemo(memo);

    hideModal(sparModal);
    await refreshMemoList();
    await selectMemo(savedMemo.memo_id);
}

// ===== Outcome Tracking =====

async function openOutcomeCheck(memoId) {
    const memo = await store.getMemo(memoId);
    if (!memo) return;

    currentOutcomeCheck = prepareOutcomeCheck(memo);

    // Update modal
    document.getElementById('outcome-memo-title').textContent = memo.title;
    document.getElementById('outcome-check-date').textContent =
        `Check date: ${new Date().toLocaleDateString()}`;
    document.getElementById('outcome-actual').value = '';
    document.getElementById('outcome-next-action').value = '';
    document.getElementById('outcome-next-date').value = '';

    // Reset verdict buttons
    document.querySelectorAll('.verdict-btn').forEach(btn => btn.classList.remove('active'));

    // Render audit form
    renderOutcomeForm(outcomeModal, currentOutcomeCheck, (verdict) => {
        currentOutcomeCheck.verdict = verdict;
    });

    showModal(outcomeModal);
}

async function handleSaveOutcome() {
    if (!currentOutcomeCheck) return;

    // Get form values
    currentOutcomeCheck.actual_result = document.getElementById('outcome-actual').value;
    currentOutcomeCheck.next_action = document.getElementById('outcome-next-action').value;
    currentOutcomeCheck.next_check_date = document.getElementById('outcome-next-date').value || null;

    // Get assumption audit values
    document.querySelectorAll('.assumption-check').forEach((checkbox, i) => {
        if (currentOutcomeCheck.assumptions[i]) {
            currentOutcomeCheck.assumptions[i].accurate = checkbox.checked;
        }
    });

    // Get dissent audit values
    document.querySelectorAll('.dissent-check').forEach((checkbox, i) => {
        if (currentOutcomeCheck.dissents[i]) {
            currentOutcomeCheck.dissents[i].vindicated = checkbox.checked;
        }
    });

    if (!currentOutcomeCheck.verdict) {
        alert('Please select a verdict');
        return;
    }

    try {
        await saveOutcomeCheck(store, currentOutcomeCheck.memo_id, currentOutcomeCheck);
        hideModal(outcomeModal);
        await refreshMemoList();
        await refreshUpcomingOutcomes();

        // If the current memo was updated, refresh it
        if (currentMemoId === currentOutcomeCheck.memo_id) {
            await selectMemo(currentMemoId);
        }
    } catch (error) {
        console.error('Error saving outcome:', error);
        alert('Error saving outcome: ' + error.message);
    }
}

// Setup event listeners
function setupEventListeners() {
    // New memo buttons
    newMemoBtn.addEventListener('click', openNewMemoModal);
    editorNewBtn?.addEventListener('click', openNewMemoModal);

    // SPAR button
    sparBtn?.addEventListener('click', openSPARModal);

    // Modal controls
    closeModalBtn.addEventListener('click', () => hideModal(memoModal));
    cancelMemoBtn.addEventListener('click', () => hideModal(memoModal));
    saveMemoBtn.addEventListener('click', saveNewMemo);

    // SPAR modal controls
    document.getElementById('close-spar-modal')?.addEventListener('click', () => hideModal(sparModal));
    document.getElementById('cancel-spar')?.addEventListener('click', () => hideModal(sparModal));
    document.getElementById('run-spar')?.addEventListener('click', handleRunSPAR);
    document.getElementById('spar-to-memo')?.addEventListener('click', handleSPARToMemo);

    // SPAR mode selection
    document.querySelectorAll('.spar-mode-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.spar-mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // Outcome modal controls
    document.getElementById('close-outcome-modal')?.addEventListener('click', () => hideModal(outcomeModal));
    document.getElementById('cancel-outcome')?.addEventListener('click', () => hideModal(outcomeModal));
    document.getElementById('save-outcome')?.addEventListener('click', handleSaveOutcome);

    // Add option
    addOptionBtn.addEventListener('click', addOptionInput);

    // Export
    exportBtn.addEventListener('click', async () => {
        if (currentMemoId) {
            const memo = await store.getMemo(currentMemoId);
            exportMemo(memo);
        } else {
            alert('Select a MEMO to export');
        }
    });

    // RAMP selector
    rampSelector.querySelectorAll('.ramp-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const level = parseInt(btn.dataset.level);
            updateRampSelector(level);

            if (currentMemoId) {
                const memo = await store.getMemo(currentMemoId);
                memo.ramp = { level };
                memo.updated_at = new Date().toISOString();
                await store.updateMemo(memo);
                await refreshMemoList();
            }
        });
    });

    // Outcome date change
    outcomeDate?.addEventListener('change', async (e) => {
        if (currentMemoId) {
            const memo = await store.getMemo(currentMemoId);
            if (!memo.outcome) {
                memo.outcome = { outcome_id: `outcome-${currentMemoId}` };
            }
            memo.outcome.next_check_date = e.target.value;
            memo.updated_at = new Date().toISOString();
            await store.updateMemo(memo);
            await refreshMemoList();
            await refreshUpcomingOutcomes();
        }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Cmd/Ctrl + N = New memo
        if ((e.metaKey || e.ctrlKey) && e.key === 'n') {
            e.preventDefault();
            openNewMemoModal();
        }
        // Cmd/Ctrl + Shift + S = SPAR
        if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key === 's') {
            e.preventDefault();
            openSPARModal();
        }
        // Escape = Close modal
        if (e.key === 'Escape') {
            hideModal(memoModal);
            hideModal(sparModal);
            hideModal(outcomeModal);
        }
    });
}

// Start the app
init();

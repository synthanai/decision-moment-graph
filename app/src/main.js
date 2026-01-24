/**
 * DMG App — Main Entry Point
 * Decision Moment Graph: Stop storing chats. Store decision objects.
 */

import { DMGStore } from './stores/dmg-store.js';
import { renderMemoList, renderMemoEditor } from './components/memo-list.js';
import { showModal, hideModal } from './components/modal.js';
import { exportMemo } from './utils/export.js';

// Initialize the store
const store = new DMGStore();

// DOM Elements
const newMemoBtn = document.getElementById('new-memo-btn');
const editorNewBtn = document.getElementById('editor-new-btn');
const exportBtn = document.getElementById('export-btn');
const memoModal = document.getElementById('memo-modal');
const closeModalBtn = document.getElementById('close-modal');
const cancelMemoBtn = document.getElementById('cancel-memo');
const saveMemoBtn = document.getElementById('save-memo');
const addOptionBtn = document.getElementById('add-option');
const memoList = document.getElementById('memo-list');
const memoCount = document.getElementById('memo-count');
const rightPanel = document.getElementById('right-panel');
const editorContent = document.getElementById('editor-content');
const rampSelector = document.getElementById('ramp-selector');

// State
let currentMemoId = null;

// Initialize app
async function init() {
    await store.init();
    await refreshMemoList();
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

    return `
    <div class="memo-card ${memo.memo_id === currentMemoId ? 'active' : ''}" data-id="${memo.memo_id}">
      <div class="memo-card-title">${memo.title || 'Untitled Decision'}</div>
      <div class="memo-card-meta">
        <span class="ramp-badge l${rampLevel}">L${rampLevel}</span>
        <span>${date}</span>
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
        await refreshMemoList();
    }
}

// Update RAMP selector
function updateRampSelector(level) {
    rampSelector.querySelectorAll('.ramp-btn').forEach(btn => {
        btn.classList.toggle('active', parseInt(btn.dataset.level) === level);
    });
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

// Setup event listeners
function setupEventListeners() {
    // New memo buttons
    newMemoBtn.addEventListener('click', openNewMemoModal);
    editorNewBtn?.addEventListener('click', openNewMemoModal);

    // Modal controls
    closeModalBtn.addEventListener('click', () => hideModal(memoModal));
    cancelMemoBtn.addEventListener('click', () => hideModal(memoModal));
    saveMemoBtn.addEventListener('click', saveNewMemo);

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

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Cmd/Ctrl + N = New memo
        if ((e.metaKey || e.ctrlKey) && e.key === 'n') {
            e.preventDefault();
            openNewMemoModal();
        }
        // Escape = Close modal
        if (e.key === 'Escape') {
            hideModal(memoModal);
        }
    });
}

// Start the app
init();

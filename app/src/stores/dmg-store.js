/**
 * DMG Store — IndexedDB-backed Local Storage
 * Offline-first decision storage
 */

const DB_NAME = 'dmg-app';
const DB_VERSION = 1;
const MEMO_STORE = 'memos';
const MOMENT_STORE = 'moments';

export class DMGStore {
    constructor() {
        this.db = null;
    }

    async init() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(DB_NAME, DB_VERSION);

            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve();
            };

            request.onupgradeneeded = (event) => {
                const db = event.target.result;

                // MEMOs store
                if (!db.objectStoreNames.contains(MEMO_STORE)) {
                    const memoStore = db.createObjectStore(MEMO_STORE, { keyPath: 'memo_id' });
                    memoStore.createIndex('title', 'title', { unique: false });
                    memoStore.createIndex('updated_at', 'updated_at', { unique: false });
                }

                // MOMENTs store (provenance events)
                if (!db.objectStoreNames.contains(MOMENT_STORE)) {
                    const momentStore = db.createObjectStore(MOMENT_STORE, { keyPath: 'moment_id' });
                    momentStore.createIndex('memo_id', 'memo_id', { unique: false });
                }
            };
        });
    }

    // Generate unique ID
    generateId() {
        return 'dmg-' + Date.now().toString(36) + '-' + Math.random().toString(36).substr(2, 9);
    }

    // MEMO Operations
    async createMemo(memoData) {
        const memo = {
            dmg_version: '0.1',
            memo_id: this.generateId(),
            ...memoData,
            created_at: memoData.created_at || new Date().toISOString(),
            updated_at: new Date().toISOString(),
            version: 1
        };

        return new Promise((resolve, reject) => {
            const tx = this.db.transaction(MEMO_STORE, 'readwrite');
            const store = tx.objectStore(MEMO_STORE);
            const request = store.add(memo);

            request.onsuccess = () => {
                // Create initial MOMENT event
                this.addMomentEvent(memo.memo_id, 'MEMO_CREATED', {
                    title: memo.title
                });
                resolve(memo);
            };
            request.onerror = () => reject(request.error);
        });
    }

    async getMemo(memoId) {
        return new Promise((resolve, reject) => {
            const tx = this.db.transaction(MEMO_STORE, 'readonly');
            const store = tx.objectStore(MEMO_STORE);
            const request = store.get(memoId);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    async getAllMemos() {
        return new Promise((resolve, reject) => {
            const tx = this.db.transaction(MEMO_STORE, 'readonly');
            const store = tx.objectStore(MEMO_STORE);
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result || []);
            request.onerror = () => reject(request.error);
        });
    }

    async updateMemo(memo) {
        memo.updated_at = new Date().toISOString();
        memo.version = (memo.version || 0) + 1;

        return new Promise((resolve, reject) => {
            const tx = this.db.transaction(MEMO_STORE, 'readwrite');
            const store = tx.objectStore(MEMO_STORE);
            const request = store.put(memo);

            request.onsuccess = () => {
                this.addMomentEvent(memo.memo_id, 'MEMO_UPDATED', {
                    version: memo.version
                });
                resolve(memo);
            };
            request.onerror = () => reject(request.error);
        });
    }

    async deleteMemo(memoId) {
        return new Promise((resolve, reject) => {
            const tx = this.db.transaction(MEMO_STORE, 'readwrite');
            const store = tx.objectStore(MEMO_STORE);
            const request = store.delete(memoId);

            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }

    // MOMENT Operations
    async addMomentEvent(memoId, type, payload) {
        const moment = await this.getMoment(memoId) || {
            moment_id: 'moment-' + memoId,
            memo_id: memoId,
            events: []
        };

        const seq = moment.events.length + 1;
        const prevHash = moment.events.length > 0
            ? moment.events[moment.events.length - 1].hash
            : '';

        const event = {
            event_id: 'evt-' + this.generateId(),
            seq,
            ts: new Date().toISOString(),
            type,
            actor: 'local-user', // TODO: Support user identity
            payload,
            prev_hash: prevHash,
            hash: await this.hashEvent(seq, type, payload, prevHash)
        };

        moment.events.push(event);

        return new Promise((resolve, reject) => {
            const tx = this.db.transaction(MOMENT_STORE, 'readwrite');
            const store = tx.objectStore(MOMENT_STORE);
            const request = store.put(moment);

            request.onsuccess = () => resolve(event);
            request.onerror = () => reject(request.error);
        });
    }

    async getMoment(memoId) {
        const momentId = 'moment-' + memoId;

        return new Promise((resolve, reject) => {
            const tx = this.db.transaction(MOMENT_STORE, 'readonly');
            const store = tx.objectStore(MOMENT_STORE);
            const request = store.get(momentId);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Hash an event (simple implementation)
    async hashEvent(seq, type, payload, prevHash) {
        const data = JSON.stringify({ seq, type, payload, prevHash });
        const encoder = new TextEncoder();
        const dataBuffer = encoder.encode(data);

        // Use SubtleCrypto for SHA-256
        const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

        return hashHex.substring(0, 12); // Short hash for display
    }

    // Export full DMG
    async exportDMG(memoId) {
        const memo = await this.getMemo(memoId);
        const moment = await this.getMoment(memoId);

        if (!memo) return null;

        return {
            dmg_version: '0.1',
            memo,
            moment: moment || { moment_id: 'moment-' + memoId, memo_id: memoId, events: [] },
            objects: {
                dissents: memo.dissents || [],
                traces: memo.traces || [],
                commit: memo.commit || { state: 'Draft' },
                outcome: memo.outcome || {}
            }
        };
    }
}

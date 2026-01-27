/**
 * Cross-Kit Decision Replay
 * 
 * Enables replaying decisions across kits for:
 * - Post-mortem analysis
 * - Alternative scenario testing
 * - Training data generation
 * 
 * @module decision-moment-graph/replay
 */

/**
 * Replay modes
 */
const REPLAY_MODES = {
    EXACT: 'exact',           // Replay with same inputs
    COUNTERFACTUAL: 'counter', // Replay with modified inputs
    ACCELERATED: 'fast',       // Skip waiting periods
    INSTRUMENTED: 'trace'      // Full GAUGE emission
};

/**
 * Stored decision snapshots
 */
const decisionSnapshots = new Map();

/**
 * Capture a decision snapshot for replay
 * 
 * @param {Object} decision - Decision to snapshot
 * @returns {string} Snapshot ID
 */
function captureSnapshot(decision) {
    const snapshotId = `snap_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;

    const snapshot = {
        id: snapshotId,
        capturedAt: new Date().toISOString(),
        decision: {
            id: decision.id,
            question: decision.question,
            context: decision.context,
            options: decision.options
        },
        phases: decision.phases || [],
        outcome: decision.outcome,
        metadata: {
            duration: decision.duration,
            participantCount: decision.participants?.length || 0,
            gaugeScore: decision.gaugeScore
        }
    };

    decisionSnapshots.set(snapshotId, snapshot);
    return snapshotId;
}

/**
 * Replay a decision with optional modifications
 * 
 * @param {string} snapshotId - Snapshot to replay
 * @param {Object} options - Replay options
 * @returns {Object} Replay result
 */
function replayDecision(snapshotId, options = {}) {
    const snapshot = decisionSnapshots.get(snapshotId);

    if (!snapshot) {
        return { success: false, error: 'Snapshot not found' };
    }

    const {
        mode = REPLAY_MODES.EXACT,
        modifications = {},
        targetPhase = null
    } = options;

    // Build replay context
    const replayContext = {
        replayId: `replay_${Date.now()}`,
        originalSnapshotId: snapshotId,
        mode,
        startedAt: new Date().toISOString(),
        decision: { ...snapshot.decision }
    };

    // Apply modifications for counterfactual replay
    if (mode === REPLAY_MODES.COUNTERFACTUAL && modifications) {
        if (modifications.context) {
            replayContext.decision.context = {
                ...replayContext.decision.context,
                ...modifications.context
            };
        }
        if (modifications.options) {
            replayContext.decision.options = modifications.options;
        }
        if (modifications.question) {
            replayContext.decision.question = modifications.question;
        }
    }

    // Filter phases if target specified
    let phasesToReplay = snapshot.phases;
    if (targetPhase) {
        const phaseIndex = phasesToReplay.findIndex(p => p.name === targetPhase);
        if (phaseIndex >= 0) {
            phasesToReplay = phasesToReplay.slice(0, phaseIndex + 1);
        }
    }

    // Execute replay (simulated)
    const replayResult = {
        ...replayContext,
        phasesReplayed: phasesToReplay.map(phase => ({
            name: phase.name,
            originalDuration: phase.duration,
            replayDuration: mode === REPLAY_MODES.ACCELERATED ? 0 : phase.duration,
            inputsMatched: mode === REPLAY_MODES.EXACT,
            gaugeEmitted: mode === REPLAY_MODES.INSTRUMENTED
        })),
        completedAt: new Date().toISOString(),
        success: true
    };

    // Compare outcomes for counterfactual
    if (mode === REPLAY_MODES.COUNTERFACTUAL) {
        replayResult.outcomeComparison = {
            original: snapshot.outcome,
            replayed: 'simulated', // Would be actual outcome in real implementation
            divergencePoint: modifications.context ? 'context' : 'options'
        };
    }

    return replayResult;
}

/**
 * Generate training data from decision history
 * 
 * @param {Object} options - Filter options
 * @returns {Array} Training examples
 */
function generateTrainingData(options = {}) {
    const { minGaugeScore = 0.7, limit = 100 } = options;

    const examples = [];

    for (const [id, snapshot] of decisionSnapshots) {
        if (snapshot.metadata.gaugeScore >= minGaugeScore) {
            examples.push({
                input: {
                    question: snapshot.decision.question,
                    context: snapshot.decision.context,
                    options: snapshot.decision.options
                },
                output: {
                    outcome: snapshot.outcome,
                    reasoning: snapshot.phases.map(p => p.summary).filter(Boolean)
                },
                quality: snapshot.metadata.gaugeScore
            });
        }

        if (examples.length >= limit) break;
    }

    return examples;
}

/**
 * Get snapshot history
 */
function getSnapshotHistory(options = {}) {
    const { since, question } = options;

    let snapshots = Array.from(decisionSnapshots.values());

    if (since) {
        snapshots = snapshots.filter(s => new Date(s.capturedAt) > new Date(since));
    }

    if (question) {
        snapshots = snapshots.filter(s =>
            s.decision.question.toLowerCase().includes(question.toLowerCase())
        );
    }

    return snapshots.map(s => ({
        id: s.id,
        question: s.decision.question.substring(0, 50),
        capturedAt: s.capturedAt,
        gaugeScore: s.metadata.gaugeScore
    }));
}

/**
 * Delete a snapshot
 */
function deleteSnapshot(snapshotId) {
    return decisionSnapshots.delete(snapshotId);
}

module.exports = {
    REPLAY_MODES,
    captureSnapshot,
    replayDecision,
    generateTrainingData,
    getSnapshotHistory,
    deleteSnapshot
};

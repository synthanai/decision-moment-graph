/**
 * DMS-Kit GAUGE Emitter
 * 
 * Emits GAUGE_EVENT at each Heptagon phase completion.
 * This is the source of truth for GAUGE events in the ecosystem.
 * 
 * @module decision-moment-graph/gauge-emitter
 */

/**
 * Heptagon phase names (7-step decision protocol)
 */
export const HEPTAGON_PHASES = {
    SCOPE: 'scope',      // Define the decision space
    POPULATE: 'populate', // Gather stakeholders/personas
    RUMBLE: 'rumble',    // Structured disagreement
    KNIT: 'knit',        // Synthesize tensions
    INTERROGATE: 'interrogate', // Challenge the synthesis
    TRANSMIT: 'transmit', // Commit and broadcast
    GAUGE: 'gauge'       // Retrospective learning
};

/**
 * Emit GAUGE_EVENT from DMS after phase completion
 * 
 * @param {string} phase - Which Heptagon phase just completed
 * @param {Object} moment - The decision moment context
 * @param {Object} insight - The insight/outcome from this phase
 * @param {Object} options - Additional options
 * @returns {Object|null} The emitted event, or null if event bus unavailable
 */
export async function emitDmsGaugeEvent(phase, moment, insight, options = {}) {
    try {
        // Dynamic import to avoid hard dependency
        const { emitGaugeEvent } = await import('agentic-kit/src/core/event-bus.js');

        const event = emitGaugeEvent(
            moment,
            {
                category: `dms_phase_${phase}`,
                phase,
                summary: insight.summary || `Phase ${phase} completed`,
                delta: insight.delta || 0,
                confidence: insight.confidence || 0.5,
                ...insight
            },
            {
                source: 'dms-kit',
                priority: options.priority || 'medium',
                ...options
            }
        );

        return event;

    } catch (error) {
        // Event bus not available — log and continue silently
        if (options.verbose) {
            console.log(`[DMS] GAUGE emit failed: ${error.message}`);
        }
        return null;
    }
}

/**
 * Emit GAUGE_EVENT specifically for the GAUGE phase (meta-learning)
 * This is the final phase that triggers ecosystem-wide learning.
 * 
 * @param {Object} moment - The decision moment
 * @param {Object} retrospective - The retrospective analysis
 * @returns {Object|null} The emitted event
 */
export async function emitGaugePhaseEvent(moment, retrospective) {
    return emitDmsGaugeEvent(
        HEPTAGON_PHASES.GAUGE,
        moment,
        {
            summary: retrospective.summary || 'GAUGE phase complete',
            delta: retrospective.scoreChange || 0,
            confidence: retrospective.confidence || 0.7,
            learnings: retrospective.learnings || [],
            recommendations: retrospective.recommendations || []
        },
        { priority: 'high' } // GAUGE phase events are always high priority
    );
}

/**
 * Create a DMS moment wrapper that auto-emits GAUGE events
 * 
 * @param {Object} moment - Base decision moment
 * @returns {Object} Wrapped moment with GAUGE emission
 */
export function createGaugeTrackedMoment(moment) {
    return {
        ...moment,
        _gaugeEmissions: [],

        async completePhase(phase, insight) {
            const event = await emitDmsGaugeEvent(phase, moment, insight);
            if (event) {
                this._gaugeEmissions.push(event);
            }
            return event;
        },

        async completeGauge(retrospective) {
            return emitGaugePhaseEvent(moment, retrospective);
        },

        getEmissions() {
            return this._gaugeEmissions;
        }
    };
}

export default {
    HEPTAGON_PHASES,
    emitDmsGaugeEvent,
    emitGaugePhaseEvent,
    createGaugeTrackedMoment
};

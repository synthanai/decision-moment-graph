/**
 * SPAR Service — Integration with SPAR deliberation engine
 * 
 * This service simulates/connects to SPAR for structured deliberation
 * before creating a DMG MEMO.
 */

// SPAR Mode configurations
const SPAR_MODES = {
    quick: {
        agents: 2,
        duration: 30000,
        pattern: 'dialectic',
        depth: 'argue'
    },
    balanced: {
        agents: 4,
        duration: 60000,
        pattern: 'news',
        depth: 'clash'
    },
    deep: {
        agents: 8,
        duration: 180000,
        pattern: 'panel',
        depth: 'probe'
    }
};

/**
 * Run a SPAR deliberation session
 * 
 * @param {string} question - The decision question
 * @param {string} context - Optional context/constraints
 * @param {string} mode - 'quick', 'balanced', or 'deep'
 * @param {function} onProgress - Progress callback
 * @returns {Promise<Object>} SPAR output
 */
export async function runSPAR(question, context, mode = 'balanced', onProgress = () => { }) {
    const config = SPAR_MODES[mode];

    onProgress({ stage: 'starting', message: 'Initializing SPAR session...' });

    // Check if SPAR Arena API is available
    const sparEndpoint = getSPAREndpoint();

    if (sparEndpoint) {
        // Real SPAR integration
        return await runSPARRemote(sparEndpoint, question, context, config, onProgress);
    } else {
        // Simulated SPAR for demo/offline
        return await runSPARSimulated(question, context, config, onProgress);
    }
}

/**
 * Get SPAR Arena endpoint from config
 */
function getSPAREndpoint() {
    // Check for local SPAR Arena
    if (typeof window !== 'undefined') {
        return localStorage.getItem('spar_endpoint') ||
            window.SPAR_ENDPOINT ||
            null;  // Return null to use simulated mode
    }
    return null;
}

/**
 * Run SPAR via remote API (SPAR Arena)
 */
async function runSPARRemote(endpoint, question, context, config, onProgress) {
    try {
        onProgress({ stage: 'connecting', message: 'Connecting to SPAR Arena...' });

        const response = await fetch(`${endpoint}/api/spar/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question,
                context,
                config: {
                    pattern: config.pattern,
                    depth: config.depth,
                    agents: config.agents
                }
            })
        });

        if (!response.ok) {
            throw new Error(`SPAR Arena error: ${response.statusText}`);
        }

        const result = await response.json();
        onProgress({ stage: 'complete', message: 'SPAR complete!' });

        return result;
    } catch (error) {
        console.error('SPAR Remote error:', error);
        // Fallback to simulated
        return await runSPARSimulated(question, context, config, onProgress);
    }
}

/**
 * Simulated SPAR for demo/offline use
 * Generates structured deliberation output
 */
async function runSPARSimulated(question, context, config, onProgress) {
    const { agents, duration } = config;

    // Simulate deliberation phases
    const phases = [
        { stage: 'framing', message: 'Framing the decision...', time: 0.1 },
        { stage: 'positions', message: 'Generating positions...', time: 0.2 },
        { stage: 'clash', message: 'Positions clashing...', time: 0.4 },
        { stage: 'probe', message: 'Probing weaknesses...', time: 0.2 },
        { stage: 'synthesis', message: 'Synthesizing...', time: 0.1 }
    ];

    for (const phase of phases) {
        onProgress(phase);
        await delay(duration * phase.time);
    }

    // Generate simulated SPAR output
    const positions = generatePositions(question, context, agents);
    const synthesis = generateSynthesis(positions, question);

    onProgress({ stage: 'complete', message: 'SPAR complete!' });

    return {
        spar_id: `spar-${Date.now()}`,
        question,
        context,
        config,
        positions,
        synthesis,
        transcript: generateTranscript(positions),
        probe: {
            plurality: 8,
            rigor: 7,
            origin: 8,
            basis: 7,
            execution: 8
        }
    };
}

/**
 * Generate positions based on question
 */
function generatePositions(question, context, agentCount) {
    const positionTemplates = [
        {
            agent: 'north',
            role: 'Champion',
            stance: 'proactive',
            prefix: 'We should move forward with'
        },
        {
            agent: 'east',
            role: 'Challenger',
            stance: 'skeptical',
            prefix: 'We should reconsider because'
        },
        {
            agent: 'south',
            role: 'Pragmatist',
            stance: 'practical',
            prefix: 'A balanced approach would be'
        },
        {
            agent: 'west',
            role: 'Sage',
            stance: 'cautious',
            prefix: 'History suggests we should'
        },
        {
            agent: 'northeast',
            role: 'Innovator',
            stance: 'exploratory',
            prefix: 'An emerging option is'
        },
        {
            agent: 'southeast',
            role: 'Analyst',
            stance: 'data-driven',
            prefix: 'The data indicates'
        },
        {
            agent: 'southwest',
            role: 'Steward',
            stance: 'risk-aware',
            prefix: 'To minimize risk, we could'
        },
        {
            agent: 'northwest',
            role: 'Visionary',
            stance: 'long-term',
            prefix: 'For long-term value,'
        }
    ];

    // Extract key terms from question
    const questionLower = question.toLowerCase();
    const isBuildBuy = questionLower.includes('build') || questionLower.includes('buy');
    const isHire = questionLower.includes('hire') || questionLower.includes('team');
    const isPriority = questionLower.includes('prioriti') || questionLower.includes('first');

    return positionTemplates.slice(0, agentCount).map((template, i) => {
        let position = '';
        let arguments_ = [];

        if (isBuildBuy) {
            const options = ['build in-house', 'buy a vendor solution', 'hybrid approach', 'defer decision'];
            position = `${template.prefix} ${options[i % 4]}`;
            arguments_ = getArgumentsForBuildBuy(i);
        } else if (isHire) {
            const options = ['hire externally', 'promote internally', 'contract first', 'restructure existing'];
            position = `${template.prefix} ${options[i % 4]}`;
            arguments_ = getArgumentsForHiring(i);
        } else if (isPriority) {
            const options = ['Option A first', 'Option B first', 'parallel execution', 'defer both'];
            position = `${template.prefix} ${options[i % 4]}`;
            arguments_ = getArgumentsForPriority(i);
        } else {
            position = `${template.prefix} a structured approach`;
            arguments_ = ['Reduces uncertainty', 'Enables learning', 'Maintains flexibility'];
        }

        return {
            agent: template.agent,
            role: template.role,
            position,
            arguments: arguments_,
            evidence: []
        };
    });
}

function getArgumentsForBuildBuy(index) {
    const args = [
        ['Full control and customization', 'No vendor lock-in', 'Team expertise grows'],
        ['Faster time-to-value', 'Lower initial risk', 'Focus on core competency'],
        ['Best of both worlds', 'Reduce complexity gradually', 'Flexible adaptation'],
        ['Validate need first', 'Preserve resources', 'Wait for market clarity']
    ];
    return args[index % 4];
}

function getArgumentsForHiring(index) {
    const args = [
        ['Fresh perspectives', 'Immediate skill gap fill', 'Market-tested talent'],
        ['Cultural continuity', 'Loyalty and retention', 'Known performance'],
        ['Test fit before commit', 'Flexibility', 'Lower initial risk'],
        ['Maximize existing talent', 'Cost efficiency', 'Avoid onboarding overhead']
    ];
    return args[index % 4];
}

function getArgumentsForPriority(index) {
    const args = [
        ['Higher impact potential', 'Dependencies favor this order', 'Resource availability'],
        ['Lower risk starting point', 'Quick wins build momentum', 'Clearer requirements'],
        ['Speed through parallelism', 'Resource efficiency', 'Hedges uncertainty'],
        ['Wait for more information', 'Current priorities sufficient', 'Avoid overcommitment']
    ];
    return args[index % 4];
}

/**
 * Generate synthesis from positions
 */
function generateSynthesis(positions, question) {
    // Pick the most practical position as recommendation
    const recommendedPosition = positions.find(p => p.role === 'Pragmatist') || positions[0];

    // Identify tensions
    const tensions = positions
        .filter(p => p.role === 'Challenger' || p.role === 'Sage')
        .map(p => p.position);

    return {
        recommendation: recommendedPosition.position,
        confidence: 0.7,
        rationale: `This approach balances the competing concerns while maintaining flexibility. ${recommendedPosition.arguments[0]}.`,
        key_tensions: tensions.slice(0, 2),
        conditions_to_reverse: [
            'If initial results are significantly below expectations',
            'If key assumptions prove false within 30 days'
        ]
    };
}

/**
 * Generate transcript events
 */
function generateTranscript(positions) {
    let seq = 1;
    const transcript = [];

    for (const pos of positions) {
        transcript.push({
            seq: seq++,
            ts: new Date().toISOString(),
            agent: pos.agent,
            type: 'position',
            content: pos.position
        });
    }

    // Add some rebuttals
    if (positions.length >= 2) {
        transcript.push({
            seq: seq++,
            ts: new Date().toISOString(),
            agent: positions[1].agent,
            type: 'rebuttal',
            content: `However, this overlooks ${positions[1].arguments[0].toLowerCase()}.`
        });
    }

    return transcript;
}

/**
 * Convert SPAR output to DMG MEMO format
 */
export function sparToDMG(sparOutput) {
    const { question, context, positions, synthesis, probe } = sparOutput;

    // Map positions to options
    const options = positions.map((pos, i) => ({
        name: `Option ${String.fromCharCode(65 + i)}: ${pos.role}`,
        description: pos.position,
        pros: pos.arguments,
        cons: [],
        source: `spar:${pos.agent}`
    }));

    // Parse context into constraints
    const constraints = context ?
        context.split(/[;,.]/).map(c => c.trim()).filter(c => c) :
        [];

    // Calculate suggested RAMP
    const suggestedRamp = calculateSuggestedRamp(sparOutput);

    return {
        title: question,
        decision: synthesis.recommendation,
        context: {
            constraints,
            assumptions: []
        },
        options,
        recommendation: `${synthesis.recommendation}. ${synthesis.rationale}`,
        ramp: {
            level: suggestedRamp,
            justification: 'Auto-assigned from SPAR; review recommended'
        },
        expected_outcomes: [
            {
                metric: 'Decision confidence',
                expected: 'Successful outcome',
                confidence: synthesis.confidence,
                notes: `PROBE score: P${probe.plurality} R${probe.rigor} O${probe.origin} B${probe.basis} E${probe.execution}`
            }
        ],
        dissents: positions
            .filter(p => p.role === 'Challenger' || p.role === 'Sage')
            .map(p => ({
                dissent_id: `dissent-${p.agent}`,
                author: `spar:${p.agent}`,
                claim: p.position,
                evidence: p.arguments,
                conditions_to_change_mind: synthesis.conditions_to_reverse[0] || ''
            })),
        spar_source: {
            spar_id: sparOutput.spar_id,
            mode: sparOutput.config?.pattern,
            probe_score: probe
        }
    };
}

/**
 * Calculate suggested RAMP level from SPAR
 */
function calculateSuggestedRamp(sparOutput) {
    const { synthesis, config } = sparOutput;

    let level = 3; // Default

    // Lower confidence = higher RAMP
    if (synthesis.confidence < 0.5) {
        level = Math.min(5, level + 1);
    }

    // More tensions = higher RAMP
    if (synthesis.key_tensions?.length > 2) {
        level = Math.min(5, level + 1);
    }

    // Deeper deliberation usually means higher stakes
    if (config?.depth === 'probe') {
        level = Math.min(5, level + 1);
    }

    return level;
}

// Utility
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

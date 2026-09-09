/* =========================================================
   NEON BREACH // Cyberpunk Escape-Room Graphical Web Engine
   ========================================================= */

// Audio Synthesizer using Web Audio API
class AudioSynth {
    constructor() {
        this.ctx = null;
        this.enabled = true;
    }

    init() {
        if (!this.ctx) {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    playTone(freq, type = 'sine', duration = 0.15, volume = 0.15) {
        if (!this.enabled || !this.ctx) return;
        try {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
            gain.gain.setValueAtTime(volume, this.ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start();
            osc.stop(this.ctx.currentTime + duration);
        } catch (e) {}
    }

    playClick() {
        this.playTone(800, 'square', 0.05, 0.08);
    }

    playSuccess() {
        if (!this.enabled) return;
        this.playTone(523.25, 'triangle', 0.15, 0.2); // C5
        setTimeout(() => this.playTone(659.25, 'triangle', 0.15, 0.2), 100); // E5
        setTimeout(() => this.playTone(783.99, 'triangle', 0.25, 0.25), 200); // G5
    }

    playAlarm() {
        if (!this.enabled) return;
        this.playTone(220, 'sawtooth', 0.2, 0.25);
        setTimeout(() => this.playTone(180, 'sawtooth', 0.2, 0.25), 150);
    }
}

const audio = new AudioSynth();

// Background Matrix Canvas Generator
function initMatrixCanvas() {
    const canvas = document.getElementById('bg-canvas');
    const ctx = canvas.getContext('2d');
    
    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const chars = '01ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*+=-';
    const fontSize = 14;
    const columns = Math.floor(canvas.width / fontSize);
    const drops = Array(columns).fill(1);

    function draw() {
        ctx.fillStyle = 'rgba(8, 9, 17, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#00f3ff';
        ctx.font = `${fontSize}px 'Share Tech Mono'`;

        for (let i = 0; i < drops.length; i++) {
            const text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }

    setInterval(draw, 45);
}

// Game State Engine
class NeonEngine {
    constructor() {
        this.runnerHandle = 'NEO_RUNNER';
        this.difficulty = 'CYBERPUNK';
        this.currentLayer = 0;
        this.totalLayers = 5;
        
        this.integrity = 100;
        this.tracePercent = 0;
        this.score = 0;
        
        this.timerLimit = 60;
        this.timerLeft = 60;
        this.timerInterval = null;
        
        this.activePuzzle = null;
        this.hintsUsed = 0;
        this.startTime = 0;
    }

    start(handle, difficulty) {
        this.runnerHandle = handle || 'NETRUNNER_X';
        this.difficulty = difficulty || 'CYBERPUNK';
        this.currentLayer = 0;
        this.integrity = 100;
        this.tracePercent = 0;
        this.score = 0;
        
        if (this.difficulty === 'NOVICE') {
            this.totalLayers = 4;
            this.timerLimit = 90;
        } else if (this.difficulty === 'BLACK_ICE') {
            this.totalLayers = 5;
            this.timerLimit = 45;
        } else {
            this.totalLayers = 5;
            this.timerLimit = 60;
        }

        this.startTime = Date.now();
        this.loadLayer(0);
    }

    loadLayer(layerIdx) {
        this.currentLayer = layerIdx;
        this.hintsUsed = 0;
        this.timerLeft = this.timerLimit;

        this.stopTimer();
        this.startTimer();

        // Generate procedural puzzle for node
        if (layerIdx === 0) {
            this.activePuzzle = this.genLogicPuzzle();
        } else if (layerIdx === 1) {
            this.activePuzzle = this.genCryptoPuzzle();
        } else if (layerIdx === 2) {
            this.activePuzzle = this.genAnomalyPuzzle();
        } else if (layerIdx === 3) {
            this.activePuzzle = this.genSequencePuzzle();
        } else {
            this.activePuzzle = this.genKeypadPuzzle();
        }
    }

    startTimer() {
        this.timerInterval = setInterval(() => {
            this.timerLeft -= 0.1;
            if (this.timerLeft <= 0) {
                this.timerLeft = 0;
                this.stopTimer();
                this.onTimeExpired();
            }
            updateHUD();
        }, 100);
    }

    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    onTimeExpired() {
        this.tracePercent = 100;
        audio.playAlarm();
        showDefeatModal();
    }

    submitPayload(payload) {
        const isCorrect = this.activePuzzle.evaluate(payload);
        
        if (isCorrect) {
            audio.playSuccess();
            const timeBonus = Math.floor(this.timerLeft * 25);
            const basePoints = this.difficulty === 'NOVICE' ? 1000 : (this.difficulty === 'CYBERPUNK' ? 1500 : 2500);
            const points = Math.max(300, basePoints + timeBonus - (this.hintsUsed * 250));
            
            this.score += points;
            this.tracePercent = Math.max(0, this.tracePercent - 10);
            
            logMessage(`[ACCESS GRANTED] Node 0${this.currentLayer + 1} pwned! +${points} PTS.`, 'text-green');

            this.currentLayer++;
            if (this.currentLayer >= this.totalLayers) {
                this.stopTimer();
                showVictoryModal();
            } else {
                this.loadLayer(this.currentLayer);
                renderStage();
            }
        } else {
            audio.playAlarm();
            const penalty = this.difficulty === 'NOVICE' ? 15 : (this.difficulty === 'CYBERPUNK' ? 25 : 35);
            this.tracePercent += penalty;
            this.integrity -= 15;

            logMessage(`[ACCESS DENIED] Payload failed! TRACE +${penalty}%.`, 'text-red');

            if (this.tracePercent >= 100 || this.integrity <= 0) {
                this.tracePercent = 100;
                this.integrity = 0;
                this.stopTimer();
                showDefeatModal();
            }
        }
        updateHUD();
    }

    // Procedural Puzzle Generators
    genLogicPuzzle() {
        const switches = { A: true, B: false, C: true };
        return {
            type: 'LOGIC',
            title: 'NODE 01: LOGIC GATE CIRCUIT OVERRIDE',
            sub: 'Toggle input switches so the final logic gate produces HIGH (1) output.',
            switches: switches,
            expr: '(A AND B) XOR (NOT C)',
            solutionTarget: '1',
            evaluate: function(userSwitches) {
                const A = userSwitches.A;
                const B = userSwitches.B;
                const C = userSwitches.C;
                const part1 = A && B;
                const part2 = !C;
                const finalOut = part1 !== part2; // XOR
                return finalOut === true;
            },
            hint: 'Set C = TRUE so that (NOT C) becomes FALSE. Then make (A AND B) = TRUE by turning both A and B ON.'
        };
    }

    genCryptoPuzzle() {
        const words = ['FIREWALL', 'NETRUNNER', 'MAINFRAME', 'OVERRIDE', 'QUANTUM'];
        const word = words[Math.floor(Math.random() * words.length)];
        const shift = 3;
        
        let cipher = '';
        for (let i = 0; i < word.length; i++) {
            cipher += String.fromCharCode(((word.charCodeAt(i) - 65 + shift) % 26) + 65);
        }

        return {
            type: 'CRYPTO',
            title: 'NODE 02: CAESAR CIPHER DECRYPTION',
            sub: `Decrypt shift offset +${shift} payload keyword: [ ${cipher} ]`,
            solution: word,
            evaluate: (ans) => (ans || '').trim().toUpperCase() === word,
            hint: `Shift each letter backwards by ${shift} positions in the alphabet.`
        };
    }

    genAnomalyPuzzle() {
        const syms = ['▲', '■', '◆', '●', '★'];
        const normal = syms[Math.floor(Math.random() * syms.length)];
        let anomaly = syms[Math.floor(Math.random() * syms.length)];
        while (anomaly === normal) anomaly = syms[Math.floor(Math.random() * syms.length)];

        const targetR = Math.floor(Math.random() * 4);
        const targetC = Math.floor(Math.random() * 4);

        const grid = [];
        for (let r = 0; r < 4; r++) {
            const row = [];
            for (let c = 0; c < 4; c++) {
                row.push(r === targetR && c === targetC ? anomaly : normal);
            }
            grid.push(row);
        }

        return {
            type: 'ANOMALY',
            title: 'NODE 03: MEMORY GRID ANOMALY SCANNER',
            sub: `Click directly on the anomalous node symbol '${anomaly}' in the neural matrix.`,
            grid: grid,
            targetR: targetR,
            targetC: targetC,
            evaluate: (coord) => coord === `${targetR},${targetC}`,
            hint: `The corrupted symbol '${anomaly}' is located in Row ${targetR + 1}.`
        };
    }

    genSequencePuzzle() {
        const start = Math.floor(Math.random() * 4) + 2;
        const mult = 2;
        const offset = 3;
        const seq = [start];
        for (let i = 0; i < 4; i++) {
            seq.push(seq[seq.length - 1] * mult + offset);
        }
        const nextVal = seq[seq.length - 1] * mult + offset;

        return {
            type: 'SEQUENCE',
            title: 'NODE 04: FREQUENCY BUS SEQUENCE',
            sub: `Compute the next frequency value in sequence: [ ${seq.join(', ')}, ??? ]`,
            solution: nextVal.toString(),
            evaluate: (ans) => (ans || '').trim() === nextVal.toString(),
            hint: `Rule: Multiply previous value by ${mult} and add ${offset}.`
        };
    }

    genKeypadPuzzle() {
        const chars = '0123456789ABCDEF';
        let secret = '';
        for (let i = 0; i < 4; i++) {
            secret += chars[Math.floor(Math.random() * chars.length)];
        }

        return {
            type: 'KEYPAD',
            title: 'NODE 05: BLACK-ICE HEX KEYPAD CODEBREAKER',
            sub: 'Enter 4-character Hexadecimal PIN. Use feedback reel clues.',
            solution: secret,
            history: [],
            evaluate: function(guess) {
                if (!guess || guess.length !== 4) return false;
                let exact = 0;
                let partial = 0;
                for (let i = 0; i < 4; i++) {
                    if (guess[i] === secret[i]) exact++;
                    else if (secret.includes(guess[i])) partial++;
                }
                this.history.push({ guess, exact, partial });
                return guess === secret;
            },
            hint: `Secret PIN starts with character '${secret[0]}' and ends with '${secret[3]}'.`
        };
    }
}

const engine = new NeonEngine();

// DOM Element References & Event Handlers
document.addEventListener('DOMContentLoaded', () => {
    initMatrixCanvas();
    audio.init();

    // Start Game Button
    document.getElementById('btn-start-game').addEventListener('click', () => {
        audio.init();
        audio.playClick();
        const handle = document.getElementById('input-handle').value.trim() || 'NETRUNNER_X';
        const difficulty = document.getElementById('select-difficulty').value;
        
        hideModal();
        engine.start(handle, difficulty);
        updateHUD();
        renderStage();
        logMessage(`[SYSTEM] Neural link initialized. Runner ${handle} active.`, 'text-cyan');
    });

    // Audio Toggle Button
    document.getElementById('btn-audio').addEventListener('click', () => {
        audio.enabled = !audio.enabled;
        document.getElementById('btn-audio').textContent = `AUDIO: ${audio.enabled ? 'ON' : 'OFF'}`;
    });

    // Diagnostic Hint Button
    document.getElementById('btn-hint').addEventListener('click', () => {
        audio.playClick();
        if (engine.hintsUsed >= 3) {
            logMessage('[DIAGNOSTIC] Maximum hint quota reached for node.', 'text-red');
            return;
        }
        engine.hintsUsed++;
        engine.score = Math.max(0, engine.score - 150);
        logMessage(`[HINT] ${engine.activePuzzle.hint}`, 'text-yellow');
        updateHUD();
    });

    // Abort Run Button
    document.getElementById('btn-abort').addEventListener('click', () => {
        audio.playAlarm();
        engine.stopTimer();
        logMessage('[SYSTEM] Connection aborted by runner.', 'text-red');
        showStartModal();
    });

    // Leaderboard Buttons
    document.getElementById('btn-show-scores').addEventListener('click', showLeaderboardModal);
    document.getElementById('btn-close-scores').addEventListener('click', showStartModal);

    // Restart Buttons
    document.getElementById('btn-vic-restart').addEventListener('click', showStartModal);
    document.getElementById('btn-def-restart').addEventListener('click', showStartModal);
});

// HUD Updater
function updateHUD() {
    document.getElementById('hud-runner').textContent = engine.runnerHandle;
    document.getElementById('hud-integrity').textContent = `${Math.max(0, engine.integrity)} HP`;
    document.getElementById('integrity-bar').style.width = `${Math.max(0, engine.integrity)}%`;

    document.getElementById('hud-trace').textContent = `${Math.min(100, engine.tracePercent)}%`;
    document.getElementById('trace-bar').style.width = `${Math.min(100, engine.tracePercent)}%`;

    document.getElementById('hud-timer').textContent = `${engine.timerLeft.toFixed(1)}s`;
    document.getElementById('hud-score').textContent = engine.score;

    // Update Security Nodes Navigation Bar
    for (let i = 0; i < 5; i++) {
        const nodeEl = document.getElementById(`node-step-${i}`);
        if (!nodeEl) continue;
        nodeEl.classList.remove('active', 'completed');
        if (i < engine.currentLayer) {
            nodeEl.classList.add('completed');
        } else if (i === engine.currentLayer) {
            nodeEl.classList.add('active');
        }
    }
}

// Stage Renderer for Mini-Game Viewports
function renderStage() {
    const p = engine.activePuzzle;
    document.getElementById('puzzle-title').textContent = p.title;
    document.getElementById('puzzle-sub').textContent = p.sub;

    const area = document.getElementById('puzzle-interactive-area');
    area.innerHTML = '';

    if (p.type === 'LOGIC') {
        renderLogicStage(area, p);
    } else if (p.type === 'CRYPTO') {
        renderCryptoStage(area, p);
    } else if (p.type === 'ANOMALY') {
        renderAnomalyStage(area, p);
    } else if (p.type === 'SEQUENCE') {
        renderSequenceStage(area, p);
    } else if (p.type === 'KEYPAD') {
        renderKeypadStage(area, p);
    }
}

// 1. Logic Wiring Viewport
function renderLogicStage(container, puzzle) {
    const wrap = document.createElement('div');
    wrap.className = 'wiring-container';

    const exprBox = document.createElement('div');
    exprBox.className = 'gate-expr-box';
    exprBox.textContent = `CIRCUIT EXPR: ${puzzle.expr}`;
    wrap.appendChild(exprBox);

    const switchesRow = document.createElement('div');
    switchesRow.className = 'signal-switches';

    const currentSwitches = { ...puzzle.switches };

    Object.keys(currentSwitches).forEach(key => {
        const card = document.createElement('div');
        card.className = `switch-card ${currentSwitches[key] ? 'on' : ''}`;
        card.innerHTML = `<div>SIGNAL ${key}</div><div class="switch-val">${currentSwitches[key] ? 'HIGH (1)' : 'LOW (0)'}</div>`;
        card.onclick = () => {
            audio.playClick();
            currentSwitches[key] = !currentSwitches[key];
            card.className = `switch-card ${currentSwitches[key] ? 'on' : ''}`;
            card.querySelector('.switch-val').textContent = currentSwitches[key] ? 'HIGH (1)' : 'LOW (0)';
        };
        switchesRow.appendChild(card);
    });

    wrap.appendChild(switchesRow);
    container.appendChild(wrap);

    // Submit button event
    document.getElementById('btn-submit').onclick = () => {
        engine.submitPayload(currentSwitches);
    };
}

// 2. Crypto Cipher Viewport
function renderCryptoStage(container, puzzle) {
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'cyber-input';
    input.placeholder = 'ENTER DECRYPTED KEYWORD...';
    input.style.width = '320px';
    input.style.textAlign = 'center';

    container.appendChild(input);

    document.getElementById('btn-submit').onclick = () => {
        engine.submitPayload(input.value);
    };
}

// 3. Anomaly Grid Viewport
function renderAnomalyStage(container, puzzle) {
    const grid = document.createElement('div');
    grid.className = 'anomaly-grid';
    grid.style.gridTemplateColumns = `repeat(${puzzle.grid[0].length}, 1fr)`;

    puzzle.grid.forEach((row, r) => {
        row.forEach((sym, c) => {
            const cell = document.createElement('div');
            cell.className = 'grid-cell';
            cell.textContent = sym;
            cell.onclick = () => {
                audio.playClick();
                engine.submitPayload(`${r},${c}`);
            };
            grid.appendChild(cell);
        });
    });

    container.appendChild(grid);
    document.getElementById('btn-submit').onclick = () => {};
}

// 4. Sequence Viewport
function renderSequenceStage(container, puzzle) {
    const input = document.createElement('input');
    input.type = 'number';
    input.className = 'cyber-input';
    input.placeholder = 'ENTER NEXT SEQUENCE VALUE...';
    input.style.width = '300px';
    input.style.textAlign = 'center';

    container.appendChild(input);

    document.getElementById('btn-submit').onclick = () => {
        engine.submitPayload(input.value);
    };
}

// 5. Keypad Viewport
function renderKeypadStage(container, puzzle) {
    let currentInput = '';

    const display = document.createElement('div');
    display.className = 'keypad-display';
    display.textContent = '____';
    container.appendChild(display);

    const grid = document.createElement('div');
    grid.className = 'keypad-grid';

    const keys = ['7','8','9','A', '4','5','6','B', '1','2','3','C', '0','CLR','D','E'];
    keys.forEach(k => {
        const btn = document.createElement('button');
        btn.className = 'keypad-btn';
        btn.textContent = k;
        btn.onclick = () => {
            audio.playClick();
            if (k === 'CLR') {
                currentInput = '';
            } else if (currentInput.length < 4) {
                currentInput += k;
            }
            display.textContent = (currentInput + '____').substring(0, 4);
        };
        grid.appendChild(btn);
    });

    container.appendChild(grid);

    // History reel
    const historyDiv = document.createElement('div');
    historyDiv.className = 'guess-history';
    puzzle.history.forEach(h => {
        const row = document.createElement('div');
        row.className = 'guess-row';
        row.innerHTML = `<span>GUESS: ${h.guess}</span> <span class="text-green">EXACT: ${h.exact}</span> <span class="text-yellow">PARTIAL: ${h.partial}</span>`;
        historyDiv.appendChild(row);
    });
    container.appendChild(historyDiv);

    document.getElementById('btn-submit').onclick = () => {
        engine.submitPayload(currentInput);
    };
}

// Log Messages to Terminal Output Feed
function logMessage(text, colorClass = '') {
    const feed = document.getElementById('feed-messages');
    const line = document.createElement('div');
    line.className = `log-line ${colorClass}`;
    line.textContent = text;
    feed.appendChild(line);
    feed.scrollTop = feed.scrollHeight;
}

// Modal Handlers
function hideModal() {
    document.getElementById('modal-overlay').classList.add('hidden');
}

function showStartModal() {
    const overlay = document.getElementById('modal-overlay');
    overlay.classList.remove('hidden');
    
    document.getElementById('start-modal').classList.remove('hidden');
    document.getElementById('scores-modal').classList.add('hidden');
    document.getElementById('victory-modal').classList.add('hidden');
    document.getElementById('defeat-modal').classList.add('hidden');
}

function showVictoryModal() {
    const totalTime = ((Date.now() - engine.startTime) / 1000).toFixed(1);
    document.getElementById('vic-score').textContent = engine.score;
    document.getElementById('vic-time').textContent = `${totalTime}s`;

    saveScore(engine.runnerHandle, engine.score, engine.totalLayers, engine.difficulty);

    const overlay = document.getElementById('modal-overlay');
    overlay.classList.remove('hidden');
    document.getElementById('victory-modal').classList.remove('hidden');
}

function showDefeatModal() {
    document.getElementById('def-nodes').textContent = engine.currentLayer;
    document.getElementById('def-score').textContent = engine.score;

    const overlay = document.getElementById('modal-overlay');
    overlay.classList.remove('hidden');
    document.getElementById('defeat-modal').classList.remove('hidden');
}

function showLeaderboardModal() {
    const tbody = document.getElementById('scores-tbody');
    tbody.innerHTML = '';
    const scores = getScores();

    scores.forEach((s, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>#${idx + 1}</td><td>${s.handle}</td><td class="text-yellow">${s.score}</td><td>${s.layers}</td><td>${s.difficulty}</td>`;
        tbody.appendChild(tr);
    });

    document.getElementById('start-modal').classList.add('hidden');
    document.getElementById('scores-modal').classList.remove('hidden');
}

// High Scores LocalStorage Utility
function getScores() {
    try {
        return JSON.parse(localStorage.getItem('neon_breach_scores')) || [
            { handle: 'NEO_GHOST', score: 9500, layers: 5, difficulty: 'BLACK_ICE' },
            { handle: 'CYBER_VIXEN', score: 7800, layers: 5, difficulty: 'CYBERPUNK' },
            { handle: 'NULL_POINTER', score: 6200, layers: 4, difficulty: 'CYBERPUNK' }
        ];
    } catch (e) {
        return [];
    }
}

function saveScore(handle, score, layers, difficulty) {
    const scores = getScores();
    scores.push({ handle, score, layers, difficulty });
    scores.sort((a, b) => b.score - a.score);
    try {
        localStorage.setItem('neon_breach_scores', JSON.stringify(scores.slice(0, 10)));
    } catch (e) {}
}

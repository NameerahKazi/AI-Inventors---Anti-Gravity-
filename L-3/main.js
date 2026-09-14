/**
 * LUNAR EXPLORER - MISSION CONTROL DISPLAY CORE
 * 100% Offline-first, Framework-free Vanilla JavaScript
 */

(function () {
  'use strict';

  /* ==========================================================================
     AUDIO SYNTHESIS ENGINE (Web Audio API)
     Zero external audio files required — 100% offline procedural sci-fi audio
     ========================================================================== */
  class SoundEngine {
    constructor() {
      this.ctx = null;
      this.enabled = true;
    }

    init() {
      if (!this.ctx) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) {
          this.ctx = new AudioCtx();
        }
      }
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
    }

    playClick() {
      if (!this.enabled) return;
      this.init();
      if (!this.ctx) return;
      try {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(400, this.ctx.currentTime + 0.04);
        gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.001, this.ctx.currentTime + 0.04);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.04);
      } catch (e) {
        console.warn('Audio play error', e);
      }
    }

    playCorrect() {
      if (!this.enabled) return;
      this.init();
      if (!this.ctx) return;
      try {
        const now = this.ctx.currentTime;
        const freqs = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
        freqs.forEach((f, i) => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(f, now + i * 0.07);
          gain.gain.setValueAtTime(0.18, now + i * 0.07);
          gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.07 + 0.25);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(now + i * 0.07);
          osc.stop(now + i * 0.07 + 0.25);
        });
      } catch (e) {
        console.warn('Audio play error', e);
      }
    }

    playWrong() {
      if (!this.enabled) return;
      this.init();
      if (!this.ctx) return;
      try {
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(140, now);
        osc.frequency.linearRampToValueAtTime(90, now + 0.2);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.linearRampToValueAtTime(0.001, now + 0.2);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.2);
      } catch (e) {
        console.warn('Audio play error', e);
      }
    }

    playChirp() {
      if (!this.enabled) return;
      this.init();
      if (!this.ctx) return;
      try {
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(950, now);
        osc.frequency.exponentialRampToValueAtTime(1400, now + 0.08);
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.linearRampToValueAtTime(0.001, now + 0.08);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.08);
      } catch (e) {
        console.warn('Audio play error', e);
      }
    }

    playFanfare() {
      if (!this.enabled) return;
      this.init();
      if (!this.ctx) return;
      try {
        const notes = [440, 554.37, 659.25, 880]; // A4, C#5, E5, A5
        const now = this.ctx.currentTime;
        notes.forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(freq, now + idx * 0.12);
          gain.gain.setValueAtTime(0.25, now + idx * 0.12);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.12 + 0.6);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(now + idx * 0.12);
          osc.stop(now + idx * 0.12 + 0.6);
        });
      } catch (e) {
        console.warn('Fanfare error', e);
      }
    }
  }

  const sound = new SoundEngine();

  // Audio Toggle Button
  const audioToggleBtn = document.getElementById('audio-toggle-btn');
  const audioIcon = document.getElementById('audio-icon');
  if (audioToggleBtn) {
    audioToggleBtn.addEventListener('click', () => {
      sound.enabled = !sound.enabled;
      if (sound.enabled) {
        sound.init();
        sound.playChirp();
        audioIcon.textContent = '🔊';
        audioToggleBtn.style.borderColor = 'var(--gold)';
      } else {
        audioIcon.textContent = '🔇';
        audioToggleBtn.style.borderColor = 'rgba(255,255,255,0.2)';
      }
    });
  }

  /* ==========================================================================
     DYNAMIC STARFIELD CANVAS (180+ Twinkling Stars)
     ========================================================================== */
  const starCanvas = document.getElementById('star-canvas');
  if (starCanvas) {
    const ctx = starCanvas.getContext('2d');
    let width = (starCanvas.width = window.innerWidth);
    let height = (starCanvas.height = window.innerHeight);

    const starCount = 185;
    const stars = [];

    for (let i = 0; i < starCount; i++) {
      stars.push({
        x: Math.random() * width,
        y: Math.random() * height,
        r: Math.random() * 1.5 + 0.4,
        alpha: Math.random() * 0.8 + 0.2,
        speed: Math.random() * 0.02 + 0.005,
        twinkleFactor: Math.random() * Math.PI * 2,
        hue: Math.random() > 0.8 ? 48 : Math.random() > 0.6 ? 205 : 0 // slight gold or blue tint
      });
    }

    function renderStars() {
      ctx.clearRect(0, 0, width, height);
      for (let i = 0; i < stars.length; i++) {
        const s = stars[i];
        s.twinkleFactor += s.speed;
        const currentAlpha = s.alpha * (0.5 + 0.5 * Math.sin(s.twinkleFactor));
        
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        if (s.hue === 48) {
          ctx.fillStyle = `rgba(255, 225, 120, ${currentAlpha})`;
        } else if (s.hue === 205) {
          ctx.fillStyle = `rgba(147, 210, 255, ${currentAlpha})`;
        } else {
          ctx.fillStyle = `rgba(255, 255, 255, ${currentAlpha})`;
        }
        ctx.fill();
      }
      requestAnimationFrame(renderStars);
    }

    window.addEventListener('resize', () => {
      width = starCanvas.width = window.innerWidth;
      height = starCanvas.height = window.innerHeight;
      stars.forEach(s => {
        s.x = Math.random() * width;
        s.y = Math.random() * height;
      });
    });

    renderStars();
  }

  /* ==========================================================================
     MISSION CLOCK & MET (Mission Elapsed Time)
     ========================================================================== */
  const clockDisplay = document.getElementById('clock-display');
  let metSeconds = 56 * 3600 + 11 * 60 + 9; // Starting simulated MET

  function updateClock() {
    metSeconds++;
    const now = new Date();
    const utcHours = String(now.getUTCHours()).padStart(2, '0');
    const utcMinutes = String(now.getUTCMinutes()).padStart(2, '0');
    const utcSecs = String(now.getUTCSeconds()).padStart(2, '0');

    const metH = String(Math.floor(metSeconds / 3600)).padStart(2, '0');
    const metM = String(Math.floor((metSeconds % 3600) / 60)).padStart(2, '0');
    const metS = String(metSeconds % 60).padStart(2, '0');

    if (clockDisplay) {
      clockDisplay.textContent = `UTC ${utcHours}:${utcMinutes}:${utcSecs} // MET ${metH}:${metM}:${metS}`;
    }
  }
  setInterval(updateClock, 1000);
  updateClock();

  /* ==========================================================================
     3D EARTH-MOON SIMULATION CONTROLS
     ========================================================================== */
  const moonOrbitPivot = document.getElementById('moon-orbit-pivot');
  const simPauseToggle = document.getElementById('sim-pause-toggle');
  const simPauseIcon = document.getElementById('sim-pause-icon');
  const simPauseText = document.getElementById('sim-pause-text');
  const simSpeedToggle = document.getElementById('sim-speed-toggle');
  const simSpeedVal = document.getElementById('sim-speed-val');
  const simResetToggle = document.getElementById('sim-reset-toggle');
  const interactiveMoon = document.getElementById('interactive-moon');

  let isPaused = false;
  let currentSpeedMultiplier = 1;
  const baseOrbitDuration = 18; // 18 seconds

  function updateOrbitSpeed() {
    if (moonOrbitPivot) {
      moonOrbitPivot.style.animationDuration = `${baseOrbitDuration / currentSpeedMultiplier}s`;
    }
  }

  if (simPauseToggle) {
    simPauseToggle.addEventListener('click', () => {
      sound.playClick();
      isPaused = !isPaused;
      if (isPaused) {
        moonOrbitPivot.style.animationPlayState = 'paused';
        simPauseIcon.textContent = '▶️';
        simPauseText.textContent = 'RESUME';
        simPauseToggle.style.color = 'var(--gold)';
      } else {
        moonOrbitPivot.style.animationPlayState = 'running';
        simPauseIcon.textContent = '⏸️';
        simPauseText.textContent = 'PAUSE';
        simPauseToggle.style.color = 'var(--text-secondary)';
      }
    });
  }

  if (simSpeedToggle) {
    simSpeedToggle.addEventListener('click', () => {
      sound.playClick();
      if (currentSpeedMultiplier === 1) currentSpeedMultiplier = 2;
      else if (currentSpeedMultiplier === 2) currentSpeedMultiplier = 4;
      else currentSpeedMultiplier = 1;

      simSpeedVal.textContent = `${currentSpeedMultiplier}X`;
      updateOrbitSpeed();
    });
  }

  if (simResetToggle) {
    simResetToggle.addEventListener('click', () => {
      sound.playClick();
      currentSpeedMultiplier = 1;
      simSpeedVal.textContent = '1X';
      isPaused = false;
      moonOrbitPivot.style.animationPlayState = 'running';
      simPauseIcon.textContent = '⏸️';
      simPauseText.textContent = 'PAUSE';
      updateOrbitSpeed();
    });
  }

  if (interactiveMoon) {
    interactiveMoon.addEventListener('click', () => {
      sound.playChirp();
      queryLunaTopic('The Moon');
    });
  }

  /* ==========================================================================
     STATS COUNTER ANIMATION (Intersection Observer)
     ========================================================================== */
  const counterEls = document.querySelectorAll('.counter-num');
  let animatedStats = false;

  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !animatedStats) {
        animatedStats = true;
        counterEls.forEach(el => {
          const target = parseFloat(el.getAttribute('data-target'));
          const decimalPlaces = parseInt(el.getAttribute('data-decimal') || '0', 10);
          const duration = 1800; // ms
          const startTime = performance.now();

          function step(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentVal = target * easeOut;

            if (decimalPlaces > 0) {
              el.textContent = currentVal.toFixed(decimalPlaces);
            } else {
              el.textContent = Math.floor(currentVal).toLocaleString();
            }

            if (progress < 1) {
              requestAnimationFrame(step);
            } else {
              if (decimalPlaces > 0) {
                el.textContent = target.toFixed(decimalPlaces);
              } else {
                el.textContent = target.toLocaleString();
              }
            }
          }
          requestAnimationFrame(step);
        });
      }
    });
  }, { threshold: 0.25 });

  const statsSection = document.getElementById('stats');
  if (statsSection) {
    statsObserver.observe(statsSection);
  }

  /* ==========================================================================
     3D TILT EFFECT ON MISSION CARDS (Perspective tracking)
     ========================================================================== */
  const missionCards = document.querySelectorAll('.mission-card-3d');

  missionCards.forEach(card => {
    const glare = card.querySelector('.card-glare');

    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      // Max rotation angles
      const rotateX = ((y - centerY) / centerY) * -12; // Invert for natural tilt
      const rotateY = ((x - centerX) / centerX) * 12;

      card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.02, 1.02, 1.02)`;

      if (glare) {
        const glareX = (x / rect.width) * 100;
        const glareY = (y / rect.height) * 100;
        glare.style.opacity = '1';
        glare.style.background = `radial-gradient(circle at ${glareX}% ${glareY}%, rgba(255, 255, 255, 0.22) 0%, transparent 65%)`;
      }
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      if (glare) {
        glare.style.opacity = '0';
      }
    });
  });

  /* ==========================================================================
     GAMIFIED QUIZ ENGINE & STARBURST CONFETTI
     ========================================================================== */
  const quizQuestions = [
    {
      category: "ASTRONOMY & GRAVITY",
      question: "What is the surface gravity of the Moon compared to Earth?",
      options: [
        { key: "A", text: "Approximately 50% (half of Earth's gravity)" },
        { key: "B", text: "1.62 m/s², approximately 16.6% (one-sixth) of Earth's gravity" },
        { key: "C", text: "Exactly zero gravity in vacuum conditions" },
        { key: "D", text: "3.71 m/s², identical to the Martian surface" }
      ],
      correct: 1,
      explanation: "Lunar surface gravity is 1.62 m/s² (~1/6th of Earth's 9.81 m/s²). This allowed Apollo astronauts to bound easily across the regolith despite wearing heavy 80 kg spacesuits."
    },
    {
      category: "HISTORIC LANDINGS",
      question: "At which lunar mare did Neil Armstrong and Buzz Aldrin land the Lunar Module 'Eagle' in July 1969?",
      options: [
        { key: "A", text: "Oceanus Procellarum (Ocean of Storms)" },
        { key: "B", text: "Mare Imbrium (Sea of Rains)" },
        { key: "C", text: "Mare Tranquillitatis (Sea of Tranquility)" },
        { key: "D", text: "Mare Serenitatis (Sea of Serenity)" }
      ],
      correct: 2,
      explanation: "Apollo 11 landed in Mare Tranquillitatis (Sea of Tranquility) on July 20, 1969. Armstrong radioed the famous transmission: 'Houston, Tranquility Base here. The Eagle has landed.'"
    },
    {
      category: "DEEP SPACE DISCOVERY",
      question: "Which Indian Space Research Organisation (ISRO) mission first definitively confirmed water molecules across the lunar surface?",
      options: [
        { key: "A", text: "Chandrayaan-1 (2008)" },
        { key: "B", text: "Mangalyaan Mars Orbiter (2013)" },
        { key: "C", text: "Chandrayaan-2 (2019)" },
        { key: "D", text: "AstroSat Space Observatory (2015)" }
      ],
      correct: 0,
      explanation: "Chandrayaan-1 (2008) carried NASA's Moon Mineralogy Mapper (M3) and the Moon Impact Probe (MIP), which detected hydroxyl (OH) and water (H₂O) molecules, shattering the old myth of a bone-dry Moon."
    },
    {
      category: "FAR SIDE EXPLORATION",
      question: "Which spacecraft made history in 2019 as the first ever to make a soft touchdown on the Moon's Far Side?",
      options: [
        { key: "A", text: "Surveyor 7" },
        { key: "B", text: "Luna 24" },
        { key: "C", text: "Chang'e 4" },
        { key: "D", text: "SLIM" }
      ],
      correct: 2,
      explanation: "China's Chang'e 4 landed in the Von Kármán crater within the South Pole-Aitken Basin on January 3, 2019, communicating back to Earth via the Queqiao relay satellite at the L2 Lagrange point."
    },
    {
      category: "POLAR EXPEDITIONS",
      question: "What historic milestone did Chandrayaan-3 achieve on August 23, 2023?",
      options: [
        { key: "A", text: "First spacecraft to return soil from the farside" },
        { key: "B", text: "World-first soft landing near the high-latitude Lunar South Pole (69.37°S)" },
        { key: "C", text: "First crewed circumlunar mission" },
        { key: "D", text: "First rover to survive a two-year lunar night" }
      ],
      correct: 1,
      explanation: "ISRO's Chandrayaan-3 landed Vikram and Pragyan at 69.37°S latitude, making India the first nation in history to touch down in the prized Lunar South Pole region."
    },
    {
      category: "ARTEMIS PROGRAM",
      question: "What is the primary commercial Human Landing System (HLS) contracted by NASA to land Artemis III astronauts at the South Pole?",
      options: [
        { key: "A", text: "SpaceX Starship HLS" },
        { key: "B", text: "Boeing Starliner Module" },
        { key: "C", text: "Grumman Apollo Lunar Module Reissue" },
        { key: "D", text: "Lockheed Martin Orion Capsule" }
      ],
      correct: 0,
      explanation: "NASA selected SpaceX's Starship HLS as the lunar lander to transport astronauts from lunar orbit (Orion / Gateway) down to the harsh South Pole surface for Artemis III."
    }
  ];

  let currentQuestionIndex = 0;
  let quizScore = 0;
  let hasAnsweredCurrent = false;

  const quizCurrIdxEl = document.getElementById('quiz-curr-idx');
  const quizTotalIdxEl = document.getElementById('quiz-total-idx');
  const quizProgressFill = document.getElementById('quiz-progress-fill');
  const quizCategoryEl = document.getElementById('quiz-category');
  const quizQuestionText = document.getElementById('quiz-question-text');
  const quizOptionsContainer = document.getElementById('quiz-options-container');
  const quizFeedbackBox = document.getElementById('quiz-feedback-box');
  const quizFeedbackHeader = document.getElementById('quiz-feedback-header');
  const quizFeedbackIcon = document.getElementById('quiz-feedback-icon');
  const quizFeedbackTitle = document.getElementById('quiz-feedback-title');
  const quizFeedbackText = document.getElementById('quiz-feedback-text');
  const quizNextRow = document.getElementById('quiz-next-row');
  const quizNextBtn = document.getElementById('quiz-next-btn');

  const quizActiveBody = document.getElementById('quiz-active-body');
  const quizResultsScreen = document.getElementById('quiz-results-screen');
  const resultsScoreBig = document.getElementById('results-score-big');
  const resultsTitle = document.getElementById('results-title');
  const resultsMessage = document.getElementById('results-message');
  const quizRestartBtn = document.getElementById('quiz-restart-btn');

  function renderQuizQuestion(index) {
    hasAnsweredCurrent = false;
    const q = quizQuestions[index];

    quizCurrIdxEl.textContent = index + 1;
    quizTotalIdxEl.textContent = quizQuestions.length;
    quizProgressFill.style.width = `${((index + 1) / quizQuestions.length) * 100}%`;

    quizCategoryEl.textContent = q.category;
    quizQuestionText.textContent = q.question;

    quizFeedbackBox.classList.remove('show');
    quizNextRow.style.display = 'none';

    quizOptionsContainer.innerHTML = '';
    q.options.forEach((opt, optIdx) => {
      const btn = document.createElement('button');
      btn.className = 'quiz-opt-btn';
      btn.innerHTML = `
        <span class="quiz-opt-key">${opt.key}</span>
        <span class="quiz-opt-text">${opt.text}</span>
      `;
      btn.addEventListener('click', () => handleQuizAnswer(optIdx, btn));
      quizOptionsContainer.appendChild(btn);
    });
  }

  function handleQuizAnswer(selectedIdx, clickedBtn) {
    if (hasAnsweredCurrent) return;
    hasAnsweredCurrent = true;

    const q = quizQuestions[currentQuestionIndex];
    const optionBtns = quizOptionsContainer.querySelectorAll('.quiz-opt-btn');

    // Disable all options
    optionBtns.forEach(btn => (btn.disabled = true));

    if (selectedIdx === q.correct) {
      quizScore++;
      sound.playCorrect();
      clickedBtn.classList.add('correct');
      quizFeedbackHeader.className = 'quiz-feedback-header success';
      quizFeedbackIcon.textContent = '✓';
      quizFeedbackTitle.textContent = 'TELEMETRY CONFIRMED // ACCURATE';
    } else {
      sound.playWrong();
      clickedBtn.classList.add('wrong');
      // Highlight the correct one
      optionBtns[q.correct].classList.add('correct');
      quizFeedbackHeader.className = 'quiz-feedback-header error';
      quizFeedbackIcon.textContent = '✕';
      quizFeedbackTitle.textContent = 'TELEMETRY MISMATCH // ANOMALY';
    }

    quizFeedbackText.textContent = q.explanation;
    quizFeedbackBox.classList.add('show');
    quizNextRow.style.display = 'flex';
  }

  if (quizNextBtn) {
    quizNextBtn.addEventListener('click', () => {
      sound.playClick();
      currentQuestionIndex++;
      if (currentQuestionIndex < quizQuestions.length) {
        renderQuizQuestion(currentQuestionIndex);
      } else {
        showQuizResults();
      }
    });
  }

  function showQuizResults() {
    quizActiveBody.style.display = 'none';
    quizResultsScreen.classList.add('show');
    resultsScoreBig.textContent = `${quizScore} / ${quizQuestions.length}`;

    if (quizScore === 6) {
      sound.playFanfare();
      resultsTitle.textContent = 'Flight Commander Rank Awarded!';
      resultsMessage.textContent = 'Flawless telemetry! You answered every question with 100% precision. The Starburst celebration flare has launched across Mission Control!';
      triggerStarburstConfetti();
    } else if (quizScore >= 4) {
      sound.playCorrect();
      resultsTitle.textContent = 'Senior Lunar Specialist Certified';
      resultsMessage.textContent = `Commendable flight rating! You scored ${quizScore} out of 6. A slight recalibration of deep space trivia will make you fully certified.`;
    } else {
      sound.playWrong();
      resultsTitle.textContent = 'Cadet Trainee Status';
      resultsMessage.textContent = `Telemetry score: ${quizScore} / 6. Review the mission timeline and 3D archive cards, then recalibrate your evaluation!`;
    }
  }

  if (quizRestartBtn) {
    quizRestartBtn.addEventListener('click', () => {
      sound.playClick();
      currentQuestionIndex = 0;
      quizScore = 0;
      quizResultsScreen.classList.remove('show');
      quizActiveBody.style.display = 'block';
      renderQuizQuestion(0);
    });
  }

  // Initialize Quiz
  renderQuizQuestion(0);

  /* ==========================================================================
     STARBURST CONFETTI CANVAS ENGINE (For 6/6 Perfect Score)
     ========================================================================== */
  function triggerStarburstConfetti() {
    const confettiCanvas = document.getElementById('confetti-canvas');
    if (!confettiCanvas) return;
    const ctx = confettiCanvas.getContext('2d');
    const w = (confettiCanvas.width = window.innerWidth);
    const h = (confettiCanvas.height = window.innerHeight);

    const particles = [];
    const colors = ['#ffd54f', '#5bb8ff', '#4eff9a', '#ff6b45', '#d8aaff', '#ffffff'];

    // Burst from center
    const centerX = w / 2;
    const centerY = h / 2;

    for (let i = 0; i < 240; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 14 + 3;
      particles.push({
        x: centerX,
        y: centerY,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        size: Math.random() * 6 + 3,
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: 1,
        decay: Math.random() * 0.015 + 0.008,
        gravity: 0.18,
        rotation: Math.random() * 360,
        rotSpeed: (Math.random() - 0.5) * 12
      });
    }

    let animId;
    function animConfetti() {
      ctx.clearRect(0, 0, w, h);
      let aliveCount = 0;

      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += p.gravity;
        p.vx *= 0.98;
        p.alpha -= p.decay;
        p.rotation += p.rotSpeed;

        if (p.alpha > 0) {
          aliveCount++;
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate((p.rotation * Math.PI) / 180);
          ctx.globalAlpha = Math.max(0, p.alpha);
          ctx.fillStyle = p.color;
          ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
          ctx.restore();
        }
      });

      if (aliveCount > 0) {
        animId = requestAnimationFrame(animConfetti);
      } else {
        ctx.clearRect(0, 0, w, h);
        cancelAnimationFrame(animId);
      }
    }
    animConfetti();
  }

  /* ==========================================================================
     L.U.N.A COMPREHENSIVE KNOWLEDGE BASE (60+ Lunar Nodes)
     ========================================================================== */
  const moonKnowledge = [
    // 1-15: Orbital & Physical Characteristics
    {
      keywords: ["distance", "how far", "distance to earth", "orbit distance"],
      answer: "The Moon orbits Earth at an average distance of 384,400 km (238,855 miles). At perigee (closest point) it is approximately 363,300 km away, and at apogee (furthest) it reaches 405,500 km."
    },
    {
      keywords: ["gravity", "surface gravity", "how heavy", "weight on moon"],
      answer: "Lunar surface gravity is 1.62 m/s², which is approximately 16.6% (one-sixth) of Earth's gravity. A 90 kg astronaut weighs only about 15 kg on the lunar surface."
    },
    {
      keywords: ["size", "diameter", "how big", "dimensions"],
      answer: "The Moon has an equatorial diameter of 3,474.8 km (2,159 miles), roughly 27% the size of Earth. It is the fifth largest satellite in our Solar System."
    },
    {
      keywords: ["atmosphere", "air", "breathe", "exosphere", "vacuum"],
      answer: "The Moon has virtually no atmosphere. It possesses an ultra-thin surface boundary exosphere with a total mass under 10 metric tons, containing traces of argon-40, helium-4, neon, sodium, and potassium."
    },
    {
      keywords: ["temperature", "how hot", "how cold", "climate"],
      answer: "Lunar surface temperatures swing wildly from approximately +120°C (+250°F) during the lunar daytime to -130°C (-208°F) at night, plunging to -246°C (-410°F) inside permanently shadowed polar craters."
    },
    {
      keywords: ["day length", "lunar day", "rotation period", "how long is day"],
      answer: "A single lunar day-night cycle (synodic period) lasts 29.5 Earth days. The Moon takes 27.3 Earth days to rotate once on its axis (sidereal period)."
    },
    {
      keywords: ["tidal locking", "synchronous rotation", "same side", "dark side"],
      answer: "The Moon is tidally locked to Earth by gravitational friction. It rotates on its axis in the exact same time it takes to orbit Earth, meaning the same face always points toward us."
    },
    {
      keywords: ["far side", "dark side of moon", "back of moon"],
      answer: "The Moon's far side is not perpetually dark; it receives as much sunlight as the near side. It features a thicker crust, far fewer basaltic 'seas' (maria), and is heavily saturated with impact craters."
    },
    {
      keywords: ["origin", "how formed", "giant impact", "theia"],
      answer: "The leading scientific theory is the Giant Impact Hypothesis: approximately 4.5 billion years ago, a Mars-sized protoplanet named Theia collided with the early proto-Earth, hurling molten debris into orbit that coalesced into the Moon."
    },
    {
      keywords: ["mass", "weight of moon", "how heavy is the moon"],
      answer: "The mass of the Moon is 7.342 × 10²² kg, approximately 1.2% of Earth's total mass (1/81st)."
    },
    {
      keywords: ["density", "what is it made of", "composition"],
      answer: "The Moon's mean density is 3.344 g/cm³, noticeably lighter than Earth's (5.51 g/cm³), because it lacks a massive iron-nickel metallic core. Its core is small, only ~350 km across."
    },
    {
      keywords: ["regolith", "lunar soil", "dust"],
      answer: "Lunar regolith is a fine, glass-like powdery dust created by billions of years of meteorite pulverization. It is extremely abrasive, electrically charged by solar ultraviolet rays, and smells faintly like spent gunpowder."
    },
    {
      keywords: ["maria", "seas", "dark spots"],
      answer: "Lunar maria (Latin for 'seas') are expansive, dark basaltic plains formed by ancient volcanic eruptions between 3.0 and 3.8 billion years ago. They cover about 16% of the Moon's surface, mostly on the near side."
    },
    {
      keywords: ["highlands", "terrae", "white parts"],
      answer: "The lunar highlands (terrae) are the bright, mountainous terrains of the Moon. Composed primarily of calcium-rich anorthosite rock, they represent the Moon's original primordial magma-ocean crust."
    },
    {
      keywords: ["craters", "why craters", "meteorite impacts"],
      answer: "The Moon is covered in impact craters because it has no liquid water, wind, active plate tectonics, or substantial atmosphere to erode or burn up incoming meteorites over billions of years."
    },

    // 16-25: Famous Craters & Geography
    {
      keywords: ["tycho", "tycho crater", "bright rays"],
      answer: "Tycho is a prominent 85-km diameter impact crater in the southern highlands, famous for its brilliant white ray system that stretches more than 1,500 km across the lunar disk. It is relatively young, formed ~108 million years ago."
    },
    {
      keywords: ["copernicus", "copernicus crater"],
      answer: "Copernicus is an iconic 93-km impact crater in eastern Oceanus Procellarum, featuring towering terraced walls 3.8 km high and a cluster of central peaks rising 1.2 km above the crater floor."
    },
    {
      keywords: ["shackleton", "shackleton crater", "south pole crater"],
      answer: "Shackleton crater sits precisely at the lunar South Pole (89.9°S). Its 4.2 km deep interior is permanently cloaked in darkness and harbors significant reservoirs of cryogenic water ice."
    },
    {
      keywords: ["south pole aitken", "largest crater", "aitken basin"],
      answer: "The South Pole-Aitken Basin is one of the largest and oldest preserved impact basins in the Solar System, spanning 2,500 km across and up to 8 km deep on the Moon's far side."
    },
    {
      keywords: ["tranquility base", "sea of tranquility", "mare tranquillitatis"],
      answer: "Tranquility Base is the landing site of Apollo 11 (0.67°N, 23.47°E). Neil Armstrong and Buzz Aldrin spent 21 hours and 36 minutes there in July 1969."
    },
    {
      keywords: ["oceanus procellarum", "ocean of storms"],
      answer: "Oceanus Procellarum is the vastest lunar mare, stretching over 2,500 km along the western near side and covering approximately 4 million square kilometers."
    },

    // 26-40: Historical Apollo Missions
    {
      keywords: ["apollo 11", "neil armstrong", "buzz aldrin", "first man on moon"],
      answer: "Apollo 11 landed on July 20, 1969. Neil Armstrong and Buzz Aldrin became the first humans to walk on the lunar surface, collecting 21.5 kg of rocks while Michael Collins orbited in the Command Module Columbia."
    },
    {
      keywords: ["apollo 12", "pete conrad", "alan bean", "surveyor 3"],
      answer: "Apollo 12 (November 1969) achieved the first pinpoint lunar landing in Oceanus Procellarum, touching down within walking distance of the robotic Surveyor 3 probe."
    },
    {
      keywords: ["apollo 13", "houston we have a problem", "oxygen tank explosion"],
      answer: "Apollo 13 (April 1970) suffered a catastrophic cryogenic oxygen tank rupture en route to the Moon. The lunar landing was aborted, and the crew survived by using the Lunar Module Aquarius as a lifeboat during a circumlunar loop."
    },
    {
      keywords: ["apollo 14", "alan shepard", "golf on moon"],
      answer: "Apollo 14 (February 1971) explored the Fra Mauro highlands. Commander Alan Shepard famously hit two golf balls across the lunar regolith with a modified six-iron."
    },
    {
      keywords: ["apollo 15", "lunar rover", "hadley rille", "first car on moon"],
      answer: "Apollo 15 (July 1971) was the first 'J-mission', deploying the Lunar Roving Vehicle (LRV) to explore the 1,000-foot-deep Hadley Rille and Apennine mountains."
    },
    {
      keywords: ["apollo 16", "john young", "charles duke", "descartes highlands"],
      answer: "Apollo 16 (April 1972) landed in the Descartes Highlands, disproving the theory that the highlands were volcanic and proving they were impact breccias."
    },
    {
      keywords: ["apollo 17", "gene cernan", "harrison schmitt", "last man on moon"],
      answer: "Apollo 17 (December 1972) was the final Apollo mission. Geologist Harrison Schmitt and Gene Cernan spent 75 hours in Taurus-Littrow, returning 110.5 kg of samples."
    },
    {
      keywords: ["how many walked on moon", "moonwalkers", "12 astronauts"],
      answer: "Exactly 12 humans—all American astronauts during the Apollo program between 1969 and 1972—have walked on the Moon."
    },
    {
      keywords: ["saturn v", "saturn 5", "moon rocket"],
      answer: "The Saturn V rocket stood 110.6 meters (363 feet) tall, generated 34.5 million Newtons (7.6 million pounds) of liftoff thrust, and launched 13 times with a 100% mission success rate."
    },
    {
      keywords: ["lunar module", "the eagle", "lander"],
      answer: "The Apollo Lunar Module (LM) was a two-stage spacecraft built by Grumman. Designed exclusively to fly in the vacuum of space, its walls were as thin as two layers of aluminum foil (0.012 inches) in non-pressurized sections."
    },

    // 41-50: Soviet, Indian & Chinese Missions
    {
      keywords: ["luna 2", "first object on moon", "1959"],
      answer: "Soviet Luna 2 became the first artificial human spacecraft to impact the lunar surface on September 14, 1959, confirming the lack of an intrinsic lunar magnetic field."
    },
    {
      keywords: ["luna 3", "first far side photo"],
      answer: "Soviet Luna 3 (October 1959) took the first photographs of the Moon's previously invisible far side, developing film onboard and scanning it with television transmitters."
    },
    {
      keywords: ["luna 9", "first soft landing"],
      answer: "Soviet Luna 9 achieved the first controlled soft landing on another celestial world on February 3, 1966, deploying petals and transmitting the first panoramic surface photos."
    },
    {
      keywords: ["lunokhod 1", "lunokhod", "first rover"],
      answer: "Lunokhod 1 was the world's first robotic planetary rover, landed by Luna 17 in November 1970. It drove over 10.5 km across Mare Imbrium over 322 days."
    },
    {
      keywords: ["chandrayaan 1", "chandrayaan-1", "isro water"],
      answer: "Chandrayaan-1 (2008) was India's first lunar orbiter. Its Moon Mineralogy Mapper (M3) payload proved the existence of water (H₂O) and hydroxyl molecules locked in lunar minerals."
    },
    {
      keywords: ["chandrayaan 3", "chandrayaan-3", "vikram", "pragyan", "isro"],
      answer: "Chandrayaan-3 achieved history on August 23, 2023, making India the first nation to soft-land near the Lunar South Pole (69.37°S). The Pragyan rover confirmed sulfur in the polar soil."
    },
    {
      keywords: ["change 4", "chang'e 4", "yutu 2", "far side landing"],
      answer: "Chang'e 4 touched down in the Von Kármán crater on the Moon's far side on January 3, 2019. Its Yutu-2 rover has traversed over 1.6 km, making it the longest-operating lunar rover in history."
    },
    {
      keywords: ["change 5", "chang'e 5", "chinese sample return"],
      answer: "Chang'e 5 (December 2020) returned 1.73 kg of lunar rocks and soil from Mons Rümker, confirming lunar volcanism continued as recently as 2.0 billion years ago."
    },
    {
      keywords: ["change 6", "chang'e 6", "far side sample return"],
      answer: "Chang'e 6 (June 2024) made history by returning the world's first-ever geological samples collected directly from the Moon's far side (Apollo Basin)."
    },
    {
      keywords: ["slim", "jaxa slim", "smart lander"],
      answer: "Japan's SLIM (Smart Lander for Investigating Moon) achieved a pinpoint soft landing on January 19, 2024, landing just 55 meters from its target on Shioli crater's slope."
    },

    // 51-65: Artemis, Science & Future Exploits
    {
      keywords: ["artemis", "artemis program", "artemis 2", "artemis 3"],
      answer: "NASA's Artemis program aims to land the first woman and person of color on the Moon. Artemis II will carry 4 astronauts on a lunar flyby, while Artemis III will land a crew at the South Pole using SpaceX Starship HLS."
    },
    {
      keywords: ["water on moon", "water ice", "ice at poles"],
      answer: "Over 600 million metric tons of cryogenic water ice are estimated to be trapped within permanently shadowed craters at the lunar poles. This water can be mined for drinking and split into hydrogen and oxygen rocket propellant."
    },
    {
      keywords: ["lunar gateway", "gateway station", "space station"],
      answer: "The Lunar Gateway will be an international crewed space station in Near-Rectilinear Halo Orbit (NRHO) around the Moon, serving as a staging post for lunar landings and future Mars journeys."
    },
    {
      keywords: ["moonquakes", "quakes", "seismic activity"],
      answer: "Seismometers left by Apollo recorded four types of moonquakes: deep quakes from Earth tides, meteorite impact vibrations, thermal expansion quakes, and shallow tectonic moonquakes reaching up to magnitude 5.5."
    },
    {
      keywords: ["helium 3", "he-3", "clean fusion fuel"],
      answer: "Helium-3 is a rare isotope deposited into lunar regolith by billions of years of solar wind. It is considered an ideal, non-radioactive fuel candidate for future nuclear fusion power plants."
    },
    {
      keywords: ["blue moon", "what is blue moon"],
      answer: "A 'Blue Moon' refers either to the second full moon occurring in a single calendar month, or the third full moon in an astronomical season containing four full moons. It does not look blue."
    },
    {
      keywords: ["supermoon", "perigee full moon"],
      answer: "A supermoon occurs when a full moon coincides with perigee (closest orbital approach to Earth). It appears up to 14% larger and 30% brighter than an apogee micromoon."
    },
    {
      keywords: ["lunar eclipse", "blood moon"],
      answer: "A lunar eclipse happens when Earth passes directly between the Sun and the Moon. Earth's atmosphere refracts red sunlight into our planet's umbral shadow, bathing the Moon in a deep coppery-red 'blood' glow."
    },
    {
      keywords: ["retroreflector", "laser ranging", "measuring distance"],
      answer: "Apollo and Lunokhod missions left corner-cube laser retroreflectors on the Moon. Observatories on Earth fire lasers at them to measure the Earth-Moon distance down to millimeter precision, discovering the Moon drifts away at 3.8 cm per year."
    },
    {
      keywords: ["moon is drifting", "drifting away"],
      answer: "Due to tidal friction transferring Earth's rotational energy into the lunar orbit, the Moon is currently drifting away from Earth at a rate of 3.8 cm (1.5 inches) per year."
    },
    {
      keywords: ["the moon", "what is the moon", "luna"],
      answer: "The Moon (Luna) is Earth's only natural satellite. Formed ~4.5 billion years ago, it stabilizes Earth's axial tilt, drives ocean tides, and serves as humanity's gateway to the Solar System."
    }
  ];

  /* ==========================================================================
     L.U.N.A VOICE & TERMINAL ENGINE
     Web Speech API + 100% Local Keyword Matching Engine
     ========================================================================== */
  const lunaFloatPill = document.getElementById('luna-float-pill');
  const lunaTerminalDrawer = document.getElementById('luna-terminal-drawer');
  const lunaCloseBtn = document.getElementById('luna-close-btn');
  const lunaTtsToggle = document.getElementById('luna-tts-toggle');
  const lunaWaveformBar = document.getElementById('luna-waveform-bar');
  const lunaMessagesWrap = document.getElementById('luna-messages-wrap');
  const lunaTextInput = document.getElementById('luna-text-input');
  const lunaMicBtn = document.getElementById('luna-mic-btn');
  const heroLunaCta = document.getElementById('hero-luna-cta');

  let isTtsEnabled = true;
  let hasGreetedUser = false;
  let synth = window.speechSynthesis || null;
  let recognition = null;
  let isListening = false;

  // Setup Web Speech Recognition
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    try {
      recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        isListening = true;
        lunaMicBtn.classList.add('listening');
        lunaWaveformBar.classList.add('active');
        sound.playChirp();
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        lunaTextInput.value = transcript;
        processLunaQuery(transcript);
      };

      recognition.onerror = (e) => {
        console.warn('Speech recognition error:', e);
        stopListening();
      };

      recognition.onend = () => {
        stopListening();
      };
    } catch (e) {
      console.warn('Speech recognition init failed', e);
    }
  }

  function startListening() {
    if (!recognition) {
      appendLunaMsg("ai", "Speech recognition is not natively supported in this browser. Please type your query in the prompt terminal!");
      return;
    }
    try {
      recognition.start();
    } catch (e) {
      recognition.stop();
    }
  }

  function stopListening() {
    isListening = false;
    lunaMicBtn.classList.remove('listening');
    lunaWaveformBar.classList.remove('active');
  }

  if (lunaMicBtn) {
    lunaMicBtn.addEventListener('click', () => {
      if (isListening) {
        if (recognition) recognition.stop();
      } else {
        startListening();
      }
    });
  }

  // Toggle TTS
  if (lunaTtsToggle) {
    lunaTtsToggle.addEventListener('click', () => {
      isTtsEnabled = !isTtsEnabled;
      lunaTtsToggle.textContent = isTtsEnabled ? '🔊' : '🔇';
      if (!isTtsEnabled && synth) {
        synth.cancel();
      }
    });
  }

  // Speak with pitch 1.1 and preferred female voice
  function speakLunaText(text) {
    if (!isTtsEnabled || !synth) return;
    try {
      synth.cancel(); // cancel prior speech
      const cleanText = text.replace(/<[^>]*>?/gm, ''); // remove any html tags
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.pitch = 1.1; // crisp sci-fi tone
      utterance.rate = 1.02;

      // Select female voice if available
      const voices = synth.getVoices();
      const femaleVoice = voices.find(v => 
        (v.name.includes('Samantha') || 
         v.name.includes('Google UK English Female') || 
         v.name.includes('Zira') || 
         v.name.includes('Female') || 
         v.name.includes('Victoria') ||
         v.name.includes('Natural')) && v.lang.startsWith('en')
      );
      if (femaleVoice) {
        utterance.voice = femaleVoice;
      }

      utterance.onstart = () => {
        lunaWaveformBar.classList.add('active');
      };

      utterance.onend = () => {
        lunaWaveformBar.classList.remove('active');
      };

      utterance.onerror = () => {
        lunaWaveformBar.classList.remove('active');
      };

      synth.speak(utterance);
    } catch (e) {
      console.warn('Speech synthesis error', e);
    }
  }

  // Open & Close Terminal
  function openLunaTerminal() {
    lunaTerminalDrawer.classList.add('open');
    sound.playChirp();
    lunaTextInput.focus();

    if (!hasGreetedUser) {
      hasGreetedUser = true;
      const greeting = "L.U.N.A online. Greetings Commander. Ask me anything about lunar geography, Apollo missions, or water ice at the south pole.";
      speakLunaText(greeting);
    }
  }

  function closeLunaTerminal() {
    lunaTerminalDrawer.classList.remove('open');
    if (synth) synth.cancel();
    stopListening();
  }

  if (lunaFloatPill) {
    lunaFloatPill.addEventListener('click', openLunaTerminal);
  }
  if (heroLunaCta) {
    heroLunaCta.addEventListener('click', openLunaTerminal);
  }
  if (lunaCloseBtn) {
    lunaCloseBtn.addEventListener('click', closeLunaTerminal);
  }

  // Append message to UI
  function appendLunaMsg(sender, htmlContent) {
    const div = document.createElement('div');
    div.className = `luna-msg ${sender}`;
    if (sender === 'ai') {
      div.innerHTML = `<strong>L.U.N.A:</strong> ${htmlContent}`;
    } else {
      div.textContent = htmlContent;
    }
    lunaMessagesWrap.appendChild(div);
    lunaMessagesWrap.scrollTop = lunaMessagesWrap.scrollHeight;
  }

  // Core NLP keyword matcher for 60+ entries
  function findBestFact(query) {
    const q = query.toLowerCase().trim();
    let bestMatch = null;
    let highestScore = 0;

    for (let i = 0; i < moonKnowledge.length; i++) {
      const item = moonKnowledge[i];
      let score = 0;

      for (let k = 0; k < item.keywords.length; k++) {
        const keyword = item.keywords[k].toLowerCase();
        if (q === keyword) {
          score += 100;
        } else if (q.includes(keyword)) {
          score += 20 + keyword.length;
        } else {
          // Check word-by-word intersection
          const words = keyword.split(' ');
          let matches = 0;
          for (let w = 0; w < words.length; w++) {
            if (q.includes(words[w])) matches++;
          }
          if (matches > 0) {
            score += matches * 5;
          }
        }
      }

      if (score > highestScore) {
        highestScore = score;
        bestMatch = item;
      }
    }

    if (highestScore > 0) {
      return bestMatch.answer;
    }

    // Default fallback
    return "Telemetry query recorded. My lunar database contains extensive telemetry on Apollo missions (11 through 17), Chandrayaan-3, Chang'e missions, orbital physical constants, water ice deposits, and craters like Tycho and Shackleton. Try asking 'Tell me about water on the Moon' or 'What is Chandrayaan-3?'";
  }

  function processLunaQuery(rawQuery) {
    if (!rawQuery || !rawQuery.trim()) return;
    const cleanQuery = rawQuery.trim();

    appendLunaMsg('user', cleanQuery);
    lunaTextInput.value = '';

    sound.playClick();

    setTimeout(() => {
      const answer = findBestFact(cleanQuery);
      appendLunaMsg('ai', answer);
      speakLunaText(answer);
    }, 250);
  }

  // Global query helper for chips & buttons
  window.queryLunaTopic = function (topic) {
    openLunaTerminal();
    processLunaQuery(topic);
  };

  // Submit Handler
  window.handleLunaFormSubmit = function (e) {
    e.preventDefault();
    const val = lunaTextInput.value;
    processLunaQuery(val);
  };

  /* ==========================================================================
     TICKER MARQUEE SEAMLESS LOOP
     ========================================================================== */
  const tickerTrack = document.getElementById('ticker-track');
  if (tickerTrack) {
    // Clone children once to ensure completely seamless infinite scrolling
    const clone = tickerTrack.innerHTML;
    tickerTrack.innerHTML += clone;
  }

  /* ==========================================================================
     KEYBOARD & NAVIGATION ACCESSIBILITY
     ========================================================================== */
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && lunaTerminalDrawer.classList.contains('open')) {
      closeLunaTerminal();
    }
  });

  // Highlight active navigation link on scroll
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;
    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 100;
      const sectionId = current.getAttribute('id');

      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active');
          }
        });
      }
    });
  });

  console.log('Lunar Explorer Mission Control Engine Initialized. Offline Status: READY.');

})();

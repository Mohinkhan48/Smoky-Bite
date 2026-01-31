(function () {
    console.log("Admin Notifications Script Loaded");

    let lastOrderId = localStorage.getItem('last_notified_order');
    let soundEnabled = false;
    const POLLING_INTERVAL = 10000;

    // Create the Toggle Button
    const toggleBtn = document.createElement('div');
    toggleBtn.id = "notif-toggle";
    toggleBtn.style.display = 'inline-flex';
    toggleBtn.style.alignItems = 'center';
    toggleBtn.style.marginLeft = '20px';
    toggleBtn.style.padding = '6px 16px';
    toggleBtn.style.borderRadius = '50px';
    toggleBtn.style.background = 'rgba(255, 255, 255, 0.05)';
    toggleBtn.style.border = '1px solid rgba(255, 255, 255, 0.1)';
    toggleBtn.style.cursor = 'pointer';
    toggleBtn.style.verticalAlign = 'middle';
    toggleBtn.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
    toggleBtn.style.boxShadow = '0 2px 10px rgba(0,0,0,0.3)';
    toggleBtn.style.userSelect = 'none';

    const icon = document.createElement('span');
    icon.innerHTML = "🔔";
    icon.style.marginRight = '8px';
    icon.style.fontSize = '14px';
    icon.style.filter = 'grayscale(1) opacity(0.5)';
    icon.style.transition = 'all 0.3s';

    const text = document.createElement('span');
    text.innerText = "NOTIFICATIONS: OFF";
    text.style.color = "#888";
    text.style.fontWeight = "900";
    text.style.fontSize = "10px";
    text.style.fontFamily = "'Satoshi', sans-serif";
    text.style.letterSpacing = "2px";
    text.style.textTransform = "uppercase";

    toggleBtn.appendChild(icon);
    toggleBtn.appendChild(text);

    // Hover effect
    toggleBtn.onmouseenter = () => {
        if (!soundEnabled) {
            toggleBtn.style.background = 'rgba(255, 255, 255, 0.1)';
            toggleBtn.style.borderColor = 'rgba(255, 255, 255, 0.2)';
            text.style.color = "#fff";
            icon.style.filter = 'grayscale(0) opacity(0.8)';
        }
    };
    toggleBtn.onmouseleave = () => {
        if (!soundEnabled) {
            toggleBtn.style.background = 'rgba(255, 255, 255, 0.05)';
            toggleBtn.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            text.style.color = "#888";
            icon.style.filter = 'grayscale(1) opacity(0.5)';
        }
    };

    // Sound Synthesis using Web Audio API (No files needed!)
    function playDing() {
        if (!soundEnabled) return;

        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            const ctx = new AudioContext();

            // Create oscillator for the main tone
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            // High pitch service bell frequency (1760Hz)
            osc.frequency.setValueAtTime(1760, ctx.currentTime);
            osc.type = 'sine';

            // Envelope: Percussive "Ding"
            gain.gain.setValueAtTime(0, ctx.currentTime);
            gain.gain.linearRampToValueAtTime(0.3, ctx.currentTime + 0.01);
            gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 1.0);

            osc.connect(gain);
            gain.connect(ctx.destination);

            osc.start();
            osc.stop(ctx.currentTime + 1.0);

            // Cleanup context after sound finishes
            setTimeout(() => ctx.close(), 1200);
        } catch (e) {
            console.error("Audio synthesis failed:", e);
        }
    }

    toggleBtn.onclick = (e) => {
        e.preventDefault();
        soundEnabled = !soundEnabled;
        if (soundEnabled) {
            text.innerText = "NOTIFICATIONS: ON";
            toggleBtn.style.background = "#ffd700";
            toggleBtn.style.borderColor = "#fff";
            toggleBtn.style.boxShadow = '0 0 15px rgba(255, 215, 0, 0.4)';
            text.style.color = "#000";
            icon.style.filter = 'grayscale(0) opacity(1)';
            playDing();
        } else {
            text.innerText = "NOTIFICATIONS: OFF";
            toggleBtn.style.background = 'rgba(255, 255, 255, 0.05)';
            toggleBtn.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            toggleBtn.style.boxShadow = '0 2px 10px rgba(0,0,0,0.3)';
            text.style.color = "#888";
            icon.style.filter = 'grayscale(1) opacity(0.5)';
        }
    };

    // Injection Logic: Target the header area robustly
    function injectToggle() {
        console.log("Attempting to inject toggle...");
        // Search multiple possible targets in the admin header
        const targets = [
            document.getElementById('site-name'),
            document.getElementById('branding'),
            document.querySelector('#header h1'),
            document.querySelector('.stats-header'), // Support the financial dashboard header too
            document.getElementById('header')
        ];

        let found = false;
        for (const target of targets) {
            if (target) {
                // Ensure target has flex to show toggle next to text
                if (target.id === 'site-name' || target.tagName === 'H1') {
                    target.style.display = 'inline-flex';
                    target.style.alignItems = 'center';
                }
                target.appendChild(toggleBtn);
                console.log("Toggle injected successfully into:", target);
                found = true;
                break;
            }
        }

        if (!found) {
            console.warn("Header not found, using fixed fallback");
            toggleBtn.style.position = 'fixed';
            toggleBtn.style.top = '10px';
            toggleBtn.style.left = '50%';
            toggleBtn.style.transform = 'translateX(-50%)';
            toggleBtn.style.zIndex = '99999';
            document.body.appendChild(toggleBtn);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectToggle);
    } else {
        injectToggle();
    }

    async function checkNewOrders() {
        try {
            const response = await fetch('/api/latest_order/');
            if (!response.ok) return;
            const data = await response.json();

            if (data.latest_id) {
                if (!lastOrderId) {
                    lastOrderId = data.latest_id;
                    localStorage.setItem('last_notified_order', lastOrderId);
                } else if (data.latest_id !== lastOrderId) {
                    lastOrderId = data.latest_id;
                    localStorage.setItem('last_notified_order', lastOrderId);
                    if (soundEnabled) {
                        playDing();
                    }
                }
            }
        } catch (error) {
            console.error("Polling error:", error);
        }
    }

    setInterval(checkNewOrders, POLLING_INTERVAL);
    checkNewOrders();
})();

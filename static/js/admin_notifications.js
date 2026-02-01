(function () {
    console.log("Admin Notifications Script Loaded");

    let lastOrderId = localStorage.getItem('last_notified_order');
    let soundEnabled = localStorage.getItem('sound_notifications_enabled') === 'true';
    const POLLING_INTERVAL = 10000; // Poll every 10 seconds

    // Create the Toggle Button
    const toggleBtn = document.createElement('div');
    toggleBtn.id = "notif-toggle";

    function updateUI(playSound = false) {
        if (soundEnabled) {
            text.innerText = "NOTIFICATIONS: ON";
            toggleBtn.style.background = "#ffd700";
            toggleBtn.style.borderColor = "#fff";
            toggleBtn.style.boxShadow = '0 0 15px rgba(255, 215, 0, 0.4)';
            text.style.color = "#000";
            icon.style.filter = 'grayscale(0) opacity(1)';
            if (playSound) playNotification();
        } else {
            text.innerText = "NOTIFICATIONS: OFF";
            toggleBtn.style.background = 'rgba(255, 255, 255, 0.05)';
            toggleBtn.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            toggleBtn.style.boxShadow = '0 2px 10px rgba(0,0,0,0.3)';
            text.style.color = "#888";
            icon.style.filter = 'grayscale(1) opacity(0.5)';
        }
    }
    toggleBtn.style.display = 'inline-flex';
    toggleBtn.style.alignItems = 'center';
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

    // Sound Synthesis: High-Loudness Triple-Alert (Optimized for attention)
    function playNotification() {
        if (!soundEnabled) return;

        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            const ctx = new AudioContext();

            function chime(freq, startTime, duration) {
                // Stack two oscillators for a much louder, richer harmonic sound
                const osc1 = ctx.createOscillator();
                const osc2 = ctx.createOscillator();
                const gain = ctx.createGain();

                osc1.type = 'sine';
                osc2.type = 'square'; // Square wave adds a "buzz" that makes it much louder to humans

                osc1.frequency.setValueAtTime(freq, startTime);
                osc2.frequency.setValueAtTime(freq, startTime);

                // Higher gain for maximum loudness (0.6 is very loud for Web Audio)
                gain.gain.setValueAtTime(0, startTime);
                gain.gain.linearRampToValueAtTime(0.6, startTime + 0.02);
                gain.gain.exponentialRampToValueAtTime(0.01, startTime + duration);

                osc1.connect(gain);
                osc2.connect(gain);
                gain.connect(ctx.destination);

                osc1.start(startTime);
                osc2.start(startTime);
                osc1.stop(startTime + duration);
                osc2.stop(startTime + duration);
            }

            // High-Loudness Triple Chime (D6 - F#6 - A6)
            chime(1174.66, ctx.currentTime, 0.4);          // D6
            chime(1479.98, ctx.currentTime + 0.15, 0.45);   // F#6
            chime(1760.00, ctx.currentTime + 0.30, 0.6);    // A6

            // Final safety cleanup
            setTimeout(() => ctx.close(), 2000);
        } catch (e) {
            console.error("Audio synthesis failed:", e);
        }
    }

    toggleBtn.onclick = (e) => {
        e.preventDefault();
        soundEnabled = !soundEnabled;
        localStorage.setItem('sound_notifications_enabled', soundEnabled);
        updateUI(true);
        if (soundEnabled) checkNewOrders();
    };

    // Injection Logic: Target the header area robustly
    function injectToggle() {
        if (document.getElementById('notif-toggle')) return;
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
        document.addEventListener('DOMContentLoaded', () => {
            injectToggle();
            updateUI();
        });
    } else {
        injectToggle();
        updateUI();
    }

    async function checkNewOrders() {
        if (!soundEnabled || document.hidden) return;

        try {
            // 1. Fetch Latest Order ID (for sound/auto-refresh part)
            const response = await fetch('/api/latest_order/');
            if (response.ok) {
                const data = await response.json();
                if (data.latest_id) {
                    const savedLastId = localStorage.getItem('last_notified_order');
                    if (savedLastId) lastOrderId = savedLastId;

                    if (!lastOrderId) {
                        lastOrderId = data.latest_id;
                        localStorage.setItem('last_notified_order', lastOrderId);
                    } else if (String(data.latest_id) !== String(lastOrderId)) {
                        lastOrderId = data.latest_id;
                        localStorage.setItem('last_notified_order', lastOrderId);
                        playNotification();

                        // Only auto-refresh if on the ORDERS LIST page
                        const path = window.location.pathname;
                        if (path.includes('/admin/orders/order/') && !path.includes('/add/') && !path.match(/\/\d+\//)) {
                            setTimeout(() => window.location.reload(), 1500);
                        }
                    }
                }
            }

            // 2. Fetch Dashboard Stats (if on index page)
            if (window.location.pathname === '/admin/' || window.location.pathname === '/admin/index.html') {
                const statsRes = await fetch('/api/dashboard_stats/');
                if (statsRes.ok) {
                    const stats = await statsRes.json();
                    const els = {
                        'stat-orders': stats.total_orders,
                        'stat-revenue': '₹' + stats.total_revenue,
                        'stat-profit': '₹' + stats.total_profit
                    };
                    for (const [id, val] of Object.entries(els)) {
                        const el = document.getElementById(id);
                        if (el && el.innerText !== String(val)) {
                            el.style.transition = 'all 0.5s';
                            el.style.transform = 'scale(1.2)';
                            el.style.color = '#ffd700';
                            setTimeout(() => {
                                el.innerText = val;
                                el.style.transform = 'scale(1)';
                                // Restore color after a bit
                                setTimeout(() => {
                                    el.style.color = id === 'stat-revenue' ? '#2ecc71' :
                                        id === 'stat-profit' ? '#3498db' : '#fff';
                                }, 500);
                            }, 300);
                        }
                    }
                }
            }
        } catch (error) {
            console.error("Polling network error:", error);
        }
    }

    setInterval(checkNewOrders, POLLING_INTERVAL);
    checkNewOrders();

    // Delivery Toggle UI Helper (Strict)
    window.toggleStrictOptions = function (idPrefix) {
        const el = document.getElementById(idPrefix + '-options');
        if (el) {
            const isHidden = el.style.display === 'none';
            document.querySelectorAll('.strict-options').forEach(c => c.style.display = 'none');
            if (isHidden) el.style.display = 'flex';
        }
    };

    window.confirmStatusUpdate = function (url, statusName) {
        window.location.href = url;
    };

    // Delivery Toggle UI Helper
    window.toggleDeliveryOptions = function (idPrefix) {
        const el = document.getElementById(idPrefix + '-options');
        if (el) {
            const isHidden = el.style.display === 'none';
            // Hide all others first for clean UI
            document.querySelectorAll('.delivery-toggle-container').forEach(c => c.style.display = 'none');
            if (isHidden) el.style.display = 'flex';
        }
    };
})();

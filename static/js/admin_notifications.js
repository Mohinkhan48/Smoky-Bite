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
    toggleBtn.style.padding = '4px 12px';
    toggleBtn.style.borderRadius = '4px';
    toggleBtn.style.background = '#222';
    toggleBtn.style.border = '1px solid #333';
    toggleBtn.style.cursor = 'pointer';
    toggleBtn.style.verticalAlign = 'middle';
    toggleBtn.style.transition = 'all 0.2s';

    const icon = document.createElement('span');
    icon.innerHTML = "🔔";
    icon.style.marginRight = '6px';
    icon.style.fontSize = '14px';

    const text = document.createElement('span');
    text.innerText = "NOTIFICATIONS: OFF";
    text.style.color = "#888";
    text.style.fontWeight = "bold";
    text.style.fontSize = "11px";
    text.style.letterSpacing = "1px";

    toggleBtn.appendChild(icon);
    toggleBtn.appendChild(text);

    // Audio Element
    const audio = new Audio('/static/audio/notify.mp3');

    toggleBtn.onclick = (e) => {
        e.preventDefault();
        soundEnabled = !soundEnabled;
        if (soundEnabled) {
            text.innerText = "NOTIFICATIONS: ON";
            toggleBtn.style.background = "#ffd700";
            toggleBtn.style.borderColor = "#fff";
            text.style.color = "#000";
            audio.play().catch(e => console.log("Audio unlock"));
        } else {
            text.innerText = "NOTIFICATIONS: OFF";
            toggleBtn.style.background = "#222";
            toggleBtn.style.borderColor = "#333";
            text.style.color = "#888";
        }
    };

    // Injection Logic: Try to find the branding header
    function injectToggle() {
        const branding = document.getElementById('branding') || document.querySelector('#header h1');
        if (branding) {
            branding.appendChild(toggleBtn);
            console.log("Toggle injected into branding");
        } else {
            // Fallback to fixed if branding not found
            toggleBtn.style.position = 'fixed';
            toggleBtn.style.bottom = '20px';
            toggleBtn.style.right = '20px';
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
                        audio.currentTime = 0;
                        audio.play().catch(e => console.error(e));
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

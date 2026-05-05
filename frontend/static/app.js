// State
let currentUser = null;

// Views
const loginSection = document.getElementById('login-section');
const appSection = document.getElementById('app-section');
const loginForm = document.getElementById('login-form');
const loginError = document.getElementById('login-error');
const userDisplay = document.getElementById('user-display');
const inputsSidebar = document.getElementById('inputs-sidebar');

// Tabs
const tabs = {
    dashboard: document.getElementById('tab-dashboard'),
    info: document.getElementById('tab-info'),
    audit: document.getElementById('tab-audit')
};

// Check if already logged in (using sessionStorage)
const storedUser = sessionStorage.getItem('user');
if (storedUser) {
    currentUser = JSON.parse(storedUser);
    showApp();
}

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    loginError.classList.add('hidden');
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const res = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (!res.ok) throw new Error("Invalid username or password");
        
        const data = await res.json();
        currentUser = data;
        sessionStorage.setItem('user', JSON.stringify(data));
        showApp();
    } catch (err) {
        loginError.textContent = err.message;
        loginError.classList.remove('hidden');
    }
});

function logout() {
    sessionStorage.removeItem('user');
    currentUser = null;
    appSection.classList.add('hidden');
    loginSection.classList.remove('hidden');
    document.getElementById('login-form').reset();
}

function showApp() {
    loginSection.classList.add('hidden');
    appSection.classList.remove('hidden');
    userDisplay.innerHTML = `👤 <b>${currentUser.display_name}</b> <i>(${currentUser.role})</i>`;
    switchTab('dashboard');
}

function switchTab(tabId) {
    Object.values(tabs).forEach(t => t.classList.add('hidden'));
    tabs[tabId].classList.remove('hidden');
    
    // Manage active nav state
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    const activeLink = document.querySelector(`.nav-link[onclick="switchTab('${tabId}')"]`);
    if (activeLink) activeLink.classList.add('active');
    
    // Show inputs only on dashboard
    inputsSidebar.style.display = tabId === 'dashboard' ? 'block' : 'none';
    
    if (tabId === 'audit') loadAuditLog();
}

// Prediction Logic
document.getElementById('predict-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    btn.disabled = true;
    btn.textContent = "Processing...";
    
    const payload = {
        data: {
            Type: parseInt(document.getElementById('quality').value),
            air_temperature: parseFloat(document.getElementById('air-temp').value),
            process_temperature: parseFloat(document.getElementById('process-temp').value),
            rotational_speed: parseInt(document.getElementById('speed').value),
            torque: parseFloat(document.getElementById('torque').value),
            tool_wear: parseInt(document.getElementById('tool-wear').value),
        },
        username: currentUser.username,
        role: currentUser.role,
        component_id: document.getElementById('comp-id').value
    };
    
    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await res.json();
        
        displayResult(result, payload);
    } catch (err) {
        alert("Error connecting to prediction server.");
    } finally {
        btn.disabled = false;
        btn.textContent = "🚀 Run Check";
    }
});

function displayResult(result, payload) {
    const area = document.getElementById('results-area');
    area.classList.remove('hidden');
    
    document.getElementById('res-status').textContent = result.prediction === 1 ? "NEEDS REPAIR" : "ALL GOOD";
    document.getElementById('res-status').className = result.prediction === 1 ? "fw-bold text-danger" : "fw-bold text-success";
    
    const probPct = (result.probability * 100).toFixed(2);
    document.getElementById('res-prob').textContent = `${probPct} %`;
    document.getElementById('res-eq').textContent = payload.component_id;
    
    const alertDiv = document.getElementById('res-alert');
    if (result.prediction === 1) {
        alertDiv.className = "alert alert-danger mt-3";
        alertDiv.innerHTML = `🚨 <b>WARNING — ${payload.component_id} may break down soon!</b><br>There is a ${probPct}% chance of failure. Please alert your supervisor.`;
    } else {
        alertDiv.className = "alert alert-success mt-3";
        alertDiv.innerHTML = `✅ <b>${payload.component_id} looks fine!</b><br>Chance of breaking down is only ${probPct}%. No action needed.`;
    }
}

async function loadAuditLog() {
    const tbody = document.getElementById('audit-tbody');
    tbody.innerHTML = "<tr><td colspan='5' class='text-center'>Loading...</td></tr>";
    try {
        const res = await fetch('/api/audit-log');
        const logs = await res.json();
        
        if (logs.length === 0) {
            tbody.innerHTML = "<tr><td colspan='5' class='text-center'>No checks recorded yet.</td></tr>";
            return;
        }
        
        tbody.innerHTML = logs.reverse().map(log => `
            <tr>
                <td>${log.timestamp}</td>
                <td>${log.username}</td>
                <td>${log.machine_id}</td>
                <td><span class="badge ${log.prediction == 1 ? 'bg-danger' : 'bg-success'}">${log.status}</span></td>
                <td>${(log.probability * 100).toFixed(2)}%</td>
            </tr>
        `).join('');
    } catch (err) {
        tbody.innerHTML = "<tr><td colspan='5' class='text-center text-danger'>Failed to load audit log.</td></tr>";
    }
}
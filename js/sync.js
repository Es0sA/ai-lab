/*
  AI Lab - GitHub Gist Sync
  Stores progress JSON in a private GitHub Gist so it syncs across all devices.
  The PAT and Gist ID are stored in localStorage only (never committed to the repo).
*/

const GIST_PAT_KEY    = 'ailab_gist_pat';
const GIST_ID_KEY     = 'ailab_gist_id';
const GIST_SYNC_KEY   = 'ailab_last_synced';
const GIST_FILE_NAME  = 'ailab_progress.json';
const GIST_DESC       = 'AI Lab - Learning Tracker Progress (auto-managed)';

/* ---------- Storage helpers ---------- */
function getPAT()    { return localStorage.getItem(GIST_PAT_KEY) || ''; }
function getGistId() { return localStorage.getItem(GIST_ID_KEY) || ''; }
function isConnected() { return !!(getPAT() && getGistId()); }

/* ---------- GitHub Gist API helpers ---------- */
async function gistRequest(method, path, body) {
  const res = await fetch('https://api.github.com' + path, {
    method,
    headers: {
      'Authorization': 'token ' + getPAT(),
      'Accept': 'application/vnd.github+json',
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.message || 'GitHub API error ' + res.status);
  }
  return res.json();
}

/* ---------- Create a new Gist ---------- */
async function createGist() {
  const data = await gistRequest('POST', '/gists', {
    description: GIST_DESC,
    public: false,
    files: {
      [GIST_FILE_NAME]: { content: JSON.stringify(getProgress(), null, 2) }
    }
  });
  localStorage.setItem(GIST_ID_KEY, data.id);
  return data.id;
}

/* ---------- Push local progress to Gist ---------- */
async function pushToGist() {
  let gistId = getGistId();
  if (!gistId) gistId = await createGist();
  const content = JSON.stringify(getProgress(), null, 2);
  await gistRequest('PATCH', '/gists/' + gistId, {
    files: { [GIST_FILE_NAME]: { content } }
  });
  const now = new Date().toLocaleTimeString();
  localStorage.setItem(GIST_SYNC_KEY, now);
  updateSyncUI();
}

/* ---------- Pull progress from Gist and merge ---------- */
async function pullFromGist() {
  const gistId = getGistId();
  if (!gistId) return;
  const data = await gistRequest('GET', '/gists/' + gistId);
  const file = data.files[GIST_FILE_NAME];
  if (!file) return;
  const remote = JSON.parse(file.content || '{}');
  const local  = getProgress();

  // Merge: a resource is checked if EITHER local or remote has it checked
  const merged = { ...local };
  for (const [weekId, items] of Object.entries(remote)) {
    if (!merged[weekId]) merged[weekId] = {};
    for (const [itemId, checked] of Object.entries(items)) {
      merged[weekId][itemId] = checked || (merged[weekId][itemId] || false);
    }
  }
  saveProgress(merged);
  const now = new Date().toLocaleTimeString();
  localStorage.setItem(GIST_SYNC_KEY, now);
}

/* ---------- Verify a PAT has gist scope ---------- */
async function verifyPAT(pat) {
  const res = await fetch('https://api.github.com/user', {
    headers: { 'Authorization': 'token ' + pat }
  });
  if (!res.ok) throw new Error('Invalid token or no network access.');
  const scopes = res.headers.get('x-oauth-scopes') || '';
  if (!scopes.split(',').map(s => s.trim()).includes('gist')) {
    throw new Error('Token is valid but is missing the "gist" scope. Please regenerate with gist scope enabled.');
  }
  return await res.json(); // returns user object
}

/* ---------- Connect flow ---------- */
async function connectGist(pat) {
  setSyncStatus('Verifying token...', 'pending');
  const user = await verifyPAT(pat);
  localStorage.setItem(GIST_PAT_KEY, pat);

  // Check if there is already a Gist ID stored from a previous session
  let gistId = getGistId();
  if (!gistId) {
    setSyncStatus('Creating Gist...', 'pending');
    gistId = await createGist();
  } else {
    // Try to pull existing progress from remote
    setSyncStatus('Pulling remote progress...', 'pending');
    await pullFromGist();
  }

  setSyncStatus('Connected as ' + user.login, 'connected');
  updateSyncUI();
  // Re-render checkboxes so pulled progress is visible
  window.location.reload();
}

/* ---------- Disconnect ---------- */
function disconnectGist() {
  localStorage.removeItem(GIST_PAT_KEY);
  localStorage.removeItem(GIST_ID_KEY);
  localStorage.removeItem(GIST_SYNC_KEY);
  updateSyncUI();
}

/* ---------- Auto-push on every checkbox change ---------- */
let pushTimer = null;
function schedulePush() {
  if (!isConnected()) return;
  clearTimeout(pushTimer);
  pushTimer = setTimeout(async () => {
    try {
      setSyncStatus('Syncing...', 'pending');
      await pushToGist();
      setSyncStatus('Synced', 'connected');
    } catch (e) {
      setSyncStatus('Sync failed: ' + e.message, 'error');
    }
  }, 1200); // debounce 1.2s
}

/* ---------- UI injection ---------- */
function injectSyncUI() {
  // Sync indicator in navbar
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    const indicator = document.createElement('button');
    indicator.id = 'sync-indicator';
    indicator.title = 'Sync Settings';
    indicator.onclick = () => document.getElementById('sync-modal').classList.add('open');
    indicator.style.cssText = `
      display:flex;align-items:center;gap:6px;
      background:var(--surface);border:1px solid var(--border);
      border-radius:99px;padding:5px 12px;cursor:pointer;
      font-size:12px;font-weight:600;color:var(--text-muted);
      transition:all 0.15s;
    `;
    indicator.innerHTML = '<span id="sync-dot" style="width:8px;height:8px;border-radius:50%;background:var(--text-muted);flex-shrink:0;"></span><span id="sync-label">Not synced</span>';
    navbar.appendChild(indicator);
  }

  // Modal
  const modal = document.createElement('div');
  modal.id = 'sync-modal';
  modal.style.cssText = `
    display:none;position:fixed;inset:0;z-index:200;
    background:rgba(0,0,0,0.7);backdrop-filter:blur(4px);
    align-items:center;justify-content:center;padding:16px;
  `;
  modal.innerHTML = `
    <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
      padding:28px;max-width:480px;width:100%;position:relative;">

      <button onclick="document.getElementById('sync-modal').classList.remove('open')"
        style="position:absolute;top:14px;right:14px;background:var(--surface2);
        border:none;color:var(--text-muted);border-radius:6px;padding:4px 8px;cursor:pointer;font-size:13px;">
        Close
      </button>

      <h2 style="font-size:18px;font-weight:700;margin-bottom:6px;">Cross-Device Sync</h2>
      <p style="font-size:13px;color:var(--text-muted);margin-bottom:20px;">
        Your progress is saved to a private GitHub Gist so it syncs across every device automatically.
        Your token is stored only in this browser and never sent anywhere except GitHub.
      </p>

      <div id="sync-connected-panel" style="display:none;">
        <div style="background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.2);
          border-radius:8px;padding:14px;margin-bottom:16px;">
          <div style="font-size:13px;font-weight:600;color:var(--green);margin-bottom:4px;">Connected</div>
          <div id="sync-gist-link" style="font-size:12px;color:var(--text-muted);"></div>
          <div id="sync-last-synced" style="font-size:12px;color:var(--text-muted);margin-top:4px;"></div>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <button onclick="syncManualPush()" class="btn btn-primary" style="font-size:13px;padding:8px 16px;">Push Now</button>
          <button onclick="syncManualPull()" class="btn btn-ghost" style="font-size:13px;padding:8px 16px;">Pull from Gist</button>
          <button onclick="if(confirm('Disconnect sync? Local progress is kept.')) { disconnectGist(); document.getElementById('sync-modal').classList.remove('open'); }"
            style="font-size:13px;padding:8px 16px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);
            color:#f87171;border-radius:6px;cursor:pointer;margin-left:auto;">Disconnect</button>
        </div>
      </div>

      <div id="sync-setup-panel">
        <label style="display:block;font-size:13px;font-weight:600;margin-bottom:8px;">
          GitHub Personal Access Token (PAT)
        </label>
        <p style="font-size:12px;color:var(--text-muted);margin-bottom:10px;">
          1. Go to <a href="https://github.com/settings/tokens/new?scopes=gist&description=AI+Lab+Sync" target="_blank" style="color:var(--accent);">github.com/settings/tokens</a>
          &rarr; Generate new token (Classic)<br>
          2. Check only the <strong>gist</strong> scope<br>
          3. Copy the token and paste it below
        </p>
        <input type="password" id="pat-input" placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
          style="width:100%;background:var(--surface2);border:1px solid var(--border);
          color:var(--text);border-radius:6px;padding:10px 12px;font-size:13px;
          font-family:var(--font-mono);margin-bottom:12px;outline:none;
          transition:border-color 0.15s;"
          onfocus="this.style.borderColor='var(--accent)'"
          onblur="this.style.borderColor='var(--border)'"
        >
        <div id="sync-error" style="color:#f87171;font-size:12px;margin-bottom:10px;display:none;"></div>
        <button onclick="handleConnect()" class="btn btn-primary" style="width:100%;">Connect &amp; Sync</button>
        <p style="font-size:11px;color:var(--text-muted);margin-top:10px;text-align:center;">
          Already connected on another device? Paste the same token and paste your Gist ID below (optional &mdash; leave blank to create a new one).
        </p>
        <input type="text" id="gist-id-input" placeholder="Gist ID (optional, e.g. a1b2c3d4e5...)"
          style="width:100%;background:var(--surface2);border:1px solid var(--border);
          color:var(--text);border-radius:6px;padding:8px 12px;font-size:12px;
          font-family:var(--font-mono);margin-top:6px;outline:none;
          transition:border-color 0.15s;"
          onfocus="this.style.borderColor='var(--accent)'"
          onblur="this.style.borderColor='var(--border)'"
        >
      </div>

      <div id="sync-status-msg" style="font-size:12px;color:var(--text-muted);margin-top:14px;text-align:center;min-height:18px;"></div>
    </div>
  `;

  modal.addEventListener('click', e => {
    if (e.target === modal) modal.classList.remove('open');
  });

  // CSS: show when .open
  const style = document.createElement('style');
  style.textContent = '#sync-modal.open { display:flex; }';
  document.head.appendChild(style);
  document.body.appendChild(modal);

  updateSyncUI();
}

function setSyncStatus(msg, state) {
  const el = document.getElementById('sync-status-msg');
  const dot = document.getElementById('sync-dot');
  const label = document.getElementById('sync-label');
  const indicator = document.getElementById('sync-indicator');
  if (el) el.textContent = msg;
  const colors = { connected: 'var(--green)', pending: 'var(--yellow)', error: 'var(--red)' };
  if (dot) dot.style.background = colors[state] || 'var(--text-muted)';
  if (label) label.textContent = state === 'connected' ? 'Synced' : state === 'pending' ? 'Syncing...' : state === 'error' ? 'Sync error' : 'Not synced';
  if (indicator && state === 'connected') indicator.style.borderColor = 'rgba(34,197,94,0.4)';
}

function updateSyncUI() {
  const connected = isConnected();
  const connectedPanel = document.getElementById('sync-connected-panel');
  const setupPanel = document.getElementById('sync-setup-panel');
  if (connectedPanel) connectedPanel.style.display = connected ? 'block' : 'none';
  if (setupPanel) setupPanel.style.display = connected ? 'none' : 'block';
  if (connected) {
    const gistId = getGistId();
    const linkEl = document.getElementById('sync-gist-link');
    if (linkEl) linkEl.innerHTML = 'Gist: <a href="https://gist.github.com/' + gistId + '" target="_blank" style="color:var(--accent);">' + gistId.slice(0,16) + '...</a>';
    const lastEl = document.getElementById('sync-last-synced');
    const last = localStorage.getItem(GIST_SYNC_KEY);
    if (lastEl) lastEl.textContent = last ? 'Last synced: ' + last : 'Not synced yet this session';
    setSyncStatus('Connected', 'connected');
  }
}

async function handleConnect() {
  const pat = document.getElementById('pat-input').value.trim();
  const gistIdInput = document.getElementById('gist-id-input').value.trim();
  const errEl = document.getElementById('sync-error');
  errEl.style.display = 'none';
  if (!pat) { errEl.textContent = 'Please enter a token.'; errEl.style.display = 'block'; return; }
  if (gistIdInput) localStorage.setItem(GIST_ID_KEY, gistIdInput);
  try {
    await connectGist(pat);
  } catch (e) {
    errEl.textContent = e.message;
    errEl.style.display = 'block';
    setSyncStatus('Connection failed', 'error');
  }
}

async function syncManualPush() {
  try {
    setSyncStatus('Pushing...', 'pending');
    await pushToGist();
    setSyncStatus('Connected', 'connected');
    updateSyncUI();
  } catch (e) {
    setSyncStatus('Push failed: ' + e.message, 'error');
  }
}

async function syncManualPull() {
  try {
    setSyncStatus('Pulling...', 'pending');
    await pullFromGist();
    setSyncStatus('Connected', 'connected');
    updateSyncUI();
    window.location.reload();
  } catch (e) {
    setSyncStatus('Pull failed: ' + e.message, 'error');
  }
}

/* ---------- Hook into progress changes ---------- */
const _origSaveProgress = saveProgress;
window.saveProgress = function(data) {
  _origSaveProgress(data);
  schedulePush();
};

/* ---------- Init on load ---------- */
document.addEventListener('DOMContentLoaded', async () => {
  injectSyncUI();
  if (isConnected()) {
    try {
      await pullFromGist();
      setSyncStatus('Connected', 'connected');
      updateSyncUI();
      // Re-render any checkboxes that were already initialised before pull
      document.querySelectorAll('.resource-checkbox').forEach(cb => {
        const data = getProgress();
        const id = cb.dataset.id;
        const weekId = Object.keys(data).find(w => data[w] && id in data[w]);
        if (weekId && data[weekId][id]) {
          cb.checked = true;
          cb.closest('.resource-item').classList.add('completed-item');
        }
      });
      if (typeof initDashboard === 'function') initDashboard();
      if (typeof updateWeekProgress === 'function') {
        const match = window.location.pathname.match(/\/(w\d+|prework)\.html/);
        if (match) updateWeekProgress(match[1]);
      }
    } catch (e) {
      setSyncStatus('Sync error: ' + e.message, 'error');
    }
  }
});

/* ---------- Expose functions globally for sync.html ---------- */
window.connectGist    = connectGist;
window.pushToGist     = pushToGist;
window.pullFromGist   = pullFromGist;
window.disconnectGist = disconnectGist;
window.isConnected    = isConnected;
window.getGistId      = getGistId;
window.GIST_SYNC_KEY  = GIST_SYNC_KEY;
window.GIST_ID_KEY    = GIST_ID_KEY;

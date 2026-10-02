/*
  AI Lab - Supabase Seamless Cloud Sync
  Syncs progress automatically across all devices using Supabase.
*/

const SUPABASE_URL = 'https://aiklahtntlljcttihemg.supabase.co';
const SUPABASE_KEY = 'sb_publishable_F4oh-gYnlMpTOMRC_9CD8g_uXD5I89B';
const USER_KEY = 'ailab_user_handle';
const DEFAULT_USER = 'esosa';

function getUserId() {
  return localStorage.getItem(USER_KEY) || DEFAULT_USER;
}

function setUserId(name) {
  if (name && name.trim()) {
    localStorage.setItem(USER_KEY, name.trim().toLowerCase());
  }
}

async function pullFromCloud() {
  const userId = getUserId();
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/user_progress?user_id=eq.${encodeURIComponent(userId)}&select=data`, {
      headers: {
        'apikey': SUPABASE_KEY,
        'Authorization': `Bearer ${SUPABASE_KEY}`
      }
    });
    if (!res.ok) return;
    const rows = await res.json();
    if (rows && rows.length > 0 && rows[0].data) {
      const remote = rows[0].data;
      const local = getProgress();
      // Merge progress: checked if true anywhere
      const merged = { ...local };
      for (const [w, items] of Object.entries(remote)) {
        if (!merged[w]) merged[w] = {};
        for (const [k, v] of Object.entries(items)) {
          merged[w][k] = v || (merged[w][k] || false);
        }
      }
      saveProgress(merged);
      updateSyncBadge('Synced', 'var(--green)');
    }
  } catch (err) {
    console.warn('Sync pull error:', err);
    updateSyncBadge('Offline', 'var(--yellow)');
  }
}

let syncTimeout = null;
async function pushToCloud() {
  clearTimeout(syncTimeout);
  syncTimeout = setTimeout(async () => {
    const userId = getUserId();
    const data = getProgress();
    updateSyncBadge('Saving...', 'var(--yellow)');
    try {
      const res = await fetch(`${SUPABASE_URL}/rest/v1/user_progress`, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`,
          'Content-Type': 'application/json',
          'Prefer': 'resolution=merge-duplicates'
        },
        body: JSON.stringify({
          user_id: userId,
          data: data,
          updated_at: new Date().toISOString()
        })
      });
      if (res.ok) {
        updateSyncBadge('Synced', 'var(--green)');
      } else {
        updateSyncBadge('Sync Error', 'var(--red)');
      }
    } catch (err) {
      console.warn('Sync push error:', err);
      updateSyncBadge('Offline', 'var(--yellow)');
    }
  }, 800);
}

function updateSyncBadge(label, color) {
  const dot = document.getElementById('cloud-sync-dot');
  const txt = document.getElementById('cloud-sync-text');
  if (dot) dot.style.backgroundColor = color;
  if (txt) txt.textContent = label;
}

// Hook into saveProgress
const _originalSave = window.saveProgress;
window.saveProgress = function(data) {
  _originalSave(data);
  pushToCloud();
};

document.addEventListener('DOMContentLoaded', async () => {
  // Inject clean cloud indicator
  const nav = document.querySelector('.navbar');
  if (nav && !document.getElementById('cloud-sync-indicator')) {
    const badge = document.createElement('div');
    badge.id = 'cloud-sync-indicator';
    badge.style.cssText = 'display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-muted);margin-left:auto;margin-right:12px;background:var(--surface2);padding:4px 10px;border-radius:99px;border:1px solid var(--border);';
    badge.innerHTML = '<span id="cloud-sync-dot" style="width:8px;height:8px;border-radius:50%;background:var(--green);display:inline-block;"></span><span id="cloud-sync-text">Synced</span>';
    nav.appendChild(badge);
  }

  await pullFromCloud();

  // Re-apply any newly pulled check states
  document.querySelectorAll('.resource-checkbox').forEach(cb => {
    const data = getProgress();
    const id = cb.dataset.id;
    for (const w of Object.keys(data)) {
      if (data[w] && data[w][id]) {
        cb.checked = true;
        const item = cb.closest('.resource-item');
        if (item) item.classList.add('completed-item');
      }
    }
  });

  if (typeof initDashboard === 'function') initDashboard();
  if (typeof updateCounts === 'function') updateCounts();
  const match = window.location.pathname.match(/\/(w\d+|prework)\.html/);
  if (match && typeof updateWeekProgress === 'function') updateWeekProgress(match[1]);
});

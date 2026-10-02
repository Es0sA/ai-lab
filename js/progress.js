/*
  AI Lab - Progress Tracker
  Uses localStorage to persist all checkbox states across pages.
*/

const STORAGE_KEY = 'ailab_progress';

// Master resource index per week (used for computing totals)
const WEEK_RESOURCE_COUNTS = {
  prework: 4,
  w1: 7,
  w2: 8,
  w3: 8,
  w4: 7,
  w5: 8,
  w6: 8,
  w7: 7,
  w8: 7,
  w9: 8,
  w10: 7,
  w11: 5,
  w12: 8,
  w13: 6,
};

function getProgress() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
  } catch {
    return {};
  }
}

function saveProgress(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

function getCheckedForWeek(weekId) {
  const data = getProgress();
  const weekData = data[weekId] || {};
  return Object.values(weekData).filter(Boolean).length;
}

function getTotalChecked() {
  const data = getProgress();
  let total = 0;
  for (const weekId of Object.keys(WEEK_RESOURCE_COUNTS)) {
    const weekData = data[weekId] || {};
    total += Object.values(weekData).filter(Boolean).length;
  }
  return total;
}

function getTotalResources() {
  return Object.values(WEEK_RESOURCE_COUNTS).reduce((a, b) => a + b, 0);
}

function initCheckboxes(weekId) {
  const data = getProgress();
  const weekData = data[weekId] || {};

  document.querySelectorAll('.resource-checkbox').forEach(cb => {
    const id = cb.dataset.id;
    if (weekData[id]) {
      cb.checked = true;
      cb.closest('.resource-item').classList.add('completed-item');
    }

    cb.addEventListener('change', () => {
      const current = getProgress();
      if (!current[weekId]) current[weekId] = {};
      current[weekId][id] = cb.checked;
      saveProgress(current);
      cb.closest('.resource-item').classList.toggle('completed-item', cb.checked);
      updateWeekProgress(weekId);
      dispatchProgressEvent();
    });
  });

  updateWeekProgress(weekId);
}

function updateWeekProgress(weekId) {
  const total = WEEK_RESOURCE_COUNTS[weekId] || 0;
  const checked = getCheckedForWeek(weekId);
  const pct = total > 0 ? Math.round((checked / total) * 100) : 0;

  const pctEl = document.getElementById('week-pct');
  const barEl = document.getElementById('week-bar');
  const checkedEl = document.getElementById('week-checked');
  const totalEl = document.getElementById('week-total');

  if (pctEl) pctEl.textContent = pct + '%';
  if (barEl) barEl.style.width = pct + '%';
  if (checkedEl) checkedEl.textContent = checked;
  if (totalEl) totalEl.textContent = total;
}

function initDashboard() {
  const totalRes = getTotalResources();
  const totalChecked = getTotalChecked();
  const pct = totalRes > 0 ? Math.round((totalChecked / totalRes) * 100) : 0;

  const pctEl = document.getElementById('global-pct');
  const barEl = document.getElementById('global-bar');
  const checkedEl = document.getElementById('global-checked');
  const totalEl = document.getElementById('global-total');

  if (pctEl) pctEl.textContent = pct + '%';
  if (barEl) barEl.style.width = pct + '%';
  if (checkedEl) checkedEl.textContent = totalChecked;
  if (totalEl) totalEl.textContent = totalRes;

  // Update each week card mini bar
  for (const [weekId, total] of Object.entries(WEEK_RESOURCE_COUNTS)) {
    const checked = getCheckedForWeek(weekId);
    const weekPct = total > 0 ? Math.round((checked / total) * 100) : 0;

    const miniBar = document.getElementById('mini-bar-' + weekId);
    const miniPct = document.getElementById('mini-pct-' + weekId);
    const card = document.getElementById('card-' + weekId);

    if (miniBar) miniBar.style.width = weekPct + '%';
    if (miniPct) miniPct.textContent = checked + '/' + total;

    if (card) {
      const statusEl = card.querySelector('.week-status');
      if (weekPct === 100) {
        card.classList.add('completed');
        if (statusEl) { statusEl.className = 'week-status done'; statusEl.textContent = 'Done'; }
      } else if (weekPct > 0) {
        card.classList.add('in-progress');
        if (statusEl) { statusEl.className = 'week-status active'; statusEl.textContent = 'In Progress'; }
      }
    }
  }
}

function dispatchProgressEvent() {
  window.dispatchEvent(new Event('ailab:progress'));
}

// Re-init dashboard stats when progress changes (cross-tab support)
window.addEventListener('storage', () => {
  if (typeof initDashboard === 'function') initDashboard();
});

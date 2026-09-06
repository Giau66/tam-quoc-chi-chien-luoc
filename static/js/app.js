// ==========================================================================
// TAM QUỐC CHÍ - CHIẾN LƯỢC: FRONTEND LOGIC (VANILLA JS)
// v3.0 - Chức năng Đề Xuất Đội Hình Meta & 175 Đội Excel Tối Giản
// ==========================================================================

const AppState = {
  db: {
    generals: [],
    tactics: [],
    meta_teams: [],
    tactic_substitutes: {}
  },
  ownedGenerals: new Set(),
  ownedTactics: new Set(),
  activeTab: 'tab-factions',
  apiKey: localStorage.getItem('tqc_gemini_api_key') || '',
  filters: {
    season: 'All',
    faction: 'All',
    troop: 'All',
    minScore: 30
  },
  starterData: null,
  starterFilterTroop: 'All',
  starterOnlyReady: false,
  factionTab: {
    activeFaction: 'All',
    filterTroop: 'All',
    filterTier: 'All',
    searchQuery: '',
    onlyOwned: false
  },
  uploadQueue: []
};

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', async () => {
  loadSavedInventory();
  setupEventListeners();
  setupStarterEventListeners();
  setupFactionEventListeners();
  setupUploadEventListeners();

  await fetchDatabase();
  renderInventory();
  updateStatBadges();

  // Initial fetch for all recommendation views & factions
  renderFactionTeams();
  fetchRecommendations();
  fetchStarterRecommendations();
  setupCloudSyncUI();

  handleHashNavigation();
  window.addEventListener('hashchange', handleHashNavigation);
});

function handleHashNavigation() {
  const hash = (window.location.hash || '').replace('#', '').trim();
  const validTabs = ['tab-factions', 'tab-upload', 'tab-recommend', 'tab-starter', 'tab-inventory'];
  if (hash && validTabs.includes(hash)) {
    switchTab(hash);
  }
}

// Hook: called by auth.js after cloud sync completes
window.onCloudSynced = function() {
  loadSavedInventory();
  renderInventory();
  updateStatBadges();
  fetchRecommendations();
  fetchStarterRecommendations();
  renderFactionTeams();
  showToast('☁️ Kho đồ đã được đồng bộ từ Cloud!', 'success');
};

// --- LOCAL STORAGE PERSISTENCE ---
function loadSavedInventory() {
  try {
    const savedGen = localStorage.getItem('tqc_generals') || localStorage.getItem('tqc_owned_generals');
    if (savedGen) {
      AppState.ownedGenerals = new Set(JSON.parse(savedGen));
    }
    const savedTac = localStorage.getItem('tqc_tactics') || localStorage.getItem('tqc_owned_tactics');
    if (savedTac) {
      AppState.ownedTactics = new Set(JSON.parse(savedTac));
    }
    if (AppState.apiKey) {
      const keyInput = document.getElementById('gemini-api-key');
      if (keyInput) keyInput.value = AppState.apiKey;
    }
  } catch (e) {
    console.warn('Lỗi đọc dữ liệu đã lưu:', e);
  }
}

function saveInventory() {
  const genArr = Array.from(AppState.ownedGenerals);
  const tacArr = Array.from(AppState.ownedTactics);
  localStorage.setItem('tqc_generals', JSON.stringify(genArr));
  localStorage.setItem('tqc_owned_generals', JSON.stringify(genArr));
  localStorage.setItem('tqc_tactics', JSON.stringify(tacArr));
  localStorage.setItem('tqc_owned_tactics', JSON.stringify(tacArr));
  updateStatBadges();

  if (typeof saveInventoryToCloud === 'function' && typeof AuthStore !== 'undefined' && AuthStore.isLoggedIn()) {
    saveInventoryToCloud(genArr, tacArr).then(() => {
      const badge = document.getElementById('cloud-save-badge');
      if (badge) { badge.textContent = '☁️ Đã lưu'; badge.style.color = '#34d399'; }
    });
  }
}

function resetInventoryData(skipConfirm = false) {
  if (skipConfirm || confirm('Bạn có chắc muốn làm mới kho đồ về 0 (xóa sạch toàn bộ tướng & chiến pháp đang lưu)?')) {
    AppState.ownedGenerals.clear();
    AppState.ownedTactics.clear();
    localStorage.removeItem('tqc_generals');
    localStorage.removeItem('tqc_owned_generals');
    localStorage.removeItem('tqc_tactics');
    localStorage.removeItem('tqc_owned_tactics');
    saveInventory();
    renderInventory();
    updateStatBadges();
    fetchRecommendations();
    fetchStarterRecommendations();
    renderFactionTeams();
    showToast('🗑️ Đã làm mới kho về 0 (0 Tướng, 0 Chiến pháp)');
  }
}
window.resetInventoryData = resetInventoryData;

// ── Cloud Sync UI ────────────────────────────────────────
function setupCloudSyncUI() {
  const syncBar = document.getElementById('cloud-sync-bar');
  if (!syncBar) return;

  if (typeof AuthStore !== 'undefined' && AuthStore.isLoggedIn()) {
    const user = AuthStore.getUser();
    syncBar.innerHTML = `
      <span style="color:#34d399">☁️ Cloud Save: <strong>${user?.display_name || user?.username || 'Bạn'}</strong></span>
      <button onclick="manualCloudSave()" style="margin-left:12px;padding:4px 12px;border-radius:6px;border:1px solid rgba(16,185,129,.4);background:rgba(16,185,129,.08);color:#34d399;font-size:12px;cursor:pointer;font-family:inherit">↑ Lưu Cloud</button>
      <button onclick="manualCloudLoad()" style="margin-left:6px;padding:4px 12px;border-radius:6px;border:1px solid rgba(56,189,248,.4);background:rgba(56,189,248,.08);color:#38bdf8;font-size:12px;cursor:pointer;font-family:inherit">↓ Tải Cloud</button>
      <span id="cloud-save-badge" style="margin-left:12px;font-size:12px;color:#6b7280"></span>`;
  } else {
    syncBar.innerHTML = `<span style="color:#6b7280;font-size:12px">⚠️ <a href="/" onclick="openAuthModal('login');return false;" style="color:#f59e0b;text-decoration:none">Đăng nhập</a> để bật Cloud Save — kho đồ được lưu trên mọi thiết bị.</span>`;
  }
}

async function manualCloudSave() {
  if (typeof saveInventoryToCloud !== 'function') return;
  const badge = document.getElementById('cloud-save-badge');
  if (badge) { badge.textContent = 'Đang lưu...'; badge.style.color = '#9ca3af'; }
  await saveInventoryToCloud(Array.from(AppState.ownedGenerals), Array.from(AppState.ownedTactics));
  if (badge) { badge.textContent = '✅ Đã lưu lên Cloud'; badge.style.color = '#34d399'; }
  showToast('☁️ Kho đồ đã lưu lên Cloud thành công!', 'success');
}

async function manualCloudLoad() {
  if (typeof syncInventoryFromCloud !== 'function') return;
  const data = await syncInventoryFromCloud();
  if (data) {
    loadSavedInventory();
    renderInventory();
    fetchRecommendations();
    renderFactionTeams();
    showToast('☁️ Đã tải kho đồ từ Cloud!', 'success');
  }
}

// --- FETCH DATABASE ---
async function fetchDatabase() {
  try {
    const res = await fetch('/api/database');
    if (res.ok) {
      const data = await res.json();
      AppState.db = data;
      // Update factions badge if present
      const factionsBadge = document.getElementById('factions-nav-badge');
      if (factionsBadge && data.meta_teams) {
        factionsBadge.textContent = `${data.meta_teams.length} Đội`;
      }
    }
  } catch (err) {
    showToast('⚠️ Không thể tải cơ sở dữ liệu từ máy chủ', 'error');
  }
}

// --- EVENT LISTENERS ---
function setupEventListeners() {
  // Main Nav Tabs
  document.querySelectorAll('.nav-tab').forEach(tabBtn => {
    tabBtn.addEventListener('click', () => {
      const tabTarget = tabBtn.getAttribute('data-tab');
      switchTab(tabTarget);
    });
  });

  // Gemini API Key Save & Toggle
  const btnSaveKey = document.getElementById('btn-save-key');
  if (btnSaveKey) {
    btnSaveKey.addEventListener('click', () => {
      const keyInput = document.getElementById('gemini-api-key');
      const val = keyInput ? keyInput.value.trim() : '';
      AppState.apiKey = val;
      localStorage.setItem('tqc_gemini_api_key', val);
      showToast('🔑 Đã lưu Google Gemini API Key!');
      const notice = document.getElementById('ai-key-notice');
      if (notice) notice.style.display = val ? 'none' : 'flex';
    });
  }

  const btnToggleKey = document.getElementById('btn-toggle-key');
  if (btnToggleKey) {
    btnToggleKey.addEventListener('click', () => {
      const keyInput = document.getElementById('gemini-api-key');
      if (!keyInput) return;
      if (keyInput.type === 'password') {
        keyInput.type = 'text';
        btnToggleKey.textContent = 'Ẩn Key';
      } else {
        keyInput.type = 'password';
        btnToggleKey.textContent = 'Hiện Key';
      }
    });
  }

  // Preset VIP Demo Data
  // Presets & Reset Data
  const btnDemo = document.getElementById('btn-demo-data');
  if (btnDemo) {
    btnDemo.addEventListener('click', loadDemoData);
  }

  // Reset Data
  const btnReset = document.getElementById('btn-reset-data');
  if (btnReset) {
    btnReset.addEventListener('click', () => resetInventoryData());
  }
  const btnNavReset = document.getElementById('navbar-link-reset');
  if (btnNavReset) {
    btnNavReset.addEventListener('click', () => resetInventoryData());
  }

  // Inventory Search & Filters
  const searchGen = document.getElementById('gen-search');
  if (searchGen) {
    searchGen.addEventListener('input', () => renderGenerals());
  }

  const searchTac = document.getElementById('tac-search');
  if (searchTac) {
    searchTac.addEventListener('input', () => renderTactics());
  }

  // Faction filter buttons for Generals
  const genFilterWrap = document.getElementById('gen-faction-filter');
  if (genFilterWrap) {
    genFilterWrap.querySelectorAll('.faction-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        genFilterWrap.querySelectorAll('.faction-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        renderGenerals();
      });
    });
  }

  // Type filter buttons for Tactics
  const tacFilterWrap = document.getElementById('tac-type-filter');
  if (tacFilterWrap) {
    tacFilterWrap.querySelectorAll('.faction-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        tacFilterWrap.querySelectorAll('.faction-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        renderTactics();
      });
    });
  }

  // Recommendation Filters
  ['filter-season', 'filter-faction', 'filter-troop'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('change', () => {
        const key = id.replace('filter-', '');
        AppState.filters[key] = el.value;
        fetchRecommendations();
      });
    }
  });

  const sliderScore = document.getElementById('filter-score');
  const sliderVal = document.getElementById('filter-score-val');
  if (sliderScore) {
    sliderScore.addEventListener('input', (e) => {
      const val = parseInt(e.target.value, 10);
      AppState.filters.minScore = val;
      if (sliderVal) sliderVal.textContent = `${val}%`;
    });
    sliderScore.addEventListener('change', () => {
      fetchRecommendations();
    });
  }

  const btnRecommend = document.getElementById('btn-recommend');
  if (btnRecommend) {
    btnRecommend.addEventListener('click', fetchRecommendations);
  }

  // Portfolio Builder Button
  const btnBuildPortfolio = document.getElementById('btn-build-portfolio');
  if (btnBuildPortfolio) {
    btnBuildPortfolio.addEventListener('click', fetchPortfolioRecommendations);
  }
}

// --- SWITCH TAB ---
function switchTab(tabId) {
  AppState.activeTab = tabId;
  document.querySelectorAll('.nav-tab').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-tab') === tabId);
  });
  document.querySelectorAll('.tab-panel').forEach(panel => {
    panel.classList.toggle('active', panel.id === tabId);
  });

  // Sync top navbar active state
  document.querySelectorAll('.site-navbar .nav-links .nav-link').forEach(link => {
    link.classList.remove('active');
  });
  if (tabId === 'tab-factions') {
    const el = document.getElementById('navbar-link-factions');
    if (el) el.classList.add('active');
  } else if (tabId === 'tab-upload') {
    const el = document.getElementById('navbar-link-upload');
    if (el) el.classList.add('active');
  } else if (tabId === 'tab-recommend') {
    const el = document.getElementById('navbar-link-recommend');
    if (el) el.classList.add('active');
  } else if (tabId === 'tab-starter') {
    const el = document.getElementById('navbar-link-starter');
    if (el) el.classList.add('active');
  } else if (tabId === 'tab-inventory') {
    const el = document.getElementById('navbar-link-inventory');
    if (el) el.classList.add('active');
  }

  if (tabId === 'tab-recommend') {
    fetchRecommendations();
  } else if (tabId === 'tab-factions') {
    renderFactionTeams();
  } else if (tabId === 'tab-starter') {
    fetchStarterRecommendations();
  }

  // Smooth scroll to top of main content
  const main = document.querySelector('.main-content');
  if (main) main.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// --- SWITCH INVENTORY SUB-TABS ---
function switchInventoryTab(tabName) {
  const genBtn = document.getElementById('inv-tab-generals');
  const tacBtn = document.getElementById('inv-tab-tactics');
  const genPanel = document.getElementById('inv-panel-generals');
  const tacPanel = document.getElementById('inv-panel-tactics');

  if (tabName === 'generals') {
    if (genBtn) genBtn.classList.add('active');
    if (tacBtn) tacBtn.classList.remove('active');
    if (genPanel) genPanel.classList.add('active');
    if (tacPanel) tacPanel.classList.remove('active');
  } else {
    if (genBtn) genBtn.classList.remove('active');
    if (tacBtn) tacBtn.classList.add('active');
    if (genPanel) genPanel.classList.remove('active');
    if (tacPanel) tacPanel.classList.add('active');
  }
}

// --- DROP ZONE & FILE UPLOAD (TAB 1) ---
function setupUploadEventListeners() {
  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('file-input');
  const btnSelect = document.getElementById('btn-select-files');
  const btnAnalyze = document.getElementById('btn-upload-analyze');
  const btnClear = document.getElementById('btn-clear-files');

  if (btnSelect && fileInput) {
    btnSelect.addEventListener('click', (e) => {
      e.stopPropagation();
      fileInput.click();
    });
  }

  if (dropZone && fileInput) {
    dropZone.addEventListener('click', (e) => {
      if (e.target !== btnSelect) fileInput.click();
    });

    ['dragenter', 'dragover'].forEach(name => {
      dropZone.addEventListener(name, (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
      }, false);
    });

    ['dragleave', 'drop'].forEach(name => {
      dropZone.addEventListener(name, (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
      }, false);
    });

    dropZone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      if (dt && dt.files && dt.files.length > 0) {
        addFilesToQueue(dt.files);
      }
    });

    fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files.length > 0) {
        addFilesToQueue(e.target.files);
      }
    });
  }

  if (btnAnalyze) {
    btnAnalyze.addEventListener('click', processUploadQueue);
  }

  if (btnClear) {
    btnClear.addEventListener('click', clearUploadQueue);
  }
}

function addFilesToQueue(fileList) {
  Array.from(fileList).forEach(f => {
    if (f.type.startsWith('image/')) {
      AppState.uploadQueue.push(f);
    }
  });

  renderUploadPreviews();
}

function clearUploadQueue() {
  AppState.uploadQueue = [];
  const fileInput = document.getElementById('file-input');
  if (fileInput) fileInput.value = '';

  const previewList = document.getElementById('file-preview-list');
  const actions = document.getElementById('upload-actions');
  const progress = document.getElementById('upload-progress');
  const results = document.getElementById('upload-results');

  if (previewList) { previewList.innerHTML = ''; previewList.style.display = 'none'; }
  if (actions) actions.style.display = 'none';
  if (progress) progress.style.display = 'none';
  if (results) { results.innerHTML = ''; results.style.display = 'none'; }
}

function renderUploadPreviews() {
  const previewList = document.getElementById('file-preview-list');
  const actions = document.getElementById('upload-actions');
  if (!previewList) return;

  if (AppState.uploadQueue.length === 0) {
    previewList.innerHTML = '';
    previewList.style.display = 'none';
    if (actions) actions.style.display = 'none';
    return;
  }

  previewList.style.display = 'grid';
  previewList.innerHTML = '';

  AppState.uploadQueue.forEach((file, index) => {
    const item = document.createElement('div');
    item.className = 'preview-item';

    const sizeKb = (file.size / 1024).toFixed(0);
    const reader = new FileReader();
    reader.onload = (e) => {
      item.innerHTML = `
        <img src="${e.target.result}" alt="${file.name}">
        <div class="preview-badge" title="${file.name}">${file.name} (${sizeKb} KB)</div>
        <button class="preview-remove-btn" title="Xóa ảnh này" onclick="removeUploadFile(${index}); event.stopPropagation();">✕</button>
      `;
    };
    reader.readAsDataURL(file);

    previewList.appendChild(item);
  });

  if (actions) actions.style.display = 'flex';
}

function removeUploadFile(index) {
  AppState.uploadQueue.splice(index, 1);
  renderUploadPreviews();
}

async function processUploadQueue() {
  const files = AppState.uploadQueue;
  if (!files || files.length === 0) {
    showToast('⚠️ Vui lòng chọn ít nhất 1 ảnh chụp màn hình game', 'warning');
    return;
  }

  const progress = document.getElementById('upload-progress');
  const progressText = document.getElementById('progress-text');
  const resultsDiv = document.getElementById('upload-results');
  const btnAnalyze = document.getElementById('btn-upload-analyze');

  if (progress) progress.style.display = 'flex';
  if (progressText) progressText.textContent = `Đang phân tích ${files.length} ảnh bằng AI...`;
  if (btnAnalyze) btnAnalyze.disabled = true;

  const formData = new FormData();
  files.forEach(file => formData.append('files', file));

  const apiKey = AppState.apiKey || localStorage.getItem('tqc_gemini_api_key');
  if (apiKey) {
    formData.append('gemini_api_key', apiKey);
  }

  try {
    const res = await fetch('/api/upload-images', {
      method: 'POST',
      body: formData
    });

    if (progress) progress.style.display = 'none';
    if (btnAnalyze) btnAnalyze.disabled = false;

    if (res.ok) {
      const data = await res.json();

      let addedGen = 0;
      let addedTac = 0;

      (data.generals || []).forEach(g => {
        if (!AppState.ownedGenerals.has(g)) {
          AppState.ownedGenerals.add(g);
          addedGen++;
        }
      });

      (data.tactics || []).forEach(t => {
        if (!AppState.ownedTactics.has(t)) {
          AppState.ownedTactics.add(t);
          addedTac++;
        }
      });

      saveInventory();
      renderInventory();
      fetchRecommendations();
      fetchStarterRecommendations();
      renderFactionTeams();

      if (resultsDiv) {
        resultsDiv.style.display = 'block';
        resultsDiv.innerHTML = `
          <div class="card alert alert-success" style="padding: 1.5rem; border-color: rgba(16,185,129,0.3); background: rgba(16,185,129,0.1);">
            <h3 style="color:#34d399; margin-bottom: 0.5rem; font-size:1.15rem;">
              ✅ Nhận diện thành công ${files.length} ảnh!
            </h3>
            <p style="color:#e5e7eb; margin-bottom: 1rem; font-size:0.95rem;">
              Tìm thấy tổng cộng <strong>${data.total_generals || 0} tướng</strong> và <strong>${data.total_tactics || 0} chiến pháp</strong>.
              <span style="color:#fbbf24;">(Mới thêm vào kho: +${addedGen} tướng, +${addedTac} chiến pháp).</span>
            </p>

            ${(data.generals && data.generals.length > 0) ? `
              <div style="margin-bottom: 1rem;">
                <strong style="color:var(--gold-light); font-size:0.88rem;">🗡️ TƯỚNG NHẬN DIỆN ĐƯỢC:</strong>
                <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">
                  ${data.generals.map(g => `<span class="meta-pill" style="background:rgba(59,130,246,0.15); color:#60a5fa; border-color:rgba(59,130,246,0.3); font-size:0.8rem;">${g}</span>`).join('')}
                </div>
              </div>
            ` : ''}

            ${(data.tactics && data.tactics.length > 0) ? `
              <div style="margin-bottom: 1.25rem;">
                <strong style="color:var(--gold-light); font-size:0.88rem;">📜 CHIẾN PHÁP NHẬN DIỆN ĐƯỢC:</strong>
                <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">
                  ${data.tactics.map(t => `<span class="meta-pill" style="background:rgba(245,158,11,0.15); color:#fbbf24; border-color:rgba(245,158,11,0.3); font-size:0.8rem;">${t}</span>`).join('')}
                </div>
              </div>
            ` : ''}

            <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:14px;">
              <button class="btn btn-primary" onclick="switchTab('tab-recommend')">
                🏆 Xem Đề Xuất Team Meta
              </button>
              <button class="btn btn-primary" style="background: linear-gradient(135deg, #10b981, #059669);" onclick="switchTab('tab-starter')">
                🌱 Xem Team Khai Hoang (Mở Đất)
              </button>
              <button class="btn btn-secondary" onclick="switchTab('tab-inventory')">
                ⚔️ Xem Kho Tướng &amp; Chiến Pháp
              </button>
            </div>
          </div>
        `;
      }

      showToast(`✨ Đã thêm +${addedGen} tướng và +${addedTac} chiến pháp vào kho đồ!`);
    } else {
      showToast('❌ Lỗi xử lý ảnh từ máy chủ', 'error');
    }
  } catch (err) {
    if (progress) progress.style.display = 'none';
    if (btnAnalyze) btnAnalyze.disabled = false;
    showToast('❌ Không thể kết nối tới API nhận diện ảnh', 'error');
  }
}

// --- RENDER INVENTORY (TAB 2) ---
function renderInventory() {
  renderGenerals();
  renderTactics();
  updateStatBadges();
}

function renderGenerals() {
  const container = document.getElementById('generals-grid');
  if (!container) return;

  const searchInput = document.getElementById('gen-search');
  const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

  const activeBtn = document.querySelector('#gen-faction-filter .faction-btn.active');
  const factionFilter = activeBtn ? activeBtn.getAttribute('data-faction') : 'All';

  const generals = AppState.db.generals || [];

  const filtered = generals.filter(g => {
    const matchName = g.name.toLowerCase().includes(query) || (g.inherent_skill && g.inherent_skill.toLowerCase().includes(query));
    const matchFaction = factionFilter === 'All' || g.faction === factionFilter;
    return matchName && matchFaction;
  });

  container.innerHTML = filtered.map(g => {
    const isOwned = AppState.ownedGenerals.has(g.name) || AppState.ownedGenerals.has(g.id);
    return `
      <div class="gen-card ${isOwned ? 'owned' : ''}" onclick="toggleGeneral('${g.name}')" title="${g.name} - ${g.inherent_skill || ''}">
        <div class="gen-card-top">
          <span class="gen-faction-tag faction-${g.faction}">${g.faction}</span>
          <span class="gen-cost">Cost ${g.cost || '?'}</span>
        </div>
        <div class="gen-name">${g.name}</div>
        <div class="gen-skill">${g.inherent_skill || ''}</div>
      </div>
    `;
  }).join('');

  const invGenCount = document.getElementById('inv-gen-count');
  if (invGenCount) {
    invGenCount.textContent = AppState.ownedGenerals.size;
  }
}

function renderTactics() {
  const container = document.getElementById('tactics-grid');
  if (!container) return;

  const searchInput = document.getElementById('tac-search');
  const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

  const activeBtn = document.querySelector('#tac-type-filter .faction-btn.active');
  const typeFilter = activeBtn ? activeBtn.getAttribute('data-type') : 'All';

  const tactics = AppState.db.tactics || [];

  const filtered = tactics.filter(t => {
    const matchName = t.name.toLowerCase().includes(query) || (t.description && t.description.toLowerCase().includes(query));
    const matchType = typeFilter === 'All' || t.type === typeFilter;
    return matchName && matchType;
  });

  container.innerHTML = filtered.map(t => {
    const isOwned = AppState.ownedTactics.has(t.name) || AppState.ownedTactics.has(t.id);
    const rankClass = t.rank === 'S' ? 'tactic-rank-S' : 'tactic-rank-A';
    return `
      <div class="tactic-card ${isOwned ? 'owned' : ''}" onclick="toggleTactic('${t.name}')" title="${t.name}: ${t.description || ''}">
        <div class="tactic-card-top">
          <span class="tactic-type-tag ${rankClass}">Hạng ${t.rank || 'S'}</span>
          <span class="tactic-type-tag">${t.type || 'Chủ động'}</span>
        </div>
        <div class="tactic-name">${t.name}</div>
      </div>
    `;
  }).join('');

  const invTacCount = document.getElementById('inv-tac-count');
  if (invTacCount) {
    invTacCount.textContent = AppState.ownedTactics.size;
  }
}

function toggleGeneral(name) {
  if (AppState.ownedGenerals.has(name)) {
    AppState.ownedGenerals.delete(name);
  } else {
    AppState.ownedGenerals.add(name);
  }
  saveInventory();
  renderGenerals();
  updateStatBadges();
  fetchRecommendations();
  fetchStarterRecommendations();
  renderFactionTeams();
}

function toggleTactic(name) {
  if (AppState.ownedTactics.has(name)) {
    AppState.ownedTactics.delete(name);
  } else {
    AppState.ownedTactics.add(name);
  }
  saveInventory();
  renderTactics();
  updateStatBadges();
  fetchRecommendations();
  fetchStarterRecommendations();
  renderFactionTeams();
}

function updateStatBadges() {
  const genCount = document.getElementById('stat-gen-count');
  const tacCount = document.getElementById('stat-tactic-count');
  const invCounter = document.getElementById('inventory-counter');
  const invGenCount = document.getElementById('inv-gen-count');
  const invTacCount = document.getElementById('inv-tac-count');

  const gSize = AppState.ownedGenerals.size;
  const tSize = AppState.ownedTactics.size;

  if (genCount) genCount.textContent = gSize;
  if (tacCount) tacCount.textContent = tSize;
  if (invCounter) invCounter.textContent = gSize + tSize;
  if (invGenCount) invGenCount.textContent = gSize;
  if (invTacCount) invTacCount.textContent = tSize;
}

// --- RECOMMENDATIONS (TAB 3) ---
async function fetchRecommendations() {
  const listContainer = document.getElementById('recommend-results');
  const countSpan = document.getElementById('results-count');
  const recommendBadge = document.getElementById('recommend-badge');

  if (!listContainer) return;

  // Empty inventory state: user hasn't uploaded photos yet
  if (AppState.ownedGenerals.size === 0) {
    if (countSpan) countSpan.textContent = '0';
    if (recommendBadge) recommendBadge.textContent = '0 Đội';
    listContainer.innerHTML = `
      <div class="card" style="text-align: center; padding: 3.5rem 1.5rem; max-width: 680px; margin: 2rem auto;">
        <div style="font-size: 3.5rem; margin-bottom: 0.8rem;">📷</div>
        <h3 style="color: var(--gold-light); margin-bottom: 0.75rem; font-size: 1.3rem;">Chưa Có Dữ Liệu Kho Tướng Của Bạn</h3>
        <p style="font-size: 0.95rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 1.5rem;">
          Hệ thống đề xuất dựa trên ảnh chụp kho tướng &amp; chiến pháp thực tế của bạn trong game.<br>
          Hãy tải ảnh kho của bạn lên để AI tự động nhận diện và tính toán các đội hình Meta bạn có thể xếp được!
        </p>
        <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
          <button class="btn btn-primary" onclick="switchTab('tab-upload')">
            📷 Tải Ảnh &amp; Nhận Diện Kho Của Bạn
          </button>
        </div>
      </div>
    `;
    return;
  }

  const payload = {
    owned_generals: Array.from(AppState.ownedGenerals),
    owned_tactics: Array.from(AppState.ownedTactics),
    season: AppState.filters.season || 'All',
    faction: AppState.filters.faction || 'All',
    troop: AppState.filters.troop || 'All',
    min_score: AppState.filters.minScore || 30,
    mode: 'ranked'
  };

  try {
    const res = await fetch('/api/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      const data = await res.json();
      const results = data.results || [];

      if (countSpan) countSpan.textContent = results.length;
      if (recommendBadge) recommendBadge.textContent = `${results.length} Đội`;

      if (results.length === 0) {
        listContainer.innerHTML = `
          <div class="card" style="text-align: center; padding: 3rem 1rem;">
            <p style="font-size: 1.1rem; color: var(--text-muted); margin-bottom: 1rem;">
              Chưa tìm thấy đội hình nào đạt trên ${AppState.filters.minScore}% độ hoàn thiện.
            </p>
            <p style="font-size: 0.9rem; color: var(--text-dim); margin-bottom: 1.5rem;">
              Bạn có thể hạ thanh trượt "Điểm tối thiểu" xuống 20-30% hoặc tải thêm ảnh kho tướng &amp; chiến pháp.
            </p>
            <button class="btn btn-primary" onclick="switchTab('tab-upload')">📷 Tải Thêm Ảnh Quét Kho</button>
          </div>
        `;
        return;
      }

      listContainer.innerHTML = results.map(item => renderTeamCard(item)).join('');
    }
  } catch (err) {
    console.error('Lỗi lấy gợi ý đội hình:', err);
  }
}

function renderTeamCard(evalRes) {
  const team = evalRes.meta_team;
  const generalsEval = evalRes.generals_eval;

  const tierClass = team.tier === 'T0' ? 'tier-T0' : (team.tier === 'T0.5' ? 'tier-T05' : 'tier-T1');

  let ownedBadgeHtml = '';
  if (evalRes.owned_gen_count === 3) {
    ownedBadgeHtml = '<span class="meta-pill" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; font-weight: 700;">✨ SỞ HỮU 3/3 TƯỚNG</span>';
  } else if (evalRes.owned_gen_count === 2) {
    ownedBadgeHtml = '<span class="meta-pill" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; font-weight: 700;">⚡ SỞ HỮU 2/3 TƯỚNG</span>';
  } else {
    ownedBadgeHtml = `<span class="meta-pill" style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); font-weight: 700;">❌ SỞ HỮU ${evalRes.owned_gen_count}/3 TƯỚNG</span>`;
  }

  const tacticPillHtml = `<span class="meta-pill" style="background: rgba(212, 175, 55, 0.15); color: #fde047; border: 1px solid rgba(212, 175, 55, 0.4); font-weight: 700;">📜 CP CHUẨN: ${evalRes.owned_bis_count}/${evalRes.total_tactics_count}</span>`;

  const smartBadges = (typeof buildSmartBadges === 'function') ? buildSmartBadges(evalRes) : '';

  const farmHtml = (evalRes.farm_suggestions && evalRes.farm_suggestions.length > 0 && typeof buildFarmSuggestions === 'function')
    ? buildFarmSuggestions(evalRes.farm_suggestions)
    : '';

  const analyzeBtn = (typeof buildAnalyzeButton === 'function') ? buildAnalyzeButton(evalRes) : '';

  const scoreTitle = `Tỉ lệ giống chuẩn: ${evalRes.overall_score}% | Tướng: ${evalRes.owned_gen_count}/3 | Chiến pháp: ${evalRes.owned_bis_count}/${evalRes.total_tactics_count}`;

  return `
    <div class="team-card">
      <div class="team-header">
        <div class="team-title-wrap">
          <span class="tier-badge ${tierClass}">${team.tier}</span>
          <div>
            <h4>${team.name}</h4>
            <div class="team-meta-pills">
              ${ownedBadgeHtml}
              ${tacticPillHtml}
              ${smartBadges}
              <span class="meta-pill">🏰 ${team.faction}</span>
              <span class="meta-pill">🛡️ Binh chủng: ${team.troop}</span>
              <span class="meta-pill">📅 Mùa: ${team.season || 'PK'}</span>
            </div>
          </div>
        </div>

        <div class="team-score-block">
          <span class="rating-badge ${evalRes.badge_class}">${evalRes.rating_label}</span>
          <div class="score-circle" title="${scoreTitle}">
            ${evalRes.overall_score}%
          </div>
        </div>
      </div>

      <div class="team-body">
        <div class="generals-lineup">
          ${generalsEval.map(slot => {
            const statusBadge = slot.is_owned
              ? '<span class="status-chip status-owned">✓ Có</span>'
              : '<span class="status-chip status-missing">❌ Chưa có</span>';

            return `
              <div class="general-slot-card">
                <div class="slot-position-tag">${slot.position}</div>
                <div class="slot-gen-identity">
                  <strong>${slot.target_name}</strong>
                  ${statusBadge}
                </div>

                <div class="slot-tactics-list">
                  ${slot.tactics.map(t => {
                    const slotClass = t.is_owned ? 'tactic-bis' : 'tactic-missing-slot';
                    const statusText = t.is_owned ? '✓ Có' : (t.is_substitute ? '🔄 Thay thế' : '❌ Thiếu');

                    return `
                      <div class="slot-tactic-item ${slotClass}">
                        <span class="slot-tactic-name">${t.name}</span>
                        <span class="slot-tactic-status">${statusText}</span>
                      </div>
                    `;
                  }).join('')}
                </div>

                ${(slot.binh_thu && slot.binh_thu.length > 0) ? `
                  <div class="slot-binh-thu-box" style="margin-top: 0.6rem; padding: 6px 8px; background: rgba(245, 158, 11, 0.06); border: 1px dashed rgba(245, 158, 11, 0.25); border-radius: 6px;">
                    <div style="font-size: 0.72rem; color: #fbbf24; font-weight: 700; margin-bottom: 4px; display: flex; align-items: center; gap: 4px;">
                      <span>📜 BINH THƯ CHUẨN:</span>
                    </div>
                    <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                      ${slot.binh_thu.map((bt, btIdx) => `
                        <span class="binh-thu-pill" style="font-size: 0.72rem; padding: 2px 7px; border-radius: 4px; background: ${btIdx === 0 ? 'rgba(217, 119, 6, 0.25)' : 'rgba(255, 255, 255, 0.05)'}; color: ${btIdx === 0 ? '#fde68a' : '#cbd5e1'}; border: 1px solid ${btIdx === 0 ? 'rgba(245, 158, 11, 0.4)' : 'rgba(255, 255, 255, 0.1)'}; font-weight: ${btIdx === 0 ? '700' : '500'};">
                          ${btIdx === 0 ? '★ ' : ''}${bt}
                        </span>
                      `).join('')}
                    </div>
                  </div>
                ` : ''}
              </div>
            `;
          }).join('')}
        </div>

        ${farmHtml}

        <div class="team-tactical-notes">
          <p class="notes-desc"><strong>💡 Đánh giá chiến thuật:</strong> ${team.description}</p>
          <div class="notes-chips-row">
            ${(team.strengths || []).map(s => `<span class="pro-chip">⚔️ ${s}</span>`).join('')}
            ${(team.weaknesses || []).map(w => `<span class="con-chip">⚠️ ${w}</span>`).join('')}
          </div>
        </div>
      </div>

      <div class="team-footer-actions">
        <button class="btn btn-outline btn-sm" onclick="copyTeamLineup('${team.id}')">
          📋 Sao chép cấu hình đội hình
        </button>
        ${analyzeBtn}
      </div>
    </div>
  `;
}

// --- PORTFOLIO MULTI-TEAM OPTIMIZER (TAB 6) ---
async function fetchPortfolioRecommendations() {
  const container = document.getElementById('portfolio-results');
  const countSelect = document.getElementById('portfolio-max-teams');
  const coexistList = document.getElementById('coexist-portfolios-list');
  if (!container) return;

  const maxTeams = countSelect ? parseInt(countSelect.value, 10) : 4;

  const payload = {
    owned_generals: Array.from(AppState.ownedGenerals),
    owned_tactics: Array.from(AppState.ownedTactics),
    mode: 'portfolio',
    max_teams: maxTeams
  };

  container.innerHTML = `
    <div style="text-align: center; padding: 2.5rem 0;">
      <div class="spinner"></div>
      <p style="color: var(--gold-light); margin-top: 12px;">Đang phân bổ tối ưu hóa chiến pháp và tướng không trùng lặp...</p>
    </div>
  `;

  try {
    const res = await fetch('/api/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      const data = await res.json();
      const teams = data.results || [];

      if (teams.length === 0) {
        container.innerHTML = `
          <div class="alert" style="background: rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.3);">
            ⚠️ Bạn chưa có đủ tướng hoặc chiến pháp để phân bổ tối thiểu 2 đội hình độc lập không trùng. Hãy tải thêm ảnh kho tướng/chiến pháp!
          </div>
        `;
      } else {
        let summaryHtml = `
          <div class="portfolio-summary-card">
            🎯 <strong>Thuật toán đã tối ưu xong:</strong> Phân bổ thành công <strong>${teams.length} đội hình</strong> xuất trận đồng thời.
            Tất cả các chiến pháp và tướng cốt lõi đều được chia tách hoàn hảo, không có bất kỳ xung đột nào giữa các đội!
          </div>
        `;

        let teamsHtml = teams.map((item, idx) => {
          return `
            <div style="margin-bottom: 0.5rem; font-size: 1.1rem; font-weight: 700; color: var(--gold-light);">
              🎖️ ĐỘI HÌNH ${idx + 1}
            </div>
            ${renderTeamCard(item)}
          `;
        }).join('');

        container.innerHTML = summaryHtml + teamsHtml;
      }

      // Render coexisting portfolios list
      if (coexistList && AppState.db.coexisting_portfolios) {
        renderCoexistPortfolios(coexistList, AppState.db.coexisting_portfolios);
      }
    }
  } catch (e) {
    console.error('Lỗi chạy portfolio:', e);
    container.innerHTML = `<div class="alert">Lỗi tính toán phân bổ đội hình</div>`;
  }
}

function renderCoexistPortfolios(container, sets) {
  if (!sets || sets.length === 0) return;
  container.innerHTML = `
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem;">
      ${sets.map(set => `
        <div class="card" style="background: rgba(18,22,34,0.9); border: 1px solid rgba(212,175,55,0.25); padding: 1.25rem;">
          <h4 style="color: var(--gold-light); margin-bottom: 0.35rem;">📜 ${set.set_name}</h4>
          <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 1rem;">${set.description}</p>
          <div style="display: flex; flex-direction: column; gap: 0.75rem;">
            ${(set.teams || []).map((st, sidx) => `
              <div style="padding: 0.6rem; background: rgba(0,0,0,0.3); border-radius: 6px; border-left: 3px solid var(--gold-primary);">
                <div style="font-weight: 600; font-size: 0.88rem; color: #fff; margin-bottom: 4px;">
                  ${sidx + 1}. ${(st.team_name || '').replace('\n', ' - ')}
                </div>
                <div style="font-size: 0.78rem; color: var(--text-dim);">
                  ${(st.generals || []).map(sg => `<strong>${sg.name}</strong> (${sg.tactic1 || ''}, ${sg.tactic2 || ''})`).join(' • ')}
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

// --- COPY TEAM LINEUP TO CLIPBOARD ---
function copyTeamLineup(teamId) {
  const team = (AppState.db.meta_teams || []).find(t => t.id === teamId);
  if (!team) return;

  let text = `【TAM QUỐC CHÍ - CHIẾN LƯỢC】\n`;
  text += `ĐỘI HÌNH META: ${team.name} [Tier: ${team.tier}]\n`;
  text += `Binh chủng: ${team.troop} | Phe: ${team.faction} | Mùa: ${team.season || 'PK'}\n`;
  text += `------------------------------------\n`;

  (team.generals || []).forEach(g => {
    text += `${g.position}: ${g.name}\n`;
    text += `  - Chiến pháp: ${(g.bis_tactics || []).join(', ')}\n`;
    if (g.binh_thu && g.binh_thu.length > 0) {
      text += `  - Binh thư: ${g.binh_thu.join(' - ')}\n`;
    }
    if (g.sub_tactics && g.sub_tactics.length > 0) {
      text += `  - Chiến pháp thay thế: ${g.sub_tactics.join(', ')}\n`;
    }
  });

  text += `------------------------------------\n`;
  text += `Chiến thuật: ${team.description}\n`;

  navigator.clipboard.writeText(text).then(() => {
    showToast(`📋 Đã sao chép cấu hình [${team.name}] vào bộ nhớ tạm!`);
  }).catch(() => {
    showToast('⚠️ Không thể sao chép tự động', 'error');
  });
}

// --- LOAD DEMO DATA ---
function loadDemoData() {
  const sampleGenerals = [
    "SP Mã Siêu", "SP Hoàng Phổ Tung", "Hứa Du", "SP Quan Vũ", "SP Tuân Úc",
    "Tư Mã Ý", "Tào Tháo", "Mãn Sủng", "Khương Duy", "Bàng Thống", "Gia Cát Lượng",
    "Lục Tốn", "Lỗ Túc", "SP Lữ Mông", "Tôn Thượng Hương", "Chu Thái", "Lăng Thống",
    "Cam Ninh", "Thái Sử Từ", "Trương Giác", "Tả Từ", "Vu Cát", "Triệu Vân",
    "Trương Phi", "Quan Vũ", "Lưu Bị", "Pháp Chính", "Hác Chiêu", "Giả Hủ", "Quách Gia",
    "Thái Văn Cơ", "Hạ Hầu Uyên", "Hoàng Trung", "Mã Siêu", "Lữ Bố", "Đổng Trác",
    "Viên Thiệu", "SP Chu Tuấn", "Quan Hưng", "Trương Bào"
  ];

  const sampleTactics = [
    "Thiết Kỵ Khu Trì", "Hổ Cứ Giang Đông", "Phá Quân Uy Thắng", "Hoành Tảo Thiên Quân",
    "Thảo Thuyền Mượn Tên", "Quân Dân Khích Lệ", "Đao Phách Tiên Đăng", "Phi Đao Đoạt Hồn",
    "Sĩ Biệt Ba Ngày", "Cạo Xương Chữa Độc", "Phong Tư Kiên Bích", "Đằng Giáp Binh",
    "Hãm Trận Doanh", "Bạch Mã Nghĩa Tùng", "Vô Đương Phi Quân", "Hổ Báo Kỵ",
    "Bát Môn Kim Tỏa", "Lạc Phượng", "Bất Nhục Sứ Mệnh", "Tị Thực Kích Hư",
    "Ngự Địch Bình Chướng", "Tịnh Hóa", "Đánh Đâu Thắng Đó", "Nhất Cử Tiệm Diệt"
  ];

  AppState.ownedGenerals = new Set(sampleGenerals);
  AppState.ownedTactics = new Set(sampleTactics);

  saveInventory();
  renderInventory();
  updateStatBadges();
  fetchRecommendations();
  fetchStarterRecommendations();
  renderFactionTeams();

  showToast('⚡ Đã nạp thành công Kho Mẫu VIP (40 Tướng Meta & 24 Chiến Pháp)!');
}

// --- STARTER TEAMS RECOMMENDATIONS & MINES GUIDE (TAB 5) ---
async function fetchStarterRecommendations() {
  const container = document.getElementById('starter-teams-list');
  const countSpan = document.getElementById('starter-ready-count');
  const navBadge = document.getElementById('starter-nav-badge');

  const payload = {
    owned_generals: Array.from(AppState.ownedGenerals),
    owned_tactics: Array.from(AppState.ownedTactics)
  };

  try {
    const res = await fetch('/api/recommend-starter', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      const data = await res.json();
      AppState.starterData = data;
      renderStarterTeams();
      renderMinesGuide(data.mines_guide);
      renderTouchScouts(data.touch_scout_teams);

      const readyCount = (data.starter_teams || []).filter(t => t.owned_generals_count >= 2).length;
      if (countSpan) countSpan.textContent = readyCount;
      if (navBadge) navBadge.textContent = `${readyCount} Đội`;
    }
  } catch (err) {
    console.error('Lỗi lấy dữ liệu khai hoang:', err);
  }
}

function renderStarterTeams() {
  const container = document.getElementById('starter-teams-list');
  if (!container || !AppState.starterData) return;

  const rawTeams = AppState.starterData.starter_teams || [];
  const troopFilter = AppState.starterFilterTroop || 'All';
  const onlyReady = AppState.starterOnlyReady || false;

  const filtered = rawTeams.filter(t => {
    const matchTroop = troopFilter === 'All' || (t.troop && t.troop.includes(troopFilter)) || (t.troop_lv20 && t.troop_lv20.includes(troopFilter));
    const matchReady = !onlyReady || (t.owned_generals_count >= 2);
    return matchTroop && matchReady;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="card" style="text-align: center; padding: 2.5rem 1rem;">
        <p style="color: var(--text-muted); font-size: 1rem;">
          Không tìm thấy đội hình khai hoang nào phù hợp với bộ lọc hiện tại.
        </p>
      </div>
    `;
    return;
  }

  const hasInventory = AppState.ownedGenerals.size > 0;

  const headerNotice = !hasInventory ? `
    <div style="margin-bottom: 1.25rem; padding: 0.85rem 1.15rem; border-radius: 8px; background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.25); display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; flex-wrap: wrap; gap: 10px;">
      <span>🌱 <em>Đang hiển thị các bộ khung đội hình Khai Hoang chuẩn mùa PK. Hãy tải ảnh kho tướng để AI kiểm tra đội nào bạn đủ điều kiện xuất trận!</em></span>
      <button class="btn btn-primary btn-sm" onclick="switchTab('tab-upload')" style="padding: 5px 14px; font-size: 0.82rem;">📷 Tải Ảnh Quét Kho</button>
    </div>
  ` : '';

  container.innerHTML = headerNotice + filtered.map(st => {
    const isReady = hasInventory && (st.owned_generals_count === st.total_generals);
    let badgeHtml = '';
    if (hasInventory) {
      if (isReady) {
        badgeHtml = `<span class="badge-tag" style="background: rgba(16,185,129,0.2); color: #34d399; border-color: #10b981;">✨ ĐỦ ${st.total_generals} TƯỚNG (100%)</span>`;
      } else if (st.owned_generals_count >= 2) {
        badgeHtml = `<span class="badge-tag" style="background: rgba(245,158,11,0.2); color: #fbbf24; border-color: #f59e0b;">⚡ CÓ ${st.owned_generals_count}/${st.total_generals} TƯỚNG (${st.gen_percentage}%)</span>`;
      } else {
        badgeHtml = `<span class="badge-tag" style="background: rgba(239,68,68,0.15); color: #f87171; border-color: rgba(239,68,68,0.3);">❌ CÓ ${st.owned_generals_count}/${st.total_generals} TƯỚNG</span>`;
      }
    }

    return `
      <div class="starter-card ${isReady ? 'ready-to-go' : ''}">
        <div class="starter-card-header">
          <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
            <span class="meta-pill" style="font-size: 0.92rem; font-weight: 700; color: var(--gold-light);">
              🛡️ Binh chủng: ${st.troop} ${st.troop_lv20 && st.troop_lv20 !== st.troop ? `➔ Lv20: ${st.troop_lv20}` : ''}
            </span>
            ${badgeHtml}
            <span class="rating-badge ${st.badge_class}" style="font-size: 0.76rem;">${st.starter_rating}</span>
          </div>
          <div style="font-size: 0.88rem; color: var(--text-muted);">
            ${hasInventory ? `Chiến pháp khớp: <strong style="color: var(--gold-light);">${st.tactic_percentage}%</strong>` : `<span style="font-size: 0.82rem; color: var(--gold-light);">📖 Mẫu Khai Hoang Chuẩn</span>`}
          </div>
        </div>

        <div class="starter-gens-lineup">
          ${st.generals.map(g => {
            const isGenOwned = hasInventory && g.is_owned;
            return `
              <div class="starter-gen-box ${hasInventory ? (isGenOwned ? 'owned-gen' : 'missing-gen') : ''}">
                <div class="starter-gen-title">
                  <strong>${g.active_name}</strong>
                  ${hasInventory ? `<span>${isGenOwned ? '✓ Có' : '❌ Thiếu'}</span>` : ''}
                </div>
                ${g.alt_name ? `<div style="font-size: 0.75rem; color: var(--text-dim);">(Hoặc: ${g.alt_name})</div>` : ''}

                <div style="margin-top: 0.5rem; display: flex; flex-direction: column; gap: 4px;">
                  <div class="starter-stage-section">
                    <span class="stage-label">Lv &lt; 20:</span>
                    <span class="starter-tactic-pill ${hasInventory ? (g.tactics_before_lv20.is_owned ? 'has-tac' : 'missing-tac') : 'neutral-tac'}">
                      ${g.tactics_before_lv20.name}
                    </span>
                  </div>
                  <div class="starter-stage-section">
                    <span class="stage-label">Lv &gt;= 20:</span>
                    <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                      ${g.tactics_after_lv20.map(tc => `
                        <span class="starter-tactic-pill ${hasInventory ? (tc.is_owned ? 'has-tac' : 'missing-tac') : 'neutral-tac'}">
                          ${tc.name}
                        </span>
                      `).join('')}
                    </div>
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>

        ${st.starter_note ? `
          <div class="starter-note-box" style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(0,0,0,0.25); border-radius: 6px; font-size: 0.84rem; color: var(--text-muted);">
            💡 <strong>Ghi chú khai hoang:</strong> ${st.starter_note}
          </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

function renderMinesGuide(minesGuide) {
  const container = document.getElementById('mines-guide-container');
  if (!container || !minesGuide) return;

  const tiers = Object.keys(minesGuide);
  container.innerHTML = tiers.map(tier => {
    const guards = minesGuide[tier] || [];
    return `
      <div class="mine-tier-card">
        <div class="mine-tier-header">
          <h4>🏰 ${tier} - Danh Sách Vệ Quân (Từ DỄ đến KHÓ)</h4>
          <span style="font-size: 0.8rem; color: var(--text-muted);">Ưu tiên đánh các vệ quân màu xanh trước</span>
        </div>
        <div class="mine-guards-flow">
          ${guards.map((guard, idx) => {
            let diffClass = 'guard-diff-med';
            let label = 'Trung bình';
            if (idx <= 1) {
              diffClass = 'guard-diff-easy';
              label = 'Dễ nhất';
            } else if (idx >= guards.length - 2) {
              diffClass = 'guard-diff-hard';
              label = 'Khó - Tránh';
            }

            return `
              <div class="guard-pill ${diffClass}" title="Độ khó: ${label}">
                <span>${idx + 1}. ${guard}</span>
                <span style="font-size: 0.7rem; opacity: 0.85;">(${label})</span>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }).join('');
}

function renderTouchScouts(scouts) {
  const container = document.getElementById('touch-scouts-container');
  if (!container || !scouts) return;

  container.innerHTML = scouts.map(sc => `
    <div class="touch-scout-card">
      <div class="touch-scout-header">
        <div class="touch-scout-title">⚔️ ${sc.name}</div>
        <span class="meta-pill" style="color: #f59e0b; border-color: rgba(245,158,11,0.3);">Mang 1 Lính</span>
      </div>
      <div class="touch-scout-tac">
        📜 <strong>Chiến pháp:</strong> ${sc.tactics}
      </div>
      <div class="touch-scout-desc">
        🎯 <strong>Tác dụng:</strong> ${sc.note}
      </div>
    </div>
  `).join('');
}

function setupStarterEventListeners() {
  const troopSelect = document.getElementById('starter-filter-troop');
  if (troopSelect) {
    troopSelect.addEventListener('change', (e) => {
      AppState.starterFilterTroop = e.target.value;
      renderStarterTeams();
    });
  }

  const chkReady = document.getElementById('starter-only-ready');
  if (chkReady) {
    chkReady.addEventListener('change', (e) => {
      AppState.starterOnlyReady = e.target.checked;
      renderStarterTeams();
    });
  }
}

// --- TAB: FACTIONS BY EXCEL (TAB 4) ---
function selectFactionTab(factionName) {
  AppState.factionTab.activeFaction = factionName;

  document.querySelectorAll('#faction-mega-tabs .faction-mega-tab').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-faction') === factionName);
  });

  const titleMap = {
    'All': 'TẤT CẢ CÁC PHE',
    'Ngụy': 'PHE NGỤY (ĐẾ CHẾ CAO NGUYÊN)',
    'Thục': 'PHE THỤC (THỤC HÁN TRUNG NGHĨA)',
    'Ngô': 'PHE NGÔ (GIANG ĐÔNG THỦY CHIẾN)',
    'Quần': 'PHE QUẦN (QUẦN HÙNG TRANH BÁ)',
    'Tam Thế': 'TAM THẾ & TIỀM LONG (LIÊN MINH ĐA PHE)'
  };
  const titleSpan = document.getElementById('factions-current-title');
  if (titleSpan) titleSpan.textContent = titleMap[factionName] || factionName;

  renderFactionTeams();
}

function setupFactionEventListeners() {
  // Mega-tabs click
  const megaWrap = document.getElementById('faction-mega-tabs');
  if (megaWrap) {
    megaWrap.querySelectorAll('.faction-mega-tab').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const f = e.currentTarget.getAttribute('data-faction') || 'All';
        selectFactionTab(f);
      });
    });
  }

  const troopSelect = document.getElementById('faction-filter-troop');
  if (troopSelect) {
    troopSelect.addEventListener('change', (e) => {
      AppState.factionTab.filterTroop = e.target.value;
      renderFactionTeams();
    });
  }

  const tierSelect = document.getElementById('faction-filter-tier');
  if (tierSelect) {
    tierSelect.addEventListener('change', (e) => {
      AppState.factionTab.filterTier = e.target.value;
      renderFactionTeams();
    });
  }

  const onlyOwnedCheck = document.getElementById('faction-only-owned');
  if (onlyOwnedCheck) {
    onlyOwnedCheck.addEventListener('change', (e) => {
      AppState.factionTab.onlyOwned = e.target.checked;
      renderFactionTeams();
    });
  }

  const searchInput = document.getElementById('faction-search');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      AppState.factionTab.searchQuery = e.target.value.toLowerCase().trim();
      renderFactionTeams();
    });
  }
}

function renderFactionTeams() {
  const container = document.getElementById('faction-teams-grid');
  const countSpan = document.getElementById('factions-count');
  if (!container) return;

  const hasInventory = AppState.ownedGenerals.size > 0 || AppState.ownedTactics.size > 0;
  const statusEl = document.getElementById('factions-inventory-status');
  if (statusEl) {
    if (hasInventory) {
      statusEl.innerHTML = `
        <div style="margin-bottom: 1.25rem; padding: 0.85rem 1.15rem; border-radius: 8px; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.35); display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; flex-wrap: wrap; gap: 10px;">
          <span>✅ Đang so khớp với kho đồ của bạn: <strong style="color: #34d399;">${AppState.ownedGenerals.size} Tướng</strong> &bull; <strong style="color: #fbbf24;">${AppState.ownedTactics.size} Chiến Pháp</strong></span>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-primary btn-sm" onclick="switchTab('tab-recommend')" style="padding: 5px 12px; font-size: 0.82rem;">🏆 Xem Đề Xuất Meta</button>
            <button class="btn btn-danger btn-sm" onclick="resetInventoryData()" style="padding: 5px 12px; font-size: 0.82rem;">🗑️ Làm Mới Kho Về 0</button>
          </div>
        </div>
      `;
    } else {
      statusEl.innerHTML = `
        <div style="margin-bottom: 1.25rem; padding: 0.85rem 1.15rem; border-radius: 8px; background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.25); display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; flex-wrap: wrap; gap: 10px;">
          <span>📋 <em>Đang hiển thị danh mục 175 đội hình nguyên bản theo file Excel. (Kho của bạn hiện đang trống: 0 Tướng - 0 Chiến Pháp)</em></span>
          <button class="btn btn-primary btn-sm" onclick="switchTab('tab-upload')" style="padding: 5px 14px; font-size: 0.82rem;">📷 Tải Ảnh Quét Kho Của Bạn</button>
        </div>
      `;
    }
  }

  const allTeams = AppState.db.meta_teams || [];
  const { activeFaction, filterTroop, filterTier, searchQuery, onlyOwned } = AppState.factionTab;

  const filtered = allTeams.filter(team => {
    if (activeFaction !== 'All' && team.faction !== activeFaction) return false;
    if (filterTroop !== 'All' && team.troop !== filterTroop) return false;
    if (filterTier !== 'All' && team.tier !== filterTier) return false;

    if (searchQuery) {
      const matchName = (team.name || '').toLowerCase().includes(searchQuery);
      const matchDesc = (team.description || '').toLowerCase().includes(searchQuery);
      const matchGen = (team.generals || []).some(g => g.name.toLowerCase().includes(searchQuery));
      const matchTac = (team.generals || []).some(g => (g.bis_tactics || []).some(t => t.toLowerCase().includes(searchQuery)));
      if (!matchName && !matchDesc && !matchGen && !matchTac) return false;
    }

    if (onlyOwned) {
      const ownedGensCount = (team.generals || []).filter(g => 
        AppState.ownedGenerals.has(g.name) || AppState.ownedGenerals.has(g.general_id)
      ).length;
      if (ownedGensCount < 3) return false;
    }
    return true;
  });

  if (countSpan) countSpan.textContent = filtered.length;

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="card" style="text-align: center; padding: 3rem 1rem; grid-column: 1 / -1;">
        <p style="font-size: 1.1rem; color: var(--text-muted); margin-bottom: 0.5rem;">
          Không tìm thấy đội hình nào phù hợp với bộ lọc hiện tại.
        </p>
        <p style="font-size: 0.85rem; color: var(--text-dim);">
          Hãy thử xóa từ khóa tìm kiếm hoặc bỏ chọn "Chỉ hiện đủ kho".
        </p>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(team => renderFactionTeamCard(team)).join('');
}

function renderFactionTeamCard(team) {
  const generals = team.generals || [];
  const tierClass = team.tier === 'T0' ? 'tier-T0' : (team.tier === 'T0.5' ? 'tier-T05' : 'tier-T1');

  const hasInventory = AppState.ownedGenerals.size > 0;
  const ownedGensCount = generals.filter(g => 
    AppState.ownedGenerals.has(g.name) || AppState.ownedGenerals.has(g.general_id)
  ).length;

  let ownedBadge = '';
  if (hasInventory) {
    if (ownedGensCount === 3) {
      ownedBadge = '<span class="meta-pill" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border-color: #10b981;">✨ ĐỦ 3/3 TƯỚNG</span>';
    } else if (ownedGensCount >= 1) {
      ownedBadge = `<span class="meta-pill" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24; border-color: #f59e0b;">⚡ CÓ ${ownedGensCount}/3 TƯỚNG</span>`;
    } else {
      ownedBadge = `<span class="meta-pill" style="background: rgba(239, 68, 68, 0.12); color: #f87171; border-color: rgba(239, 68, 68, 0.25);">Chưa có</span>`;
    }
  }

  return `
    <div class="team-card faction-team-card">
      <div class="team-header">
        <div class="team-title-wrap">
          <span class="tier-badge ${tierClass}">${team.tier}</span>
          <div>
            <h4>${team.name}</h4>
            <div class="team-meta-pills">
              ${ownedBadge}
              <span class="meta-pill">🏰 ${team.faction}</span>
              <span class="meta-pill">🛡️ ${team.troop}</span>
              <span class="meta-pill">📅 Mùa ${team.season || 'PK'}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="team-body">
        <div class="generals-lineup">
          ${generals.map(g => {
            const isOwned = hasInventory && (AppState.ownedGenerals.has(g.name) || AppState.ownedGenerals.has(g.general_id));

            return `
              <div class="general-slot-card">
                <div class="slot-position-tag">${g.position}</div>
                <div class="slot-gen-identity">
                  <strong>${g.name}</strong>
                  ${hasInventory ? `
                    <span class="status-chip ${isOwned ? 'status-owned' : 'status-missing'}">
                      ${isOwned ? '✓ Có' : 'Chưa có'}
                    </span>
                  ` : ''}
                </div>

                <div class="slot-tactics-list">
                  ${(g.bis_tactics || []).map(tacName => {
                    const hasTac = hasInventory && AppState.ownedTactics.has(tacName);
                    return `
                      <div class="slot-tactic-item ${hasInventory ? (hasTac ? 'tactic-bis' : 'tactic-missing-slot') : 'tactic-neutral'}">
                        <span class="slot-tactic-name">${tacName}</span>
                        ${hasInventory ? `<span class="slot-tactic-status">${hasTac ? '✓ Có' : 'Thiếu'}</span>` : ''}
                      </div>
                    `;
                  }).join('')}
                </div>

                ${(g.binh_thu && g.binh_thu.length > 0) ? `
                  <div class="slot-binh-thu-box" style="margin-top: 0.6rem; padding: 6px 8px; background: rgba(245, 158, 11, 0.06); border: 1px dashed rgba(245, 158, 11, 0.25); border-radius: 6px;">
                    <div style="font-size: 0.72rem; color: #fbbf24; font-weight: 700; margin-bottom: 4px; display: flex; align-items: center; gap: 4px;">
                      <span>📜 BINH THƯ CHUẨN:</span>
                    </div>
                    <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                      ${g.binh_thu.map((bt, btIdx) => `
                        <span class="binh-thu-pill" style="font-size: 0.72rem; padding: 2px 7px; border-radius: 4px; background: ${btIdx === 0 ? 'rgba(217, 119, 6, 0.25)' : 'rgba(255, 255, 255, 0.05)'}; color: ${btIdx === 0 ? '#fde68a' : '#cbd5e1'}; border: 1px solid ${btIdx === 0 ? 'rgba(245, 158, 11, 0.4)' : 'rgba(255, 255, 255, 0.1)'}; font-weight: ${btIdx === 0 ? '700' : '500'};">
                          ${btIdx === 0 ? '★ ' : ''}${bt}
                        </span>
                      `).join('')}
                    </div>
                  </div>
                ` : ''}
              </div>
            `;
          }).join('')}
        </div>

        ${team.description ? `
          <div class="team-tactical-notes" style="margin-top: 1rem;">
            <p class="notes-desc">💡 ${team.description}</p>
          </div>
        ` : ''}
      </div>

      <div class="team-footer-actions">
        <button class="btn btn-outline btn-sm" onclick="copyTeamLineup('${team.id}')">
          📋 Sao chép cấu hình
        </button>
      </div>
    </div>
  `;
}

// --- TAB 7: CẨM NANG CHIẾN PHÁP THAY THẾ A-TIER ---
function renderTacticSubstitutesGuide() {
  const container = document.getElementById('tactic-substitutes-guide');
  if (!container) return;

  const subs = AppState.db.tactic_substitutes || {};
  const keys = Object.keys(subs);
  if (keys.length === 0) {
    container.innerHTML = '<p style="color:var(--text-muted);grid-column:1/-1;text-align:center;padding:24px">Đang tải hướng dẫn chiến pháp thay thế...</p>';
    return;
  }

  container.innerHTML = keys.map(sTac => {
    const isOwned = AppState.ownedTactics.has(sTac);
    const aList = subs[sTac] || [];
    return `
      <div class="tactic-sub-card ${isOwned ? 'owned-bis' : ''}">
        <div class="tactic-sub-header">
          <div class="tactic-sub-name">
            <span class="tactic-rank-badge rank-s">S</span>
            <strong>${sTac}</strong>
          </div>
          <span class="sub-owned-status ${isOwned ? 'is-owned' : ''}">
            ${isOwned ? '✓ Đã sở hữu' : 'Chưa có'}
          </span>
        </div>
        <div class="tactic-sub-label">Phương án thay thế A-tier / thay thế tương đương:</div>
        <div class="tactic-sub-chips">
          ${aList.map(aTac => {
            const hasA = AppState.ownedTactics.has(aTac);
            return `
              <span class="tactic-chip ${hasA ? 'chip-owned' : 'chip-missing'}" title="${hasA ? 'Bạn đã sở hữu' : 'Chưa sở hữu'}">
                ${hasA ? '✓ ' : ''}${aTac}
              </span>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }).join('');
}

// --- TOAST NOTIFICATIONS ---
function showToast(message, type = 'success') {
  if (typeof window.showAuthToast === 'function') {
    window.showAuthToast(type, '', message);
    return;
  }
  let toast = document.getElementById('auth-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'auth-toast';
    toast.className = 'auth-toast';
    toast.innerHTML = `<div class="toast-icon"></div><div class="toast-body"><div class="toast-title"></div><div class="toast-msg"></div></div>`;
    document.body.appendChild(toast);
  }
  const icons = { success: '✅', error: '❌', info: '💬', warning: '⚠️' };
  const iconEl = toast.querySelector('.toast-icon');
  const titleEl = toast.querySelector('.toast-title');
  const msgEl = toast.querySelector('.toast-msg');
  if (iconEl) iconEl.textContent = icons[type] || '💬';
  if (titleEl) titleEl.textContent = type === 'error' ? 'Lỗi' : (type === 'warning' ? 'Chú Ý' : 'Thông Báo');
  if (msgEl) msgEl.textContent = message;
  toast.className = `auth-toast toast-${type}`;
  setTimeout(() => toast.classList.add('show'), 10);
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove('show'), 3500);
}

// Expose all interactive functions to window
window.switchTab = switchTab;
window.switchInventoryTab = switchInventoryTab;
window.toggleGeneral = toggleGeneral;
window.toggleTactic = toggleTactic;
window.copyTeamLineup = copyTeamLineup;
window.loadDemoData = loadDemoData;
window.selectFactionTab = selectFactionTab;
window.renderFactionTeams = renderFactionTeams;
window.fetchRecommendations = fetchRecommendations;
window.fetchStarterRecommendations = fetchStarterRecommendations;
window.fetchPortfolioRecommendations = fetchPortfolioRecommendations;
window.removeUploadFile = removeUploadFile;
window.showToast = showToast;
window.showToolsToast = showToast;

window.app = {
  switchTab,
  switchInventoryTab,
  toggleGeneral,
  toggleTactic,
  copyTeamLineup,
  loadDemoData,
  renderStarterTeams,
  fetchStarterRecommendations,
  selectFactionTab,
  renderFactionTeams,
  fetchRecommendations,
  fetchPortfolioRecommendations
};

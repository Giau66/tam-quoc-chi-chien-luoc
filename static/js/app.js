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
    filterSeason: 'All',
    filterTroop: 'All',
    filterTier: 'All',
    searchQuery: '',
    onlyOwned: false
  },
  caiTaoTab: {
    section: 'All',
    searchQuery: ''
  },
  cungTonTab: {
    selectedSetId: null
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

  // Initial fetch for all views & factions
  renderFactionTeams();
  fetchRecommendations();
  fetchStarterRecommendations();
  fetchDoUy();
  fetchCaiTao();
  fetchCungTon();
  setupCloudSyncUI();

  handleHashNavigation();
  window.addEventListener('hashchange', handleHashNavigation);
});

function handleHashNavigation() {
  const hash = (window.location.hash || '').replace('#', '').trim();
  const validTabs = ['tab-factions', 'tab-do-uy', 'tab-cai-tao', 'tab-cung-ton', 'tab-upload', 'tab-recommend', 'tab-starter', 'tab-inventory'];
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

  // Sync top navbar active state (primary 3 hubs)
  document.querySelectorAll('.site-navbar .nav-links .nav-link').forEach(link => {
    link.classList.remove('active');
  });

  if (['tab-factions', 'tab-do-uy', 'tab-cai-tao', 'tab-cung-ton'].includes(tabId)) {
    const el = document.getElementById('navbar-link-factions');
    if (el) el.classList.add('active');
  } else if (tabId === 'tab-recommend') {
    const el = document.getElementById('navbar-link-recommend');
    if (el) el.classList.add('active');
  } else if (tabId === 'tab-starter') {
    const el = document.getElementById('navbar-link-starter');
    if (el) el.classList.add('active');
  } else if (tabId === 'tab-upload' || tabId === 'tab-inventory') {
    const el = document.getElementById('navbar-link-upload');
    if (el) el.classList.add('active');
  }

  // Sync .team-category-switcher sub-pills across panels
  document.querySelectorAll('.team-category-switcher .cat-pill').forEach(pill => {
    const oc = pill.getAttribute('onclick') || '';
    const dt = pill.getAttribute('data-tab') || '';
    if (dt === tabId || oc.includes(`switchTab('${tabId}')`)) {
      pill.classList.add('active');
    } else {
      pill.classList.remove('active');
    }
  });

  if (tabId === 'tab-recommend') {
    fetchRecommendations();
  } else if (tabId === 'tab-factions') {
    renderFactionTeams();
  } else if (tabId === 'tab-starter') {
    fetchStarterRecommendations();
  } else if (tabId === 'tab-do-uy') {
    fetchDoUy();
  } else if (tabId === 'tab-cai-tao') {
    fetchCaiTao();
  } else if (tabId === 'tab-cung-ton') {
    fetchCungTon();
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

  // Support Ctrl+V paste from clipboard (Snipping Tool, PrintScreen, etc.)
  window.addEventListener('paste', (e) => {
    const items = e.clipboardData && e.clipboardData.items;
    if (!items) return;
    const pastedFiles = [];
    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf('image') !== -1) {
        const blob = items[i].getAsFile();
        if (blob) pastedFiles.push(blob);
      }
    }
    if (pastedFiles.length > 0) {
      switchTab('tab-upload');
      addFilesToQueue(pastedFiles);
      showToast(`📋 Đã dán ${pastedFiles.length} ảnh từ Clipboard! Nhấn 'Phân Tích Bằng AI' để quét.`);
    }
  });

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

// Giữ nguyên độ sắc nét ảnh gốc cho OCR (chỉ nén nếu ảnh quá lớn > 2.5MB)
async function compressImageForUpload(file, maxDimension = 1800, quality = 0.92) {
  if (!file || !file.type.startsWith('image/')) return file;
  // If file is already reasonable in size (<= 2.5MB), send original bytes for maximum OCR fidelity!
  if (file.size <= 2.5 * 1024 * 1024) {
    return file;
  }
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        let { width, height } = img;
        if (width > maxDimension || height > maxDimension) {
          if (width > height) {
            height = Math.round((height * maxDimension) / width);
            width = maxDimension;
          } else {
            width = Math.round((width * maxDimension) / height);
            height = maxDimension;
          }
        }
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);
        canvas.toBlob(
          (blob) => {
            if (!blob || blob.size >= file.size) {
              resolve(file);
            } else {
              const compressedFile = new File([blob], file.name.replace(/\.[^/.]+$/, '.jpg'), {
                type: 'image/jpeg',
                lastModified: Date.now()
              });
              resolve(compressedFile);
            }
          },
          'image/jpeg',
          quality
        );
      };
      img.onerror = () => resolve(file);
      img.src = e.target.result;
    };
    reader.onerror = () => resolve(file);
    reader.readAsDataURL(file);
  });
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
  if (btnAnalyze) btnAnalyze.disabled = true;

  const BATCH_SIZE = 4; // Chia nhỏ mỗi đợt 4 ảnh để tránh nghẽn mạng & timeout máy chủ
  const totalFiles = files.length;
  let totalAddedGen = 0;
  let totalAddedTac = 0;
  const allDetectedGens = new Set();
  const allDetectedTacs = new Set();

  try {
    const apiKey = AppState.apiKey || localStorage.getItem('tqc_gemini_api_key');

    for (let i = 0; i < totalFiles; i += BATCH_SIZE) {
      const batchFiles = files.slice(i, i + BATCH_SIZE);
      const batchStart = i + 1;
      const batchEnd = Math.min(i + BATCH_SIZE, totalFiles);

      if (progressText) {
        progressText.innerHTML = `
          <span>⚡ Đang nén &amp; AI quét ảnh <strong>${batchStart} - ${batchEnd} / ${totalFiles}</strong>...</span>
          <span style="font-size: 0.8rem; color: #34d399; margin-left: 8px;">(Đã tìm thấy: ${allDetectedGens.size} tướng, ${allDetectedTacs.size} chiến pháp)</span>
        `;
      }

      // Step 1: Compress images on client side
      const optimizedBatch = await Promise.all(
        batchFiles.map(f => compressImageForUpload(f))
      );

      // Step 2: Upload batch
      const formData = new FormData();
      optimizedBatch.forEach(file => formData.append('files', file));
      if (apiKey) {
        formData.append('gemini_api_key', apiKey);
      }

      const res = await fetch('/api/upload-images', {
        method: 'POST',
        body: formData
      });

      if (res.ok) {
        const data = await res.json();
        (data.generals || []).forEach(g => {
          allDetectedGens.add(g);
          if (!AppState.ownedGenerals.has(g)) {
            AppState.ownedGenerals.add(g);
            totalAddedGen++;
          }
        });
        (data.tactics || []).forEach(t => {
          allDetectedTacs.add(t);
          if (!AppState.ownedTactics.has(t)) {
            AppState.ownedTactics.add(t);
            totalAddedTac++;
          }
        });

        // Save inventory incrementally
        saveInventory();
        updateStatBadges();
      } else {
        console.warn(`Lỗi ở đợt ảnh ${batchStart} - ${batchEnd}`);
      }
    }

    if (progress) progress.style.display = 'none';
    if (btnAnalyze) btnAnalyze.disabled = false;

    // Render results
    renderInventory();
    fetchRecommendations();
    fetchStarterRecommendations();
    renderFactionTeams();

    if (resultsDiv) {
      resultsDiv.style.display = 'block';
      resultsDiv.innerHTML = `
        <div class="card alert alert-success" style="padding: 1.5rem; border-color: rgba(16,185,129,0.3); background: rgba(16,185,129,0.1);">
          <h3 style="color:#34d399; margin-bottom: 0.5rem; font-size:1.15rem;">
            ✅ Đã hoàn tất quét thành công toàn bộ ${totalFiles} ảnh!
          </h3>
          <p style="color:#e5e7eb; margin-bottom: 1rem; font-size:0.95rem;">
            Tìm thấy tổng cộng <strong>${allDetectedGens.size} tướng</strong> và <strong>${allDetectedTacs.size} chiến pháp</strong>.
            <span style="color:#fbbf24;">(Mới thêm vào kho: +${totalAddedGen} tướng, +${totalAddedTac} chiến pháp).</span>
          </p>

          ${(allDetectedGens.size > 0) ? `
            <div style="margin-bottom: 1rem;">
              <strong style="color:var(--gold-light); font-size:0.88rem;">🗡️ TƯỚNG NHẬN DIỆN ĐƯỢC:</strong>
              <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">
                ${Array.from(allDetectedGens).map(g => `<span class="meta-pill" style="background:rgba(59,130,246,0.15); color:#60a5fa; border-color:rgba(59,130,246,0.3); font-size:0.8rem;">${g}</span>`).join('')}
              </div>
            </div>
          ` : ''}

          ${(allDetectedTacs.size > 0) ? `
            <div style="margin-bottom: 1.25rem;">
              <strong style="color:var(--gold-light); font-size:0.88rem;">📜 CHIẾN PHÁP NHẬN DIỆN ĐƯỢC:</strong>
              <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">
                ${Array.from(allDetectedTacs).map(t => `<span class="meta-pill" style="background:rgba(245,158,11,0.15); color:#fbbf24; border-color:rgba(245,158,11,0.3); font-size:0.8rem;">${t}</span>`).join('')}
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

    showToast(`✨ Đã hoàn thành quét ${totalFiles} ảnh (+${totalAddedGen} tướng, +${totalAddedTac} chiến pháp)!`);
  } catch (err) {
    if (progress) progress.style.display = 'none';
    if (btnAnalyze) btnAnalyze.disabled = false;
    showToast('❌ Quá trình quét gặp sự cố kết nối, vui lòng thử lại', 'error');
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

  // Navbar and Sub-category counters
  const navGen = document.getElementById('nav-gen-count');
  const navTac = document.getElementById('nav-tac-count');
  const upGen = document.getElementById('upload-sub-gen-count');
  const upTac = document.getElementById('upload-sub-tac-count');

  const gSize = AppState.ownedGenerals.size;
  const tSize = AppState.ownedTactics.size;

  if (genCount) genCount.textContent = gSize;
  if (tacCount) tacCount.textContent = tSize;
  if (invCounter) invCounter.textContent = gSize + tSize;
  if (invGenCount) invGenCount.textContent = gSize;
  if (invTacCount) invTacCount.textContent = tSize;

  if (navGen) navGen.textContent = gSize;
  if (navTac) navTac.textContent = tSize;
  if (upGen) upGen.textContent = gSize;
  if (upTac) upTac.textContent = tSize;
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
      const recMeta1 = document.getElementById('rec-meta-count');
      const recMeta2 = document.getElementById('rec-meta-count-2');
      if (recMeta1) recMeta1.textContent = results.length;
      if (recMeta2) recMeta2.textContent = results.length;
      document.querySelectorAll('.badge-rec-meta').forEach(el => {
        el.textContent = results.length > 0 ? `(${results.length})` : '';
      });

      if (results.length === 0) {
        listContainer.innerHTML = `
          <div class="card" style="text-align: center; padding: 3rem 1rem;">
            <p style="font-size: 1.1rem; color: var(--text-muted); margin-bottom: 1rem;">
              Chưa tìm thấy đội hình nào đạt trên ${AppState.filters.minScore}% độ hoàn thiện.
            </p>
            <p style="font-size: 0.9rem; color: var(--text-dim); margin-bottom: 1.5rem;">
              Bạn có thể hạ thanh trượt "Điểm tối thiểu" xuống 20-30%, hoặc quét thêm ảnh kho tướng &amp; chiến pháp, hoặc xem trước toàn bộ 188 đội hình meta.
            </p>
            <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
              <button class="btn btn-primary" onclick="switchTab('tab-upload')">📷 Tải Thêm Ảnh Quét Kho</button>
              <button class="btn btn-secondary" onclick="switchTab('tab-factions')">⭐ Xem 188 Đội Meta PK</button>
              <button class="btn btn-outline" onclick="switchTab('tab-starter')">🌱 Xem 15 Đội Khai Hoang</button>
            </div>
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

  const actualOwnedGens = (generalsEval || []).filter(s => s.is_owned || AppState.ownedGenerals.has(s.target_name) || (s.target_id && AppState.ownedGenerals.has(s.target_id))).length;
  const displayOwnedCount = Math.max(evalRes.owned_gen_count || 0, actualOwnedGens);

  let ownedBadgeHtml = '';
  if (displayOwnedCount >= 3) {
    ownedBadgeHtml = '<span class="meta-pill" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; font-weight: 700;">✨ SỞ HỮU 3/3 TƯỚNG</span>';
  } else if (displayOwnedCount === 2) {
    ownedBadgeHtml = '<span class="meta-pill" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; font-weight: 700;">⚡ SỞ HỮU 2/3 TƯỚNG</span>';
  } else {
    ownedBadgeHtml = `<span class="meta-pill" style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); font-weight: 700;">❌ SỞ HỮU ${displayOwnedCount}/3 TƯỚNG</span>`;
  }

  const tacticPillHtml = `<span class="meta-pill" style="background: rgba(212, 175, 55, 0.15); color: #fde047; border: 1px solid rgba(212, 175, 55, 0.4); font-weight: 700;">📜 CP CHUẨN: ${evalRes.owned_bis_count}/${evalRes.total_tactics_count}</span>`;

  const smartBadges = (typeof buildSmartBadges === 'function') ? buildSmartBadges(evalRes) : '';

  const farmHtml = (evalRes.farm_suggestions && evalRes.farm_suggestions.length > 0 && typeof buildFarmSuggestions === 'function')
    ? buildFarmSuggestions(evalRes.farm_suggestions)
    : '';

  const analyzeBtn = (typeof buildAnalyzeButton === 'function') ? buildAnalyzeButton(evalRes) : '';

  const scoreTitle = `Tỉ lệ giống chuẩn: ${evalRes.overall_score}% | Tướng: ${displayOwnedCount}/3 | Chiến pháp: ${evalRes.owned_bis_count}/${evalRes.total_tactics_count}`;

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
            const isOwned = slot.is_owned || AppState.ownedGenerals.has(slot.target_name) || (slot.target_id && AppState.ownedGenerals.has(slot.target_id));
            const statusBadge = isOwned
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
                    const isTacOwned = t.is_owned || AppState.ownedTactics.has(t.name);
                    const slotClass = isTacOwned ? 'tactic-bis' : 'tactic-missing-slot';
                    const statusText = isTacOwned ? '✓ Có' : (t.is_substitute ? '🔄 Thay thế' : '❌ Thiếu');

                    return `
                      <div class="slot-tactic-item ${slotClass}">
                        <span class="slot-tactic-name">${t.name}</span>
                        <span class="slot-tactic-status">${statusText}</span>
                      </div>
                    `;
                  }).join('')}
                </div>

                ${(slot.binh_thu && slot.binh_thu.length > 0) ? `
                  <div class="slot-binh-thu-box">
                    <div class="binh-thu-label">
                      <span>📜 BINH THƯ CHUẨN:</span>
                    </div>
                    <div class="binh-thu-pills-row">
                      ${slot.binh_thu.map((bt, btIdx) => `
                        <span class="binh-thu-pill ${btIdx === 0 ? 'main-tome' : 'sub-tome'}">
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

      const allStarters = data.starter_teams || [];
      const hasInv = AppState.ownedGenerals.size > 0;
      const readyCount = allStarters.filter(t => t.owned_generals_count >= 2).length;
      if (countSpan) countSpan.textContent = hasInv ? `${readyCount}/${allStarters.length}` : allStarters.length;
      if (navBadge) navBadge.textContent = `${readyCount} Đội`;

      const recStar1 = document.getElementById('rec-starter-count');
      const recStar2 = document.getElementById('rec-starter-count-2');
      if (recStar1) recStar1.textContent = allStarters.length;
      if (recStar2) recStar2.textContent = allStarters.length;
      document.querySelectorAll('.badge-rec-starter').forEach(el => {
        el.textContent = hasInv ? `(${readyCount}/${allStarters.length})` : `(${allStarters.length})`;
      });
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
      } else if (st.owned_generals_count >= 1) {
        badgeHtml = `<span class="badge-tag" style="background: rgba(245,158,11,0.2); color: #fbbf24; border-color: #f59e0b;">⚡ CÓ ${st.owned_generals_count}/${st.total_generals} TƯỚNG (${st.gen_percentage}%)</span>`;
      } else {
        badgeHtml = `<span class="badge-tag" style="background: rgba(239,68,68,0.15); color: #f87171; border-color: rgba(239,68,68,0.3);">❌ THIẾU TƯỚNG</span>`;
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
            const isGenOwned = hasInventory && (g.is_owned || AppState.ownedGenerals.has(g.active_name));
            const earlyTac = g.cp_early || g.tactics_before_lv20 || { name: 'Chưa có', is_owned: false };
            const earlyName = earlyTac.name || '';
            const tacBeforeOwned = hasInventory && (earlyTac.is_owned || AppState.ownedTactics.has(earlyName));
            const lv20Tacs = g.cp_lv20 || g.tactics_after_lv20 || [];

            return `
              <div class="starter-gen-box ${hasInventory ? (isGenOwned ? 'owned-gen' : 'missing-gen') : ''}">
                <div class="starter-gen-title">
                  <strong>${g.active_name || g.target_name}</strong>
                  ${hasInventory ? `<span>${isGenOwned ? '✓ Có' : '❌ Thiếu'}</span>` : ''}
                </div>
                ${g.alt_name ? `<div style="font-size: 0.75rem; color: var(--text-dim);">(Hoặc: ${g.alt_name})</div>` : ''}

                <div style="margin-top: 0.5rem; display: flex; flex-direction: column; gap: 4px;">
                  <div class="starter-stage-section">
                    <span class="stage-label">Lv &lt; 20:</span>
                    <span class="starter-tactic-pill ${hasInventory ? (tacBeforeOwned ? 'has-tac' : 'missing-tac') : 'neutral-tac'}">
                      ${earlyName}
                    </span>
                  </div>
                  <div class="starter-stage-section">
                    <span class="stage-label">Lv &gt;= 20:</span>
                    <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                      ${lv20Tacs.map(tc => {
                        const tcName = tc.name || '';
                        const isTacOwned = hasInventory && (tc.is_owned || AppState.ownedTactics.has(tcName));
                        return `
                          <span class="starter-tactic-pill ${hasInventory ? (isTacOwned ? 'has-tac' : 'missing-tac') : 'neutral-tac'}">
                            ${tcName}
                          </span>
                        `;
                      }).join('')}
                    </div>
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>

        ${(st.starter_note || st.note) ? `
          <div class="starter-note-box" style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(0,0,0,0.25); border-radius: 6px; font-size: 0.84rem; color: var(--text-muted);">
            💡 <strong>Ghi chú khai hoang:</strong> ${st.starter_note || st.note}
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

  const seasonSelect = document.getElementById('faction-filter-season');
  if (seasonSelect) {
    seasonSelect.addEventListener('change', (e) => {
      AppState.factionTab.filterSeason = e.target.value;
      renderFactionTeams();
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
  const navBadge = document.getElementById('factions-nav-badge');
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
          <span>📋 <em>Đang hiển thị danh mục 178 đội hình nguyên bản theo file Excel. (Kho của bạn hiện đang trống: 0 Tướng - 0 Chiến Pháp)</em></span>
          <button class="btn btn-primary btn-sm" onclick="switchTab('tab-upload')" style="padding: 5px 14px; font-size: 0.82rem;">📷 Tải Ảnh Quét Kho Của Bạn</button>
        </div>
      `;
    }
  }

  const allTeams = AppState.db.meta_teams || [];
  if (navBadge && allTeams.length > 0) {
    navBadge.textContent = `${allTeams.length} Đội`;
  }
  const { activeFaction, filterSeason, filterTroop, filterTier, searchQuery, onlyOwned } = AppState.factionTab;

  const filtered = allTeams.filter(team => {
    if (activeFaction !== 'All' && team.faction !== activeFaction) return false;
    if (filterSeason && filterSeason !== 'All' && team.season !== filterSeason) return false;
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
                  <div class="slot-binh-thu-box">
                    <div class="binh-thu-label">
                      <span>📜 BINH THƯ CHUẨN:</span>
                    </div>
                    <div class="binh-thu-pills-row">
                      ${g.binh_thu.map((bt, btIdx) => `
                        <span class="binh-thu-pill ${btIdx === 0 ? 'main-tome' : 'sub-tome'}">
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
  fetchPortfolioRecommendations,
  fetchDoUy
};

// ==========================================================
// TEAM ĐÔ ÚY — FETCH & RENDER
// ==========================================================

async function fetchDoUy() {
  const grid = document.getElementById('do-uy-teams-grid');
  if (!grid) return;
  grid.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted)">⏳ Đang tải dữ liệu Team Đô Úy...</div>';
  try {
    const resp = await fetch('/api/team-do-uy');
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    const data = await resp.json();
    renderDoUyTeams(data);
  } catch (e) {
    grid.innerHTML = `<div style="text-align:center;padding:40px;color:#f87171">❌ Lỗi tải dữ liệu Team Đô Úy: ${e.message}</div>`;
  }
}

function renderDoUyTeams(teams) {
  const grid = document.getElementById('do-uy-teams-grid');
  const countEl = document.getElementById('do-uy-count');
  if (!grid) return;
  if (countEl) countEl.textContent = teams.length;

  const TROOP_ICON = { 'Thương': '🔱', 'Kỵ': '🐎', 'Cung': '🏹', 'Khiên': '🛡', 'Khí': '💨' };

  if (!teams || teams.length === 0) {
    grid.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted)">Không có dữ liệu Team Đô Úy.</div>';
    return;
  }

  grid.innerHTML = teams.map((team, idx) => {
    const gens = (team.generals || []);
    const troop = team.troop || 'Kỵ';
    const icon = TROOP_ICON[troop] || '⚔️';
    const note = team.note || '';

    // Extract chạm/tránh from note
    let cham = '', tranh = '';
    if (note.includes('Chạm:')) {
      const after = note.split('Chạm:')[1];
      if (after.includes('Tránh:')) {
        cham = after.split('Tránh:')[0].trim();
        tranh = after.split('Tránh:')[1].trim();
      } else {
        cham = after.trim();
      }
    }

    const gensHtml = gens.map((g, gi) => {
      const gName = g.name || g.raw_name || '';
      const cp1 = g.cp1 || g.cp1_raw || '';
      const cp2 = g.cp2 || g.cp2_raw || '';
      const bt = (g.binh_thu || []).filter(b => b);
      const pos = gi === 0 ? 'Chủ tướng' : `Phó tướng ${gi}`;
      const posClass = gi === 0 ? 'pos-main' : 'pos-sub';

      const tacticsHtml = [cp1, cp2].filter(Boolean).map(t =>
        `<span class="tactic-pill">${t}</span>`
      ).join('');

      const btHtml = bt.length > 0
        ? `<div class="binh-thu-row">${bt.map((b, bi) => `<span class="binh-thu-pill ${bi === 0 ? 'main-tome' : 'sub-tome'}">${bi === 0 ? '★ ' : ''}${b}</span>`).join('')}</div>`
        : '';

      return `
        <div class="general-slot ${posClass}">
          <div class="gen-header">
            <span class="gen-pos-badge ${posClass}">${pos}</span>
            <span class="gen-name">${gName}</span>
          </div>
          <div class="gen-tactics">${tacticsHtml}</div>
          ${btHtml}
        </div>`;
    }).join('');

    const noteHtml = note ? `
      <div class="team-note-block" style="margin-top:10px;padding:8px 12px;background:rgba(167,139,250,0.08);border-left:3px solid #7c3aed;border-radius:6px;font-size:12px;color:var(--text-muted)">
        ${cham ? `<div>✅ <strong>Chạm:</strong> ${cham}</div>` : ''}
        ${tranh ? `<div>⚠️ <strong>Tránh:</strong> ${tranh}</div>` : ''}
        ${!cham && !tranh ? `<div>${note}</div>` : ''}
      </div>` : '';

    return `
      <div class="team-card do-uy-card" style="border-top:3px solid #7c3aed">
        <div class="team-card-header">
          <div class="team-badge-group">
            <span class="troop-badge" style="background:rgba(124,58,237,0.15);color:#a78bfa;border:1px solid rgba(124,58,237,0.3)">${icon} ${troop}</span>
            <span class="tier-badge tier-t1" style="background:rgba(124,58,237,0.2);color:#c4b5fd">🛡 Đô Úy</span>
          </div>
          <span class="team-number" style="color:#7c3aed">#${idx + 1}</span>
        </div>
        <div class="team-generals">
          ${gensHtml}
        </div>
        ${noteHtml}
      </div>`;
  }).join('');
}

// ==========================================================
// CẢI TẠO BINH CHỦNG & LỆNH ĐĂNG UNG — FETCH & RENDER
// ==========================================================

let _caiTaoData = [];

async function fetchCaiTao() {
  const grid = document.getElementById('cai-tao-teams-grid');
  if (!grid) return;
  grid.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted)">⏳ Đang tải dữ liệu Cải Tạo Binh Chủng...</div>';
  try {
    const resp = await fetch('/api/cai-tao-binh-chung');
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    _caiTaoData = await resp.json();
    renderCaiTaoTeams();
  } catch (e) {
    grid.innerHTML = `<div style="text-align:center;padding:40px;color:#f87171">❌ Lỗi tải dữ liệu Cải Tạo Binh Chủng: ${e.message}</div>`;
  }
}

function filterCaiTaoSection(sec) {
  AppState.caiTaoTab.section = sec;
  document.querySelectorAll('#cai-tao-tabs .faction-mega-tab').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-section') === sec);
  });
  renderCaiTaoTeams();
}

function filterCaiTaoSearch(val) {
  AppState.caiTaoTab.searchQuery = (val || '').toLowerCase().trim();
  renderCaiTaoTeams();
}

function renderCaiTaoTeams() {
  const grid = document.getElementById('cai-tao-teams-grid');
  const countEl = document.getElementById('cai-tao-count');
  if (!grid) return;

  const { section, searchQuery } = AppState.caiTaoTab;
  let filtered = _caiTaoData || [];

  if (section !== 'All') {
    filtered = filtered.filter(t => t.section === section);
  }

  if (searchQuery) {
    filtered = filtered.filter(t => {
      const matchTrp = (t.troop || '').toLowerCase().includes(searchQuery);
      const matchNote = (t.note || '').toLowerCase().includes(searchQuery);
      const matchGen = (t.generals || []).some(g => (g.name || g.raw_name || '').toLowerCase().includes(searchQuery));
      const matchTac = (t.generals || []).some(g => [g.cp1, g.cp2].some(c => (c || '').toLowerCase().includes(searchQuery)));
      return matchTrp || matchNote || matchGen || matchTac;
    });
  }

  if (countEl) countEl.textContent = filtered.length;

  const TROOP_ICON = { 'Thương': '🔱', 'Kỵ': '🐎', 'Cung': '🏹', 'Khiên': '🛡', 'Khí': '💨' };

  if (filtered.length === 0) {
    grid.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted);grid-column:1/-1">Không tìm thấy đội hình cải tạo nào phù hợp.</div>';
    return;
  }

  grid.innerHTML = filtered.map((team, idx) => {
    const isDangUng = team.section === 'Lệnh Đăng Ung';
    const troop = team.troop || 'Kỵ';
    const icon = TROOP_ICON[troop] || '⚔️';
    const note = team.note || '';

    const gensHtml = (team.generals || []).map((g, gi) => {
      const gName = g.raw_name || g.name || '';
      const cp1 = g.cp1 || '';
      const cp2 = g.cp2 || '';
      const bt = (g.binh_thu || []).filter(b => b);
      const pos = gi === 0 ? 'Chủ tướng' : `Phó tướng ${gi}`;
      const posClass = gi === 0 ? 'pos-main' : 'pos-sub';

      const tacticsHtml = [cp1, cp2].filter(Boolean).map(t =>
        `<span class="tactic-pill">${t}</span>`
      ).join('');

      const btHtml = bt.length > 0
        ? `<div class="binh-thu-row">${bt.map((b, bi) => `<span class="binh-thu-pill ${bi === 0 ? 'main-tome' : 'sub-tome'}">${bi === 0 ? '★ ' : ''}${b}</span>`).join('')}</div>`
        : '';

      return `
        <div class="general-slot ${posClass}">
          <div class="gen-header">
            <span class="gen-pos-badge ${posClass}">${pos}</span>
            <span class="gen-name" style="font-size:13px;font-weight:700">${gName}</span>
          </div>
          <div class="gen-tactics">${tacticsHtml}</div>
          ${btHtml}
        </div>`;
    }).join('');

    const noteHtml = note ? `
      <div class="team-note-block" style="margin-top:12px;padding:8px 12px;background:${isDangUng ? 'rgba(245,158,11,0.08)' : 'rgba(14,165,233,0.08)'};border-left:3px solid ${isDangUng ? '#f59e0b' : '#0ea5e9'};border-radius:6px;font-size:12px;color:var(--text-muted)">
        💡 <strong>Ý tưởng:</strong> ${note}
      </div>` : '';

    return `
      <div class="team-card cai-tao-card ${isDangUng ? 'section-dang-ung' : ''}">
        <div class="team-card-header">
          <div class="team-badge-group">
            <span class="troop-badge" style="background:${isDangUng ? 'rgba(245,158,11,0.15)' : 'rgba(14,165,233,0.15)'};color:${isDangUng ? '#fbbf24' : '#38bdf8'};border:1px solid ${isDangUng ? 'rgba(245,158,11,0.3)' : 'rgba(14,165,233,0.3)'}">${icon} ${troop}</span>
            <span class="tier-badge" style="background:${isDangUng ? 'rgba(245,158,11,0.2)' : 'rgba(14,165,233,0.2)'};color:${isDangUng ? '#fde68a' : '#bae6fd'}">${team.section}</span>
          </div>
          <span class="team-number" style="color:${isDangUng ? '#f59e0b' : '#0ea5e9'}">#${idx + 1}</span>
        </div>
        <div class="team-generals">
          ${gensHtml}
        </div>
        ${noteHtml}
      </div>`;
  }).join('');
}

// ==========================================================
// ĐỘI HÌNH CÙNG TỒN (COEXISTING PORTFOLIOS) — FETCH & RENDER
// ==========================================================

let _cungTonData = [];
let _activePortfolioIdx = 0;

async function fetchCungTon() {
  const container = document.getElementById('cung-ton-teams-container');
  if (!container) return;
  container.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted)">⏳ Đang tải dữ liệu Đội Hình Cùng Tồn...</div>';
  try {
    const resp = await fetch('/api/coexisting-portfolios');
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    _cungTonData = await resp.json();
    renderCungTonPortfolios();
  } catch (e) {
    container.innerHTML = `<div style="text-align:center;padding:40px;color:#f87171">❌ Lỗi tải dữ liệu Đội Hình Cùng Tồn: ${e.message}</div>`;
  }
}

function selectCungTonSet(idx) {
  _activePortfolioIdx = idx;
  renderCungTonPortfolios();
}

function renderCungTonPortfolios() {
  const bar = document.getElementById('cung-ton-sets-bar');
  const infoEl = document.getElementById('cung-ton-set-info');
  const container = document.getElementById('cung-ton-teams-container');
  if (!container) return;

  if (!_cungTonData || _cungTonData.length === 0) {
    container.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted)">Không có dữ liệu Đội Hình Cùng Tồn.</div>';
    return;
  }

  // Render buttons
  if (bar) {
    bar.innerHTML = _cungTonData.map((p, idx) => {
      const isAct = idx === _activePortfolioIdx;
      const tCount = (p.teams || []).length;
      return `
        <button class="portfolio-set-btn ${isAct ? 'active' : ''}" onclick="selectCungTonSet(${idx})">
          ${p.set_name} (${tCount} Đội)
        </button>
      `;
    }).join('');
  }

  const p = _cungTonData[_activePortfolioIdx] || _cungTonData[0];
  if (!p) return;

  // Render info banner
  if (infoEl) {
    const starterHtml = p.starter_recommendation ? `
      <div class="cung-ton-starter-banner">
        <div class="cung-ton-starter-title">
          <span>🌱 TIẾN CỬ ĐỘI HÌNH KHAI HOANG CHO BỘ NÀY (EXCEL):</span>
        </div>
        <div class="cung-ton-starter-content">${p.starter_recommendation}</div>
      </div>
    ` : '';

    infoEl.innerHTML = `
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:14px 18px;margin-bottom:14px">
        <h3 style="font-size:16px;color:#10b981;margin-bottom:6px">⚜️ ${p.set_name}</h3>
        ${p.description ? `<p style="font-size:13px;color:var(--text-muted);margin-bottom:8px">${p.description}</p>` : ''}
        <div style="font-size:12px;color:var(--text-dim)">Gồm <strong>${(p.teams || []).length} đội hình</strong> phối hợp xuất chiến không trùng chiến pháp, phát huy tối đa sức mạnh liên minh.</div>
      </div>
      ${starterHtml}
    `;
  }

  // Render teams in this portfolio
  const teams = p.teams || [];
  if (teams.length === 0) {
    container.innerHTML = '<div style="text-align:center;padding:30px;color:var(--text-muted)">Bộ này chưa có thông tin chi tiết các đội.</div>';
    return;
  }

  container.innerHTML = `
    <div class="cung-ton-teams-grid">
      ${teams.map((t, tidx) => {
        const gens = t.generals || [];
        const tName = t.team_name || `Đội ${tidx + 1}`;
        const cost = t.cost || '';

        return `
          <div class="cung-ton-team-card">
            <div class="cung-ton-card-header">
              <div>
                <span class="cung-ton-team-title">${tName}</span>
                ${cost ? `<span class="meta-pill" style="margin-left:8px;background:rgba(16,185,129,0.15);color:#34d399;font-size:11px">${cost}</span>` : ''}
              </div>
              <span style="font-size:12px;font-weight:700;color:#10b981">Team #${tidx + 1}</span>
            </div>

            <div class="generals-lineup" style="display:flex;flex-direction:column;gap:10px">
              ${gens.map((g, gi) => {
                const pos = gi === 0 ? 'Chủ tướng' : `Phó tướng ${gi}`;
                const posClass = gi === 0 ? 'pos-main' : 'pos-sub';
                const gName = g.raw_name || g.name || '';
                const t1 = g.tactic1 || '';
                const t2 = g.tactic2 || '';
                const stat = g.stat_point || '';
                const bt = (g.binh_thu || []).filter(Boolean);

                return `
                  <div class="general-slot ${posClass}" style="padding:10px">
                    <div class="gen-header" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                      <div>
                        <span class="gen-pos-badge ${posClass}" style="font-size:10px">${pos}</span>
                        <strong style="font-size:13.5px;color:#f3f4f6;margin-left:6px">${gName}</strong>
                      </div>
                      ${stat ? `<span class="stat-point-pill">🎯 ${stat}</span>` : ''}
                    </div>

                    <div class="gen-tactics" style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:6px">
                      ${t1 ? `<span class="tactic-pill">${t1}</span>` : ''}
                      ${t2 ? `<span class="tactic-pill">${t2}</span>` : ''}
                    </div>

                    ${bt.length > 0 ? `
                      <div class="binh-thu-row" style="margin-top:4px">
                        ${bt.map((b, bi) => `<span class="binh-thu-pill ${bi === 0 ? 'main-tome' : 'sub-tome'}">${bi === 0 ? '★ ' : ''}${b}</span>`).join('')}
                      </div>
                    ` : ''}
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

window.fetchCaiTao = fetchCaiTao;
window.filterCaiTaoSection = filterCaiTaoSection;
window.filterCaiTaoSearch = filterCaiTaoSearch;
window.renderCaiTaoTeams = renderCaiTaoTeams;
window.fetchCungTon = fetchCungTon;
window.selectCungTonSet = selectCungTonSet;
window.renderCungTonPortfolios = renderCungTonPortfolios;
window.fetchDoUy = fetchDoUy;
window.renderDoUyTeams = renderDoUyTeams;

window.app = Object.assign(window.app || {}, {
  fetchCaiTao,
  filterCaiTaoSection,
  filterCaiTaoSearch,
  renderCaiTaoTeams,
  fetchCungTon,
  selectCungTonSet,
  renderCungTonPortfolios,
  fetchDoUy,
  renderDoUyTeams
});


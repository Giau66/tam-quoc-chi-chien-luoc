/* =========================================================
   auth.js — Login / Register / Cloud Save
   ========================================================= */

const API = '';  // Same-origin

// ── Token helpers ────────────────────────────────────────
const AuthStore = {
  getToken: () => localStorage.getItem('tqc_token'),
  setToken: (t) => localStorage.setItem('tqc_token', t),
  removeToken: () => localStorage.removeItem('tqc_token'),
  getUser: () => {
    try { return JSON.parse(localStorage.getItem('tqc_user') || 'null'); }
    catch { return null; }
  },
  setUser: (u) => localStorage.setItem('tqc_user', JSON.stringify(u)),
  removeUser: () => localStorage.removeItem('tqc_user'),
  isLoggedIn: () => !!localStorage.getItem('tqc_token'),
};

// ── API helpers ──────────────────────────────────────────
async function apiPost(endpoint, body, auth = false) {
  const headers = { 'Content-Type': 'application/json' };
  if (auth) headers['Authorization'] = `Bearer ${AuthStore.getToken()}`;
  const res = await fetch(`${API}${endpoint}`, {
    method: 'POST',
    headers,
    body: JSON.stringify(body)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Lỗi không xác định');
  return data;
}

async function apiGet(endpoint, auth = false) {
  const headers = {};
  if (auth) headers['Authorization'] = `Bearer ${AuthStore.getToken()}`;
  const res = await fetch(`${API}${endpoint}`, { headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Lỗi không xác định');
  return data;
}

// ── Auth Actions ─────────────────────────────────────────
async function doRegister(username, email, password, displayName = '') {
  const data = await apiPost('/api/auth/register', { username, email, password, display_name: displayName });
  AuthStore.setToken(data.token);
  AuthStore.setUser(data.user);
  showToast('success', '🎉 Chào mừng!', `Tài khoản ${data.user.display_name || username} đã tạo thành công!`);
  onLoginSuccess(data.user);
  return data;
}

async function doLogin(email, password) {
  const data = await apiPost('/api/auth/login', { email, password });
  AuthStore.setToken(data.token);
  AuthStore.setUser(data.user);
  showToast('success', '✅ Đăng nhập thành công!', `Chào mừng ${data.user.display_name || data.user.username}!`);
  onLoginSuccess(data.user);
  return data;
}

function doLogout() {
  AuthStore.removeToken();
  AuthStore.removeUser();
  renderNavAuth();
  showToast('info', '👋 Đã đăng xuất', 'Hẹn gặp lại Chủ Công!');
  setTimeout(() => { window.location.href = '/'; }, 800);
}

async function fetchCurrentUser() {
  if (!AuthStore.isLoggedIn()) return null;
  try {
    const data = await apiGet('/api/auth/me', true);
    AuthStore.setUser(data);
    return data;
  } catch {
    AuthStore.removeToken();
    AuthStore.removeUser();
    return null;
  }
}

// ── Cloud Inventory Sync ──────────────────────────────────
async function syncInventoryFromCloud() {
  if (!AuthStore.isLoggedIn()) return null;
  try {
    const data = await apiGet('/api/user/inventory', true);
    if (data.owned_generals && data.owned_generals.length > 0) {
      localStorage.setItem('tqc_generals', JSON.stringify(data.owned_generals));
    }
    if (data.owned_tactics && data.owned_tactics.length > 0) {
      localStorage.setItem('tqc_tactics', JSON.stringify(data.owned_tactics));
    }
    console.log(`[Cloud] Synced: ${data.owned_generals?.length || 0} generals, ${data.owned_tactics?.length || 0} tactics`);
    return data;
  } catch (e) {
    console.warn('[Cloud] Sync failed:', e.message);
    return null;
  }
}

async function saveInventoryToCloud(generals, tactics) {
  if (!AuthStore.isLoggedIn()) return;
  try {
    await apiPost('/api/user/inventory', { owned_generals: generals, owned_tactics: tactics }, true);
    console.log('[Cloud] Saved inventory to cloud');
  } catch (e) {
    console.warn('[Cloud] Save failed:', e.message);
  }
}

// ── Callback hook ─────────────────────────────────────────
function onLoginSuccess(user) {
  renderNavAuth(user);
  closeAuthModal();
  // Auto-sync inventory after login
  syncInventoryFromCloud().then(() => {
    if (typeof window.onCloudSynced === 'function') window.onCloudSynced();
  });
}

// ── NAVBAR RENDERING ─────────────────────────────────────
function renderNavAuth(user) {
  const authEl = document.getElementById('nav-auth-section');
  if (!authEl) return;

  const u = user || AuthStore.getUser();
  if (u) {
    const initial = (u.display_name || u.username || '?').charAt(0).toUpperCase();
    authEl.innerHTML = `
      <div class="nav-user" id="nav-user-btn" onclick="toggleUserDropdown(this)">
        <div class="nav-avatar" style="background:${u.avatar_color || '#f59e0b'}">${initial}</div>
        <span class="nav-username">${u.display_name || u.username}</span>
        <span class="nav-chevron">▾</span>
        <div class="nav-dropdown">
          <div class="nav-dropdown-item" style="pointer-events:none;opacity:.5;font-size:11px;padding:6px 12px;">
            ☁️ Cloud Save kho đồ
          </div>
          <a href="/tools.html" class="nav-dropdown-item">🛠️ Công Cụ</a>
          <div class="nav-dropdown-divider"></div>
          <div class="nav-dropdown-item danger" onclick="doLogout()">🚪 Đăng Xuất</div>
        </div>
      </div>`;
  } else {
    authEl.innerHTML = `
      <button class="nav-btn-login" onclick="openAuthModal('login')">Đăng Nhập</button>
      <button class="nav-btn-register" onclick="openAuthModal('register')">Đăng Ký</button>`;
  }
}

function toggleUserDropdown(el) {
  el.classList.toggle('open');
  // Close on outside click
  const handler = (e) => {
    if (!el.contains(e.target)) {
      el.classList.remove('open');
      document.removeEventListener('click', handler);
    }
  };
  setTimeout(() => document.addEventListener('click', handler), 10);
}

// ── AUTH MODAL ────────────────────────────────────────────
function openAuthModal(tab = 'login') {
  const overlay = document.getElementById('auth-overlay');
  if (!overlay) return;
  overlay.classList.add('active');
  switchAuthTab(tab);
  // Focus first input
  setTimeout(() => {
    const first = overlay.querySelector('.auth-form.active input');
    if (first) first.focus();
  }, 300);
}

function closeAuthModal() {
  const overlay = document.getElementById('auth-overlay');
  if (overlay) overlay.classList.remove('active');
  clearAuthMessages();
}

function switchAuthTab(tab) {
  document.querySelectorAll('.auth-tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tab);
  });
  document.querySelectorAll('.auth-form').forEach(f => {
    f.classList.toggle('active', f.id === `auth-form-${tab}`);
  });
  clearAuthMessages();
}

function clearAuthMessages() {
  document.querySelectorAll('.auth-message').forEach(m => {
    m.className = 'auth-message';
    m.textContent = '';
  });
}

function showAuthMsg(formId, type, msg) {
  const el = document.querySelector(`#${formId} .auth-message`);
  if (!el) return;
  el.className = `auth-message ${type}`;
  el.textContent = msg;
}

// ── FORM HANDLERS ─────────────────────────────────────────
async function handleRegisterSubmit(e) {
  e.preventDefault();
  const form = e.target;
  const btn = form.querySelector('.auth-submit-btn');
  const username = form.querySelector('[name="username"]').value.trim();
  const email    = form.querySelector('[name="email"]').value.trim();
  const password = form.querySelector('[name="password"]').value;
  const dispName = form.querySelector('[name="display_name"]')?.value.trim() || '';

  if (!username || !email || !password) {
    return showAuthMsg('auth-form-register', 'error', 'Vui lòng điền đầy đủ thông tin.');
  }

  btn.disabled = true;
  btn.textContent = 'Đang tạo tài khoản...';
  try {
    await doRegister(username, email, password, dispName || username);
  } catch (err) {
    showAuthMsg('auth-form-register', 'error', err.message);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Tạo Tài Khoản';
  }
}

async function handleLoginSubmit(e) {
  e.preventDefault();
  const form = e.target;
  const btn  = form.querySelector('.auth-submit-btn');
  const email    = form.querySelector('[name="email"]').value.trim();
  const password = form.querySelector('[name="password"]').value;

  if (!email || !password) {
    return showAuthMsg('auth-form-login', 'error', 'Vui lòng nhập email và mật khẩu.');
  }

  btn.disabled = true;
  btn.textContent = 'Đang đăng nhập...';
  try {
    await doLogin(email, password);
  } catch (err) {
    showAuthMsg('auth-form-login', 'error', err.message);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Đăng Nhập';
  }
}

// ── TOAST ─────────────────────────────────────────────────
function showToast(type, title, msg) {
  let toast = document.getElementById('auth-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'auth-toast';
    toast.className = 'auth-toast';
    toast.innerHTML = `<div class="toast-icon"></div><div class="toast-body"><div class="toast-title"></div><div class="toast-msg"></div></div>`;
    document.body.appendChild(toast);
  }
  const icons = { success: '✅', error: '❌', info: '💬', warning: '⚠️' };
  toast.querySelector('.toast-icon').textContent = icons[type] || '💬';
  toast.querySelector('.toast-title').textContent = title;
  toast.querySelector('.toast-msg').textContent = msg;
  toast.className = `auth-toast toast-${type}`;
  setTimeout(() => toast.classList.add('show'), 10);
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove('show'), 3500);
}

// ── INIT ──────────────────────────────────────────────────
function initAuth() {
  // Render initial auth state in navbar
  renderNavAuth();

  // Close modal on overlay click
  document.addEventListener('click', (e) => {
    if (e.target.id === 'auth-overlay') closeAuthModal();
  });

  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeAuthModal();
  });

  // Form submit
  const loginForm = document.getElementById('auth-form-login');
  const regForm   = document.getElementById('auth-form-register');
  if (loginForm) loginForm.addEventListener('submit', handleLoginSubmit);
  if (regForm)   regForm.addEventListener('submit', handleRegisterSubmit);

  // If token exists, verify it's still valid
  if (AuthStore.isLoggedIn()) {
    fetchCurrentUser().then(u => {
      if (u) renderNavAuth(u);
    });
  }
}

document.addEventListener('DOMContentLoaded', initAuth);

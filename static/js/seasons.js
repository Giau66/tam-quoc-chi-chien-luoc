/* =========================================================
   seasons.js — Seasons Page Logic
   ========================================================= */

const SEASONS_API = '/api/seasons';

let seasonData = {};        // { pk20: {...}, mua5: {...}, mua4: {...} }
let currentSeason = 'pk20';
let lightboxImages = [];
let lightboxIndex  = 0;

// ── Init ─────────────────────────────────────────────────
async function initSeasonsPage() {
  try {
    const seasons = await (await fetch(SEASONS_API)).json();

    // Fetch full data for each season
    for (const s of seasons) {
      const detail = await (await fetch(`${SEASONS_API}/${s.id}`)).json();
      seasonData[s.id] = detail;
    }

    buildSeasonTabs(seasons);
    openSeason(seasons[0]?.id || 'pk20');
  } catch (e) {
    console.error('Failed to load seasons:', e);
  }
}

// ── Season Tabs ────────────────────────────────────────────
function buildSeasonTabs(seasons) {
  const container = document.getElementById('season-tabs');
  if (!container) return;
  container.innerHTML = '';

  seasons.forEach(s => {
    const btn = document.createElement('button');
    btn.className = 'season-tab';
    btn.dataset.season = s.id;
    const isNew = s.is_current;

    let badgeText = '';
    if (s.image_count > 0) {
      badgeText = `${s.image_count} ảnh`;
    } else if (s.meta_teams && s.meta_teams.length > 0) {
      badgeText = `${s.meta_teams.length} đội`;
    } else if (s.intro_teams && s.intro_teams.length > 0) {
      badgeText = `${s.intro_teams.length} đội`;
    }

    btn.innerHTML = `
      ${isNew ? '<span style="width:7px;height:7px;border-radius:50%;background:#10b981;display:inline-block;animation:pulse-green 1.5s infinite"></span>' : ''}
      ${s.short_name}
      ${badgeText ? `<span class="season-tab-badge">${badgeText}</span>` : ''}`;
    btn.addEventListener('click', () => openSeason(s.id));
    container.appendChild(btn);
  });
}

// ── Open Season ────────────────────────────────────────────
function openSeason(seasonId) {
  currentSeason = seasonId;
  const data = seasonData[seasonId];
  if (!data) return;

  // Update tabs
  document.querySelectorAll('.season-tab').forEach(t => {
    t.classList.toggle('active', t.dataset.season === seasonId);
  });

  // Show content panel
  document.querySelectorAll('.season-content').forEach(c => {
    c.classList.toggle('active', c.id === `season-${seasonId}`);
  });

  // Render the content
  renderSeasonContent(seasonId, data);
}

// ── Render Season Content ──────────────────────────────────
function renderSeasonContent(seasonId, data) {
  const panel = document.getElementById(`season-${seasonId}`);
  if (!panel) return;

  // Hero banner
  renderSeasonBanner(panel, data);

  // PK20 specific: new generals
  if (data.new_generals?.length > 0) {
    renderNewGenerals(panel, data.new_generals);
  }

  // Image gallery (PK20 has images)
  if (data.images?.length > 0) {
    renderGallery(panel, data.images);
  }

  // Teams
  const teams = data.intro_teams || data.meta_teams || [];
  if (teams.length > 0) {
    renderTeamList(panel, teams, data.douy_teams || []);
  }
}

// ── Banner ─────────────────────────────────────────────────
function renderSeasonBanner(panel, data) {
  const el = panel.querySelector('.season-hero-banner');
  if (!el) return;
  const imgCount = data.images?.length || 0;
  const teamCount = (data.intro_teams?.length || 0) + (data.meta_teams?.length || 0);
  const genCount  = data.new_generals?.length || 0;

  el.innerHTML = `
    <div>
      ${data.is_current ? '<div class="season-current-badge">🔥 Mùa Hiện Tại</div>' : ''}
      <h1 class="season-banner-title">${data.name}</h1>
      <p class="season-banner-desc">${data.description || ''}</p>
    </div>
    <div class="season-banner-stats">
      ${imgCount > 0 ? `<div class="season-banner-stat"><span class="season-banner-stat-num">${imgCount}</span><span class="season-banner-stat-label">Ảnh Đội Hình</span></div>` : ''}
      ${teamCount > 0 ? `<div class="season-banner-stat"><span class="season-banner-stat-num">${teamCount}</span><span class="season-banner-stat-label">Đội Hình</span></div>` : ''}
      ${genCount > 0 ? `<div class="season-banner-stat"><span class="season-banner-stat-num">${genCount}</span><span class="season-banner-stat-label">Tướng Mới</span></div>` : ''}
    </div>`;
}

// ── New Generals ───────────────────────────────────────────
function renderNewGenerals(panel, generals) {
  const el = panel.querySelector('.new-generals-grid');
  if (!el) return;
  el.innerHTML = generals.map(g => `
    <div class="new-gen-card">
      <div class="new-gen-name">⭐ ${g.name}</div>
      <div class="new-gen-skill">${g.skill || ''}</div>
      ${g.inherit_tactic ? `<span class="new-gen-inherit">📖 ${g.inherit_tactic}</span>` : ''}
      ${g.role ? `<div style="margin-top:6px;font-size:11px;color:#6b7280">${g.role}</div>` : ''}
    </div>`).join('');
}

// ── Gallery ────────────────────────────────────────────────
function renderGallery(panel, images) {
  const el = panel.querySelector('.gallery-items-grid');
  if (!el) return;

  lightboxImages = images;

  el.innerHTML = images.map((img, i) => `
    <div class="gallery-item" onclick="openLightbox(${i})" title="Xem ảnh đội hình">
      <img src="/hinh/${img}" alt="Đội hình ${i+1}" loading="lazy"
           onerror="this.parentElement.style.display='none'">
      <div class="gallery-item-overlay">
        <span class="gallery-zoom-icon">🔍</span>
      </div>
    </div>`).join('');

  const countEl = panel.querySelector('.gallery-count');
  if (countEl) countEl.textContent = `${images.length} ảnh`;

  // Search/filter
  const searchEl = panel.querySelector('.gallery-search');
  if (searchEl) {
    searchEl.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase();
      el.querySelectorAll('.gallery-item').forEach((item, i) => {
        item.style.display = (q === '' || images[i].toLowerCase().includes(q)) ? '' : 'none';
      });
    });
  }
}

// ── Teams ──────────────────────────────────────────────────
function showTeamList(seasonId, listType) {
  const panel = document.getElementById(`season-${seasonId}`);
  if (!panel) return;
  const el = panel.querySelector('.team-list-container');
  if (!el) return;
  const data = seasonData[seasonId];
  if (!data) return;

  if (listType === 'douy') {
    renderTeams(el, data.douy_teams || []);
  } else if (listType === 'intro') {
    renderTeams(el, data.intro_teams || data.meta_teams || []);
  } else {
    renderTeams(el, data.meta_teams || data.intro_teams || []);
  }
}

function renderTeamList(panel, introTeams, douyTeams) {
  const el = panel.querySelector('.team-list-container');
  if (!el) return;

  // Render initial list according to active sub-tab
  const activeSubTab = panel.querySelector('.team-sub-tab.active');
  const activeType = activeSubTab ? activeSubTab.dataset.listType : 'intro';
  if (activeType === 'douy') {
    renderTeams(el, douyTeams);
  } else {
    renderTeams(el, introTeams);
  }

  // Wire sub-tab buttons if they exist
  panel.querySelectorAll('.team-sub-tab').forEach(btn => {
    btn.onclick = () => {
      panel.querySelectorAll('.team-sub-tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      showTeamList(currentSeason, btn.dataset.listType);
    };
  });
}

function renderTeams(container, teams) {
  if (!teams || teams.length === 0) {
    container.innerHTML = '<p style="color:#6b7280;text-align:center;padding:40px">Không có dữ liệu đội hình cho mùa này.</p>';
    return;
  }

  const troopIcons = { Kỵ: '🐴', Thương: '🗡️', Khiên: '🛡️', Cung: '🏹', Khí: '💨' };
  const troopClass = { Kỵ: 'ky', Thương: 'thu', Khiên: 'cui', Cung: 'khu', Khí: 'khi' };

  container.innerHTML = `<div class="team-list-grid">` + teams.map(team => {
    const generals = team.generals || [];
    const tierClass = (team.tier || 'T1').replace('.', '');
    return `
      <div class="season-team-card">
        <div class="season-team-header">
          <div class="season-team-troop troop-${troopClass[team.troop] || 'ky'}">
            ${troopIcons[team.troop] || '⚔️'}
          </div>
          <div class="season-team-name">${team.name || team.troop}</div>
          <span class="tier-badge tier-${tierClass}">${team.tier || 'T1'}</span>
        </div>
        <div class="season-team-generals">
          ${generals.map(g => `
            <div class="season-gen-row">
              <div class="season-gen-name">${g.name}</div>
              <div class="season-gen-tactics">
                ${g.cp1 ? `<span class="tactic-chip">${g.cp1}</span>` : ''}
                ${g.cp2 ? `<span class="tactic-chip">${g.cp2}</span>` : ''}
                ${(g.bis_tactics || []).map(t => `<span class="tactic-chip">${t}</span>`).join('')}
              </div>
            </div>`).join('')}
        </div>
        ${team.note ? `<div class="season-team-note">💡 ${team.note.substring(0, 200)}${team.note.length > 200 ? '...' : ''}</div>` : ''}
      </div>`;
  }).join('') + `</div>`;
}

// ── Lightbox ───────────────────────────────────────────────
function openLightbox(index) {
  lightboxIndex = index;
  const lb = document.getElementById('lightbox');
  if (!lb) return;
  lb.classList.add('open');
  updateLightboxImg();

  // Keyboard nav in lightbox
  document._lbHandler = (e) => {
    if (e.key === 'ArrowRight') nextLightbox();
    if (e.key === 'ArrowLeft')  prevLightbox();
    if (e.key === 'Escape')     closeLightbox();
  };
  document.addEventListener('keydown', document._lbHandler);
}

function closeLightbox() {
  document.getElementById('lightbox')?.classList.remove('open');
  document.removeEventListener('keydown', document._lbHandler);
}

function nextLightbox() {
  lightboxIndex = (lightboxIndex + 1) % lightboxImages.length;
  updateLightboxImg();
}

function prevLightbox() {
  lightboxIndex = (lightboxIndex - 1 + lightboxImages.length) % lightboxImages.length;
  updateLightboxImg();
}

function updateLightboxImg() {
  const img = document.getElementById('lightbox-img');
  const counter = document.getElementById('lightbox-counter');
  if (img) {
    img.src = `/hinh/${lightboxImages[lightboxIndex]}`;
    img.alt = `Đội hình ${lightboxIndex + 1}`;
  }
  if (counter) counter.textContent = `${lightboxIndex + 1} / ${lightboxImages.length}`;
}

// Expose globals
window.openLightbox = openLightbox;
window.closeLightbox = closeLightbox;
window.nextLightbox = nextLightbox;
window.prevLightbox = prevLightbox;
window.showTeamList = showTeamList;

document.addEventListener('DOMContentLoaded', initSeasonsPage);

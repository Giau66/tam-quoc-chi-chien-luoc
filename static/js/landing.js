/* =========================================================
   landing.js — Fullscreen Scroll + Hero Animations
   ========================================================= */

(function () {
  'use strict';

  let currentSection = 0;
  let isScrolling    = false;
  const TRANSITION_DURATION = 900; // ms - must match CSS transition

  const sections = [];
  const dots     = [];

  const sectionIds = ['#section-home', '#section-tuong', '#section-chienphap', '#section-doihinh'];

  // ── Init Sections ─────────────────────────────────────────
  function init() {
    const sectionEls = document.querySelectorAll('.fs-section');
    sectionEls.forEach((el, i) => {
      sections.push(el);
      if (i === 0) el.classList.add('is-current');
      else         el.classList.add('is-below');
    });

    buildDotNav(sectionEls);
    initNavClicks();
    initParticles();
    initScrollEvents();
    initTouchEvents();
    initKeyboardEvents();
    updateDots();
    updateNavLinks();
    checkInitialHash();
  }

  // ── Build dot navigator ────────────────────────────────────
  function buildDotNav(sectionEls) {
    const nav = document.getElementById('dot-nav');
    if (!nav) return;
    const labels = ['Trang Chủ', 'Tướng', 'Chiến Pháp', 'Đội Hình'];
    sectionEls.forEach((_, i) => {
      const dot = document.createElement('div');
      dot.className = 'dot-nav-item';
      dot.setAttribute('data-tooltip', labels[i] || `Mục ${i + 1}`);
      dot.addEventListener('click', () => goToSection(i));
      nav.appendChild(dot);
      dots.push(dot);
    });
  }

  // ── Update Navbar links ───────────────────────────────────
  function updateNavLinks() {
    const navLinks = document.querySelectorAll('.site-navbar .nav-link[data-section]');
    navLinks.forEach((link) => {
      const idx = parseInt(link.getAttribute('data-section'), 10);
      link.classList.toggle('active', idx === currentSection);
    });
  }

  // ── Click to navigate section from navbar ──────────────────
  function initNavClicks() {
    const navLinks = document.querySelectorAll('.site-navbar .nav-link[data-section]');
    navLinks.forEach((link) => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetIdx = parseInt(link.getAttribute('data-section'), 10);
        if (!isNaN(targetIdx)) {
          goToSection(targetIdx);
        }
      });
    });
  }

  // ── Check Hash on load ─────────────────────────────────────
  function checkInitialHash() {
    const hashMap = {
      '#section-home': 0,
      '#section-tuong': 1,
      '#section-chienphap': 2,
      '#section-doihinh': 3
    };
    if (window.location.hash && hashMap[window.location.hash] !== undefined) {
      setTimeout(() => goToSection(hashMap[window.location.hash]), 80);
    }
  }

  // ── Go to section ─────────────────────────────────────────
  function goToSection(index) {
    if (isScrolling || index === currentSection) return;
    if (index < 0 || index >= sections.length) return;

    isScrolling = true;
    currentSection = index;

    sections.forEach((s, i) => {
      s.classList.remove('is-above', 'is-current', 'is-below');
      if (i < currentSection)        s.classList.add('is-above');
      else if (i === currentSection) s.classList.add('is-current');
      else                           s.classList.add('is-below');
    });

    updateDots();
    updateNavLinks();

    if (history.replaceState && sectionIds[currentSection]) {
      history.replaceState(null, null, sectionIds[currentSection]);
    }

    setTimeout(() => {
      isScrolling = false;
    }, TRANSITION_DURATION);
  }

  // ── Update dot states ──────────────────────────────────────
  function updateDots() {
    dots.forEach((d, i) => d.classList.toggle('active', i === currentSection));
  }

  // ── Wheel scroll ───────────────────────────────────────────
  function initScrollEvents() {
    let wheelDelta = 0;
    let wheelTimer = null;

    window.addEventListener('wheel', (e) => {
      e.preventDefault();
      if (isScrolling) return;

      wheelDelta += e.deltaY;

      clearTimeout(wheelTimer);
      wheelTimer = setTimeout(() => {
        if (Math.abs(wheelDelta) > 30) {
          if (wheelDelta > 0) goToSection(currentSection + 1);
          else                goToSection(currentSection - 1);
        }
        wheelDelta = 0;
      }, 50);
    }, { passive: false });
  }

  // ── Touch swipe ────────────────────────────────────────────
  function initTouchEvents() {
    let startY = 0;
    let startTime = 0;

    window.addEventListener('touchstart', (e) => {
      startY    = e.touches[0].clientY;
      startTime = Date.now();
    }, { passive: true });

    window.addEventListener('touchend', (e) => {
      if (isScrolling) return;
      const deltaY  = startY - e.changedTouches[0].clientY;
      const elapsed = Date.now() - startTime;
      // Swipe: at least 50px in under 500ms
      if (Math.abs(deltaY) > 50 && elapsed < 500) {
        if (deltaY > 0) goToSection(currentSection + 1);
        else            goToSection(currentSection - 1);
      }
    }, { passive: true });
  }

  // ── Keyboard arrows ────────────────────────────────────────
  function initKeyboardEvents() {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown' || e.key === 'PageDown') { e.preventDefault(); goToSection(currentSection + 1); }
      if (e.key === 'ArrowUp'   || e.key === 'PageUp')   { e.preventDefault(); goToSection(currentSection - 1); }
    });
  }

  // ── Hero Particles ─────────────────────────────────────────
  function initParticles() {
    const container = document.querySelector('.hero-particles');
    if (!container) return;

    const count = 35;
    for (let i = 0; i < count; i++) {
      const p  = document.createElement('div');
      p.className = 'hero-particle';
      const size = Math.random() * 3 + 1;
      p.style.cssText = `
        width: ${size}px;
        height: ${size}px;
        left: ${Math.random() * 100}%;
        bottom: ${Math.random() * -20}%;
        animation-duration: ${Math.random() * 8 + 6}s;
        animation-delay: ${Math.random() * 6}s;
        opacity: ${Math.random() * 0.5 + 0.2};
      `;
      container.appendChild(p);
    }
  }

  // ── Faction Character Showcase (Wuthering Waves style) ────
  const FACTION_SHOWCASE = {
    wei: {
      name: 'NGỤY QUỐC',
      kanji: '魏',
      color: '#60a5fa',
      pill: '🔵 BÁ CHỦ TRUNG NGUYÊN',
      desc: 'Quy tụ những bậc kỳ tài mưu sâu kế hiểm, lấy kỷ luật thép và năng lực phòng ngự phản kích kiên cố để bình định thiên hạ. Sở hữu các chiến đội bền bỉ nhất mùa giải.',
      meta: '🏆 Meta T0: Thái Úy Khiên · Ngụy Kỵ',
      count: '⚔️ 28 Danh tướng 5⭐',
      generals: [
        { name: 'Tào Tháo', cost: 'C7', img: '/images/generals/tao_thao.png', role: 'Chủ Lực · Khiên S / Kỵ S', skill: 'Loạn Thế Gian Hùng' },
        { name: 'SP Bàng Đức', cost: 'C6', img: '/images/generals/sp_bang_duc.png', role: 'Khống Chế · Cung S', skill: 'Tử Chiến Quyết Liệt' },
        { name: 'Hứa Chử', cost: 'C6', img: '/images/generals/hua_chu.png', role: 'Bạo Kích · Thương S / Khiên S', skill: 'Hổ Si Trảo' },
        { name: 'Vương Dị', cost: 'C6', img: '/images/generals/vuong_di.png', role: 'Liên Kích · Cung S', skill: 'Bí Mật Khởi Nghĩa' },
        { name: 'Chân Cơ', cost: 'C6', img: '/images/generals/chan_co.png', role: 'Hồi Phục · Hỗ Trợ', skill: 'Lạc Thần Phú' },
        { name: 'Tào Thực', cost: 'C6', img: '/images/generals/tao_thuc.png', role: 'Nội Chính · Trợ Thủ', skill: 'Thất Bộ Thành Thi' },
        { name: 'Trần Quần', cost: 'C6', img: '/images/generals/tran_quan.png', role: 'Nội Chính · Mưu Lược', skill: 'Cửu Phẩm Trung Chính' }
      ]
    },
    shu: {
      name: 'THỤC QUỐC',
      kanji: '蜀',
      color: '#34d399',
      pill: '🟢 NGHĨA KHÍ TRỜI CAO',
      desc: 'Được dẫn dắt bởi tinh thần hiệp nghĩa và lòng trung kiên bất diệt. Tấn công vũ lực bùng nổ, khả năng liên chiêu sấm sét và hồi phục sinh lực dẻo dai.',
      meta: '🏆 Meta T0: Kỳ Lân Cung · Thục Thương',
      count: '⚔️ 29 Danh tướng 5⭐',
      generals: [
        { name: 'Lưu Bị', cost: 'C7', img: '/images/generals/luu_bi.png', role: 'Hồi Máu · Khiên S / Kỵ S', skill: 'Nhân Đức Hưng Hán' },
        { name: 'Quan Vũ', cost: 'C7', img: '/images/generals/quan_vu.png', role: 'Khống Chế · Kỵ S / Thương S', skill: 'Uy Chấn Hoa Hạ' },
        { name: 'Gia Cát Lượng', cost: 'C7', img: '/images/generals/gia_cat_luong.png', role: 'Áp Chế · Cung S / Thương S', skill: 'Thần Toán Kỳ Mưu' },
        { name: 'Mã Siêu', cost: 'C7', img: '/images/generals/ma_sieu.png', role: 'Bạo Sát · Kỵ S / Thương S', skill: 'Tố Mã Bách Kỵ' }
      ]
    },
    wu: {
      name: 'NGÔ QUỐC',
      kanji: '吴',
      color: '#f87171',
      pill: '🔴 HỎA THIÊU GIANG ĐÔNG',
      desc: 'Làm chủ sông nước và thế trận linh hoạt. Chiến thuật thiêu đốt liên hoàn, thủy binh kỵ binh thần tốc công kích liên tục gây hỗn loạn đội hình địch.',
      meta: '🏆 Meta T0.5: Ngô Đô Đốc · Hổ Thần Cung',
      count: '⚔️ 26 Danh tướng 5⭐',
      generals: [
        { name: 'Chu Du', cost: 'C7', img: '/images/generals/chu_du.jpg', role: 'Chủ Lực · Cung S / Đô Đốc', skill: 'Thần Hỏa Diệt Thế' },
        { name: 'Lục Tốn', cost: 'C7', img: '/images/generals/luc_ton.jpg', role: 'Hỏa Thiêu · Cung S / Thương S', skill: 'Hỏa Thiêu Liên Doanh' },
        { name: 'Trương Chiêu', cost: 'C7', img: '/images/generals/truong_chieu.png', role: 'Nội Chính · Giang Đông Lão Thần', skill: 'Kính Hiền Lễ Sĩ' }
      ]
    },
    qun: {
      name: 'QUẦN HÙNG',
      kanji: '群',
      color: '#c084fc',
      pill: '🟣 CHIẾN THẦN LOẠN THẾ',
      desc: 'Các thế lực kiêu hùng tự do tranh bá. Sở hữu sức mạnh bạo kích vũ lực khủng khiếp nhất và những chiến pháp kỳ dị khắc chế mọi meta.',
      meta: '🏆 Meta T1: Tam Thế Lữ · Quần Cung SP',
      count: '⚔️ 23 Danh tướng 5⭐',
      generals: [
        { name: 'Lữ Bố', cost: 'C7', img: '/images/generals/lu_bo.png', role: 'Vô Song · Kỵ S / Cung S', skill: 'Thiên Hạ Vô Song' },
        { name: 'Đổng Trác', cost: 'C7', img: '/images/generals/dong_trac.png', role: 'Phản Nghịch · Khiên S', skill: 'Nghịch Tặc Hút Máu' },
        { name: 'Mạnh Hoạch', cost: 'C7', img: '/images/generals/manh_hoach.png', role: 'Man Vương · Khiên S / Kỵ S', skill: 'Binh Giáp Kháng Độc' }
      ]
    }
  };

  let currentFaction = 'wei';

  function switchFactionShowcase(fKey) {
    const data = FACTION_SHOWCASE[fKey];
    if (!data) return;
    currentFaction = fKey;

    // Update nav buttons
    document.querySelectorAll('.faction-nav-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-faction') === fKey);
    });

    // Update info panel
    const wmEl = document.getElementById('faction-watermark');
    const pillEl = document.getElementById('faction-tag-pill');
    const titleEl = document.getElementById('faction-huge-title');
    const descEl = document.getElementById('faction-story-desc');
    const metaEl = document.getElementById('faction-meta-badge');
    const countEl = document.getElementById('faction-count-badge');

    if (wmEl) wmEl.textContent = data.kanji;
    if (pillEl) { pillEl.textContent = data.pill; pillEl.style.borderColor = data.color; pillEl.style.color = data.color; }
    if (titleEl) { titleEl.textContent = data.name; }
    if (descEl) descEl.textContent = data.desc;
    if (metaEl) metaEl.textContent = data.meta;
    if (countEl) countEl.textContent = data.count;

    // Render cards
    const container = document.getElementById('cards-slider-container');
    if (container) {
      container.innerHTML = data.generals.map(g => `
        <div class="showcase-card" onclick="window.location='/tools.html#tab-inventory'" title="${g.name} - Bấm để xem chi tiết">
          <img src="${g.img}" alt="${g.name}" class="showcase-card-img" loading="lazy">
          <span class="showcase-card-cost">${g.cost}</span>
          <div class="showcase-card-overlay">
            <div class="showcase-card-stars">★★★★★</div>
            <div class="showcase-card-name">${g.name}</div>
            <div class="showcase-card-role">${g.role}</div>
            <div class="showcase-card-skill">⚡ ${g.skill}</div>
          </div>
        </div>
      `).join('');
      container.scrollLeft = 0;
      updateStageCounter(1, data.generals.length);
    }
  }

  function slideGenerals(dir) {
    const container = document.getElementById('cards-slider-container');
    if (!container) return;
    const cardWidth = 200;
    container.scrollBy({ left: dir * cardWidth, behavior: 'smooth' });
    setTimeout(() => {
      const data = FACTION_SHOWCASE[currentFaction];
      if (data) {
        const curIdx = Math.max(1, Math.min(Math.round(container.scrollLeft / cardWidth) + 1, data.generals.length));
        updateStageCounter(curIdx, data.generals.length);
      }
    }, 280);
  }

  function updateStageCounter(current, total) {
    const counterEl = document.getElementById('stage-counter');
    if (counterEl) counterEl.textContent = `${current} / ${total}`;
  }

  // ── Global Exports ─────────────────────────────────────────
  window.goToLastSection = () => goToSection(sections.length - 1);
  window.goToSection = goToSection;
  window.switchFactionShowcase = switchFactionShowcase;
  window.slideGenerals = slideGenerals;

  // ── Run on DOM ready ────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', () => {
    init();
    switchFactionShowcase('wei');
  });

  // ── Animate section elements on enter ─────────────────────
  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.querySelectorAll('[data-animate]').forEach((el, i) => {
          setTimeout(() => el.classList.add('anim-in'), i * 100);
        });
      }
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('.fs-section').forEach(s => sectionObserver.observe(s));

})();

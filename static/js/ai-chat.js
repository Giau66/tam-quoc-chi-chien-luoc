// ==========================================================================
// TAM QUOC CHI - AI CHAT & TEAM ANALYZER MODULE
// v3.0 - Gemini-powered tactical advisor
// ==========================================================================

// ─────────────────────────────────────────────────────────────────────────
// AI CHAT MODULE
// ─────────────────────────────────────────────────────────────────────────

const AIChat = {
  isLoading: false,
  messageCount: 0,

  getApiKey() {
    return AppState.apiKey || localStorage.getItem('tqc_gemini_api_key') || '';
  },

  init() {
    const notice = document.getElementById('ai-key-notice');
    if (notice) {
      // Hide notice if key is already saved
      if (this.getApiKey()) {
        notice.style.display = 'none';
      }
    }

    const input = document.getElementById('ai-question-input');
    if (input) {
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          sendAIMessage();
        }
        // Auto-grow textarea
        setTimeout(() => {
          input.style.height = 'auto';
          input.style.height = Math.min(input.scrollHeight, 120) + 'px';
        }, 0);
      });
    }
  },

  appendMessage(type, text) {
    const container = document.getElementById('ai-messages');
    if (!container) return;

    const div = document.createElement('div');
    div.className = `ai-msg ${type}-msg`;

    const icon = type === 'bot' ? '🤖' : '👤';
    // Convert plain text with newlines to paragraphs; bold **text**
    const htmlText = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .split('\n')
      .filter(l => l.trim())
      .map(l => `<p>${l}</p>`)
      .join('');

    div.innerHTML = `
      <div class="ai-msg-icon">${icon}</div>
      <div class="ai-msg-bubble">${htmlText || `<p>${text}</p>`}</div>
    `;

    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    this.messageCount++;
  },

  showTyping() {
    const container = document.getElementById('ai-messages');
    if (!container) return;
    const el = document.createElement('div');
    el.className = 'ai-msg bot-msg ai-typing-indicator';
    el.id = 'ai-typing';
    el.innerHTML = `
      <div class="ai-msg-icon">🤖</div>
      <div class="typing-dots"><span></span><span></span><span></span></div>
    `;
    container.appendChild(el);
    container.scrollTop = container.scrollHeight;
  },

  hideTyping() {
    const el = document.getElementById('ai-typing');
    if (el) el.remove();
  }
};

window.sendAIMessage = async function() {
  const input = document.getElementById('ai-question-input');
  const sendBtn = document.getElementById('ai-send-btn');
  if (!input || AIChat.isLoading) return;

  const question = input.value.trim();
  if (!question) return;

  const apiKey = AIChat.getApiKey();
  if (!apiKey) {
    AIChat.appendMessage('bot', '⚠️ Chưa có Gemini API Key. Hãy nhập key ở tab **Tải Ảnh** rồi lưu lại. Lấy key miễn phí tại: https://aistudio.google.com/app/apikey');
    return;
  }

  // Show user message
  AIChat.appendMessage('user', question);
  input.value = '';
  input.style.height = 'auto';

  // Show typing
  AIChat.isLoading = true;
  if (sendBtn) sendBtn.disabled = true;
  AIChat.showTyping();

  try {
    const resp = await fetch('/api/ai-chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question,
        owned_generals: Array.from(AppState.ownedGenerals),
        owned_tactics: Array.from(AppState.ownedTactics),
        gemini_api_key: apiKey
      })
    });

    AIChat.hideTyping();

    if (resp.ok) {
      const data = await resp.json();
      AIChat.appendMessage('bot', data.answer || 'Không có câu trả lời.');
    } else {
      const err = await resp.json();
      AIChat.appendMessage('bot', `❌ Lỗi: ${err.detail || 'Không kết nối được AI.'}`);
    }
  } catch (e) {
    AIChat.hideTyping();
    AIChat.appendMessage('bot', '❌ Không thể kết nối server. Vui lòng thử lại.');
  } finally {
    AIChat.isLoading = false;
    if (sendBtn) sendBtn.disabled = false;
  }
};

window.sendAIQuickQuestion = function(btn) {
  const input = document.getElementById('ai-question-input');
  if (input) {
    input.value = btn.textContent.trim().replace(/^[^\s]+\s/, '');
    sendAIMessage();
  }
};

// ─────────────────────────────────────────────────────────────────────────
// AI TEAM ANALYZER
// ─────────────────────────────────────────────────────────────────────────

window.openAnalyzeModal = async function(teamData) {
  const overlay = document.getElementById('ai-analyze-overlay');
  const loading = document.getElementById('ai-analyze-loading');
  const result = document.getElementById('ai-analysis-result');
  const titleEl = document.getElementById('ai-analyze-team-name');

  if (!overlay) return;

  const apiKey = AIChat.getApiKey();
  if (!apiKey) {
    showToolsToast('⚠️ Cần Gemini API Key để phân tích đội hình!', 'error');
    return;
  }

  // Show modal in loading state
  overlay.classList.add('open');
  loading.style.display = 'flex';
  result.style.display = 'none';
  if (titleEl) titleEl.textContent = teamData.team_name || 'Đội Hình';

  try {
    const resp = await fetch('/api/analyze-team', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...teamData,
        owned_generals: Array.from(AppState.ownedGenerals),
        owned_tactics: Array.from(AppState.ownedTactics),
        gemini_api_key: apiKey
      })
    });

    loading.style.display = 'none';

    if (resp.ok) {
      const data = await resp.json();
      // Format the analysis nicely
      let analysisHTML = data.analysis || 'Không có dữ liệu phân tích.';
      // Bold section headers by emoji
      analysisHTML = analysisHTML
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/(⚡[^\n]+)/g, '<strong style="color:#fbbf24">$1</strong>')
        .replace(/(⚠️[^\n]+)/g, '<strong style="color:#f87171">$1</strong>')
        .replace(/(🎯[^\n]+)/g, '<strong style="color:#34d399">$1</strong>')
        .replace(/(🔧[^\n]+)/g, '<strong style="color:#60a5fa">$1</strong>');

      result.innerHTML = analysisHTML;
      result.style.display = 'block';
    } else {
      const err = await resp.json();
      result.textContent = `❌ Lỗi: ${err.detail || 'Không phân tích được.'}`;
      result.style.display = 'block';
    }
  } catch (e) {
    loading.style.display = 'none';
    result.textContent = '❌ Không kết nối được server.';
    result.style.display = 'block';
  }
};

window.closeAnalyzeModal = function() {
  const overlay = document.getElementById('ai-analyze-overlay');
  if (overlay) overlay.classList.remove('open');
};

// Close modal on overlay click
document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('ai-analyze-overlay');
  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeAnalyzeModal();
    });
  }

  // Init AI chat
  AIChat.init();

  // Update key notice visibility when switching to ai-chat tab
  const origSwitchTab = window.switchTab;
  if (origSwitchTab) {
    window.switchTab = function(tabId) {
      origSwitchTab(tabId);
      if (tabId === 'tab-ai-chat') {
        const notice = document.getElementById('ai-key-notice');
        if (notice) {
          notice.style.display = AIChat.getApiKey() ? 'none' : 'flex';
        }
      }
    };
  }
});

// ─────────────────────────────────────────────────────────────────────────
// SMART RENDER HELPERS — extend app.js rendering with new smart score fields
// ─────────────────────────────────────────────────────────────────────────

/**
 * Build HTML for synergy/faction badges from evaluation result.
 */
window.buildSmartBadges = function(evalResult) {
  let html = '';
  if (!evalResult) return html;

  // Synergy bonus badge
  if (evalResult.synergy_bonus >= 6) {
    html += `<span class="synergy-badge">✨ Synergy +${evalResult.synergy_bonus}</span> `;
  }

  // Faction purity badge
  if (evalResult.is_pure_faction) {
    html += `<span class="faction-pure-badge">🌟 Thuần Phe</span> `;
  }

  return html;
};

/**
 * Build farm suggestions HTML for teams missing 1+ generals.
 */
window.buildFarmSuggestions = function(farmSuggestions) {
  if (!farmSuggestions || farmSuggestions.length === 0) return '';
  const tags = farmSuggestions.map(f => {
    const d = f.difficulty || 3;
    return `<span class="farm-tag diff-${d}">🌱 ${f.name} (${f.difficulty_label})</span>`;
  }).join('');
  return `
    <div class="farm-section">
      <div class="farm-section-title">🌱 Cần Farm Để Hoàn Thiện</div>
      <div class="farm-list">${tags}</div>
    </div>
  `;
};

/**
 * Build "Phân Tích AI" button data for a team evaluation result.
 */
window.teamDataRegistry = window.teamDataRegistry || {};

window.openAnalyzeModalById = function(teamId) {
  const data = window.teamDataRegistry[teamId];
  if (data) {
    window.openAnalyzeModal(data);
  }
};

window.buildAnalyzeButton = function(evalResult) {
  const team = evalResult.meta_team;
  const gens = (team.generals || []).map(g => g.name);
  const tacs = (team.generals || []).flatMap(g => g.bis_tactics || []);
  const teamId = team.id || ('team_' + Math.random().toString(36).substring(2, 9));

  window.teamDataRegistry[teamId] = {
    team_id: team.id || '',
    team_name: team.name || 'Đội Hình',
    generals: gens,
    tactics: [...new Set(tacs)],
    score: evalResult.overall_score,
    tier: team.tier,
    faction: team.faction,
    troop: team.troop
  };

  return `<button class="btn-ai-analyze" onclick="openAnalyzeModalById('${teamId}')">🔍 Phân Tích AI</button>`;
};

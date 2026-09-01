/* VAPT Dashboard Interactive JavaScript */

document.addEventListener('DOMContentLoaded', () => {
  let allFindings = [];
  let currentSeverity = 'all';
  let searchQuery = '';

  const findingsContainer = document.getElementById('findings-container');
  const visibleCountEl = document.getElementById('visible-count');
  const searchInput = document.getElementById('search-input');
  const filterBtns = document.querySelectorAll('.filter-btn');

  // Metrics elements
  const elTotal = document.getElementById('metric-total');
  const elCritical = document.getElementById('metric-critical');
  const elHigh = document.getElementById('metric-high');
  const elMedium = document.getElementById('metric-medium');
  const elLow = document.getElementById('metric-low');

  // Load findings dataset
  fetchFindings();

  async function fetchFindings() {
    try {
      const response = await fetch('findings.json');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      allFindings = data.findings || [];
      renderDashboard();
    } catch (err) {
      console.warn('Could not fetch findings.json directly (likely CORS/file protocol). Using baseline snapshot.');
      allFindings = getFallbackFindings();
      renderDashboard();
    }
  }

  function renderDashboard() {
    updateMetrics();
    renderFindings();
  }

  function updateMetrics() {
    const total = allFindings.length;
    let critical = 0, high = 0, medium = 0, low = 0;

    allFindings.forEach(f => {
      const sev = f.severity ? f.severity.toLowerCase() : '';
      if (sev === 'critical') critical++;
      else if (sev === 'high') high++;
      else if (sev === 'medium') medium++;
      else low++;
    });

    elTotal.textContent = total;
    elCritical.textContent = critical;
    elHigh.textContent = high;
    elMedium.textContent = medium;
    elLow.textContent = low;
  }

  function filterFindings() {
    return allFindings.filter(f => {
      const matchesSeverity = currentSeverity === 'all' || f.severity === currentSeverity;
      const q = searchQuery.toLowerCase();
      const matchesSearch = !q || 
        f.title.toLowerCase().includes(q) ||
        f.cwe_id.toLowerCase().includes(q) ||
        f.owasp_category.toLowerCase().includes(q) ||
        f.affected_component.toLowerCase().includes(q) ||
        f.description.toLowerCase().includes(q);

      return matchesSeverity && matchesSearch;
    });
  }

  function renderFindings() {
    const filtered = filterFindings();
    visibleCountEl.textContent = filtered.length;
    findingsContainer.innerHTML = '';

    if (filtered.length === 0) {
      findingsContainer.innerHTML = `
        <div style="text-align: center; padding: 3rem; color: var(--text-muted);">
          <h3>No findings match the selected filters.</h3>
        </div>
      `;
      return;
    }

    filtered.forEach(f => {
      const card = document.createElement('div');
      card.className = 'finding-card';
      const tagClass = `tag-${(f.severity || 'info').toLowerCase()}`;

      card.innerHTML = `
        <div class="finding-header" tabindex="0" role="button" aria-expanded="false">
          <div class="finding-title-group">
            <h3>${escapeHtml(f.id)}: ${escapeHtml(f.title)}</h3>
            <div class="finding-meta">
              <span><strong>Category:</strong> ${escapeHtml(f.owasp_category)}</span>
              <span><strong>CWE:</strong> ${escapeHtml(f.cwe_id)}</span>
              <span><strong>Component:</strong> ${escapeHtml(f.affected_component)}</span>
            </div>
          </div>
          <div style="text-align: right;">
            <span class="tag ${tagClass}">${escapeHtml(f.severity)}</span>
            <div class="cvss-badge" style="margin-top: 0.4rem;">CVSS ${f.cvss_score}</div>
          </div>
        </div>

        <div class="finding-details">
          <p style="margin-bottom: 1rem;">${escapeHtml(f.description)}</p>

          <div class="detail-grid">
            <div class="detail-box">
              <h4>CVSS Vector</h4>
              <p><code>${escapeHtml(f.cvss_vector)}</code></p>
            </div>
            <div class="detail-box">
              <h4>Discovery Source</h4>
              <p>${escapeHtml(f.discovery_source)}</p>
            </div>
            <div class="detail-box">
              <h4>Validation Status</h4>
              <p><code>${escapeHtml(f.validation_status)}</code></p>
            </div>
          </div>

          <h4 style="margin-top: 1rem; color: var(--text-muted);">Reproduction Steps</h4>
          <pre>${escapeHtml(f.reproduction_steps)}</pre>

          <h4 style="margin-top: 1rem; color: var(--text-muted);">Evidence</h4>
          <pre>${escapeHtml(f.evidence)}</pre>

          <h4 style="margin-top: 1rem; color: var(--text-muted);">Remediation Guidance</h4>
          <p style="background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3b82f6; padding: 0.75rem; border-radius: 4px; margin-top: 0.5rem;">
            ${escapeHtml(f.remediation)}
          </p>
        </div>
      `;

      const header = card.querySelector('.finding-header');
      header.addEventListener('click', () => {
        const isOpen = card.classList.toggle('open');
        header.setAttribute('aria-expanded', isOpen);
      });
      header.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          const isOpen = card.classList.toggle('open');
          header.setAttribute('aria-expanded', isOpen);
        }
      });

      findingsContainer.appendChild(card);
    });
  }

  // Filter button handlers
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentSeverity = btn.getAttribute('data-severity');
      renderFindings();
    });
  });

  // Search input handler
  searchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value;
    renderFindings();
  });

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function getFallbackFindings() {
    return [
      {
        id: "VAPT-2026-001",
        title: "SQL Injection in User Authentication Endpoint",
        description: "The email input field on the login endpoint (/rest/user/login) fails to sanitize SQL metacharacters.",
        affected_component: "POST /rest/user/login",
        discovery_source: "Manual Burp Suite",
        validation_status: "confirmed",
        evidence: "Payload: ' OR 1=1-- returned HTTP 200 OK with admin session token.",
        reproduction_steps: "1. Navigate to login page.\n2. Submit ' OR 1=1-- in email field.",
        cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        cvss_score: 9.8,
        severity: "Critical",
        cwe_id: "CWE-89",
        owasp_category: "A03:2021-Injection",
        remediation: "Use parameterized SQL queries (Prepared Statements)."
      },
      {
        id: "VAPT-2026-002",
        title: "Reflected Cross-Site Scripting (XSS) in Product Search",
        description: "Search parameter reflects user input into the DOM without HTML entity encoding.",
        affected_component: "GET /#/search?q=",
        discovery_source: "Manual Burp Suite",
        validation_status: "confirmed",
        evidence: "<iframe src=\"javascript:alert(1)\"> execution pop-up.",
        reproduction_steps: "1. Access search page with iframe payload.",
        cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
        cvss_score: 6.1,
        severity: "Medium",
        cwe_id: "CWE-79",
        owasp_category: "A03:2021-Injection",
        remediation: "Contextually encode user-supplied data in DOM context."
      }
    ];
  }
});

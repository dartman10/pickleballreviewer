/* Pickleball Review Hub — App JS */
(function() {
  const searchInput = document.getElementById('search-input');
  const filterBtns = document.querySelectorAll('.filter-btn');
  const productsGrid = document.getElementById('products-grid');
  const noResults = document.getElementById('no-results');
  const totalCount = document.getElementById('total-count');
  const productCount = document.getElementById('product-count');
  let allPaddles = [];

  function loadPaddles() {
    fetch('data/paddles.json')
      .then(r => r.json())
      .then(data => {
        allPaddles = data.paddles;
        if (totalCount) totalCount.textContent = allPaddles.length;
        renderPaddles(allPaddles);
      });
  }

  function renderPaddles(paddles) {
    if (!productsGrid) return;
    if (paddles.length === 0) {
      productsGrid.innerHTML = '';
      if (noResults) noResults.style.display = 'block';
      if (productCount) productCount.textContent = 'No matches found';
      return;
    }
    if (noResults) noResults.style.display = 'none';
    if (productCount) productCount.textContent = `Showing ${paddles.length} paddle${paddles.length !== 1 ? 's' : ''}`;
    productsGrid.innerHTML = paddles.map(p => {
      const specStr = p.measured_specs ? Object.entries(p.measured_specs).slice(0,3).map(([k,v]) => `<span><span class="spec-label">${k.replace(/_/g,' ')}:</span> ${v}</span>`).join('') : '';
      const videoCount = p.youtube_videos ? p.youtube_videos.length : 0;
      const reviewCount = p.written_reviews ? p.written_reviews.length : 0;
      const consensusCount = p.consensus_topics ? p.consensus_topics.length : 0;
      return `<article class="paddle-card" id="${p.id}">
        <div class="paddle-card-header">
          <h3><a href="pages/paddles/${p.id}.html">${p.name}</a></h3>
          <span class="paddle-card-price">${p.price_range}</span>
        </div>
        <p class="paddle-card-desc">${p.description}</p>
        ${specStr ? `<div class="paddle-card-specs">${specStr}</div>` : ''}
        <div class="paddle-card-tags">${p.tags.map(t => `<span class="tag ${t}">${t}</span>`).join('')}</div>
        <div class="paddle-card-stats">
          ${videoCount ? `<span>▶ ${videoCount} video${videoCount > 1 ? 's' : ''}</span>` : ''}
          ${reviewCount ? `<span>📝 ${reviewCount} review${reviewCount > 1 ? 's' : ''}</span>` : ''}
          ${consensusCount ? `<span>🔍 ${consensusCount} consensus${consensusCount > 1 ? 'topics' : ''}</span>` : ''}
        </div>
      </article>`;
    }).join('');
  }

  function filterPaddles(query, tag) {
    let results = allPaddles;
    if (query) {
      const q = query.toLowerCase();
      results = results.filter(p =>
        p.name.toLowerCase().includes(q) ||
        p.brand.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q) ||
        (p.tags && p.tags.some(t => t.includes(q)))
      );
    }
    if (tag && tag !== 'all') {
      results = results.filter(p => p.tags && p.tags.includes(tag));
    }
    renderPaddles(results);
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const activeTag = document.querySelector('.filter-btn.active')?.dataset.filter || 'all';
      filterPaddles(e.target.value, activeTag);
    });
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const tag = btn.dataset.filter;
      filterPaddles(searchInput ? searchInput.value : '', tag);
    });
  });

  // Load data
  loadPaddles();
})();

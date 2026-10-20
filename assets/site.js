(() => {
  const search = document.querySelector('#report-search');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const rows = [...document.querySelectorAll('[data-report]')];
  let category = 'all';
  function update() {
    const query = (search?.value || '').trim().toLowerCase();
    let shown = 0;
    rows.forEach(row => {
      const match = (category === 'all' || row.dataset.category === category) &&
        row.dataset.search.toLowerCase().includes(query);
      row.hidden = !match;
      if (match) shown += 1;
    });
    const empty = document.querySelector('#empty-results');
    if (empty) empty.hidden = shown !== 0;
  }
  filters.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    update();
  }));
  search?.addEventListener('input', update);
  const toc = document.querySelector('.tocbox');
  if (toc && window.matchMedia('(min-width: 701px)').matches) toc.open = true;
})();

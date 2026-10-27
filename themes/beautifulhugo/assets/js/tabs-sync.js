// Keep tabs that share a groupId in sync across tab blocks.
document.addEventListener('shown.bs.tab', (event) => {
  const button = event.target;
  const syncGroup = button?.dataset?.tabGroup;
  const syncKey = button?.dataset?.tabKey;
  if (!syncGroup || !syncKey) return;

  document.querySelectorAll('.tabs-shortcode .nav-link').forEach((candidate) => {
    if (candidate === button) return;
    if (candidate.dataset.tabGroup !== syncGroup || candidate.dataset.tabKey !== syncKey) return;
    if (candidate.classList.contains('active')) return;
    bootstrap.Tab.getOrCreateInstance(candidate).show();
  });
});

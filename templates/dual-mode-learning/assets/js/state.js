// URL state works across modes, reloads and copied deep links; no storage needed.
export function readLabState() {
  const params = new URLSearchParams(location.search);
  const requested = params.get('filter');
  const filter = ['vertical', 'average', 'identity'].includes(requested) ? requested : 'vertical';
  const raw = params.get('position');
  const position = raw !== null && /^[0-8]$/.test(raw) ? Number(raw) : 0;
  return { filter, position };
}
export function saveLabState(filter, position) {
  const url = new URL(location.href);
  url.searchParams.set('filter', filter);
  url.searchParams.set('position', String(position));
  history.replaceState(null, '', url);
  window.dispatchEvent(new CustomEvent('lessonstatechange'));
}
export function updateModeLink(sectionId) {
  const link = document.querySelector('.mode-link');
  if (!link) return;
  const url = new URL(link.getAttribute('href'), location.href);
  const { filter, position } = readLabState();
  url.searchParams.set('filter', filter);
  url.searchParams.set('position', String(position));
  url.hash = sectionId;
  link.href = url.href;
}

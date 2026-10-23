// The view and the interactive reference's threshold survive a mode switch.
export function readThreshold() {
  const raw=new URLSearchParams(location.search).get('threshold');
  return raw!==null && /^(100|[0-9]{1,2})$/.test(raw) ? Number(raw) : 60;
}
export function setThreshold(value) {
  const url=new URL(location.href);url.searchParams.set('threshold',String(value));
  history.replaceState(null,'',url);window.dispatchEvent(new Event('referencestatechange'));
}
export function updateModeLink(id) {
  const link=document.querySelector('.mode-link');
  const url=new URL(link.getAttribute('href'),location.href);
  url.search='';url.searchParams.set('threshold',String(readThreshold()));url.hash=`ref-${id}`;
  link.href=url.href;
}
export function setReference(id) {
  const url=new URL(location.href);url.hash=`ref-${id}`;
  history.replaceState(null,'',url);updateModeLink(id);
}

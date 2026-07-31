let scheduled = null;

self.addEventListener('message', e => {
  const { type, endTime, title, body } = e.data;

  if (type === 'SCHEDULE') {
    if (scheduled) clearTimeout(scheduled);
    const delay = Math.max(0, endTime - Date.now());
    scheduled = setTimeout(() => {
      self.registration.showNotification(title, { body, icon: '/favicon.ico', badge: '/favicon.ico', tag: 'focus-timer', renotify: true });
      scheduled = null;
    }, delay);
  }

  if (type === 'CANCEL') {
    if (scheduled) { clearTimeout(scheduled); scheduled = null; }
  }
});

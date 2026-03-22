self.addEventListener('notificationclick', e => {
  e.notification.close();
  const a = e.action;
  if (a === 'done' || a === 'start' || a === 'focus') {
    e.waitUntil(clients.matchAll({type:'window'}).then(cs => {
      if (cs.length) cs[0].focus();
      else clients.openWindow('/');
    }));
  }
  if (a === 'snooze') {
    e.waitUntil(clients.matchAll({type:'window'}).then(cs => {
      cs.forEach(c => c.postMessage({action: e.notification.tag === 'water' ? 'snooze-water' : 'snooze-focus'}));
    }));
  }
  if (a === 'water') {
    e.waitUntil(clients.matchAll({type:'window'}).then(cs => {
      cs.forEach(c => c.postMessage({action:'snooze-water'}));
    }));
  }
});

self.addEventListener('push', e => {
  const d = e.data?.json() || {};
  e.waitUntil(self.registration.showNotification(d.title || 'kirbs.pomodoro', {
    body: d.body, icon: d.icon, tag: d.tag, actions: d.actions || []
  }));
});

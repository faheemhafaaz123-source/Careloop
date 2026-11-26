// CARELOOP_STATIC_TEST_2026
/* Careloop FCM background notification service worker.
   The scheduler will send data-only FCM messages; this worker displays them. */
self.addEventListener("push", (event) => {
  let payload = {};
  try {
    payload = event.data ? event.data.json() : {};
  } catch (e) {
    payload = { data: { body: event.data ? event.data.text() : "" } };
  }

  const data = payload.data || {};
  const notification = payload.notification || {};
  const title = notification.title || data.title || "Careloop reminder";
  const body = notification.body || data.body || "It's time for your reminder.";

  event.waitUntil(
    self.registration.showNotification(title, {
      body,
      tag: data.reminder_id || "careloop-reminder",
      data: data
    })
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  event.waitUntil(clients.matchAll({ type: "window", includeUncontrolled: true }).then((clientList) => {
    for (const client of clientList) {
      if ("focus" in client) return client.focus();
    }
    if (clients.openWindow) return clients.openWindow("/");
  }));
});

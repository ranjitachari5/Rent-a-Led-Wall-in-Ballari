// script.js — Booking form logic

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('bookingForm');
  if (!form) return;

  const startDateInput = document.getElementById('start_date');
  const endDateInput = document.getElementById('end_date');
  const statusDiv = document.getElementById('availabilityStatus');
  const submitBtn = document.getElementById('submitBtn');
  const wallSize = document.getElementById('led_wall_size').value;

  // Set min date to today
  const today = new Date().toISOString().split('T')[0];
  startDateInput.min = today;
  endDateInput.min = today;

  startDateInput.addEventListener('change', () => {
    endDateInput.min = startDateInput.value;
    if (endDateInput.value && endDateInput.value < startDateInput.value) {
      endDateInput.value = startDateInput.value;
    }
    checkAvailabilityIfReady();
    updateSummaryDates();
  });

  endDateInput.addEventListener('change', () => {
    checkAvailabilityIfReady();
    updateSummaryDates();
  });

  document.getElementById('event_address').addEventListener('input', (e) => {
    const el = document.getElementById('sum-location');
    const val = document.getElementById('sum-location-val');
    if (el && val && e.target.value) {
      el.style.display = 'flex';
      val.textContent = e.target.value.length > 40
        ? e.target.value.substring(0, 40) + '...'
        : e.target.value;
    }
  });

  let checkTimeout;
  function checkAvailabilityIfReady() {
    const start = startDateInput.value;
    const end = endDateInput.value;
    if (!start || !end) return;

    clearTimeout(checkTimeout);
    checkTimeout = setTimeout(() => checkAvailability(start, end), 400);
  }

  async function checkAvailability(start, end) {
    statusDiv.className = 'availability-status';
    statusDiv.style.display = 'none';
    submitBtn.disabled = true;

    statusDiv.innerHTML = '<span class="spinner"></span> Checking availability…';
    statusDiv.style.display = 'flex';

    try {
      const res = await fetch('/api/check-availability', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ led_wall_size: wallSize, start_date: start, end_date: end }),
      });
      const data = await res.json();

      if (data.available) {
        statusDiv.className = 'availability-status available';
        statusDiv.innerHTML = '✓ ' + data.message;
        submitBtn.disabled = false;
      } else {
        statusDiv.className = 'availability-status unavailable';
        statusDiv.innerHTML = '✗ ' + data.message;
        submitBtn.disabled = true;
      }
    } catch {
      statusDiv.className = 'availability-status unavailable';
      statusDiv.innerHTML = '✗ Could not check availability. Please try again.';
    }
  }

  function updateSummaryDates() {
    const start = startDateInput.value;
    const end = endDateInput.value;
    const el = document.getElementById('sum-dates');
    const val = document.getElementById('sum-dates-val');
    if (el && val && start && end) {
      el.style.display = 'flex';
      val.textContent = `${formatDate(start)} → ${formatDate(end)}`;
    }
  }

  function formatDate(str) {
    const d = new Date(str + 'T00:00:00');
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }

  // Form submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('customer_name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const address = document.getElementById('event_address').value.trim();
    const start = startDateInput.value;
    const end = endDateInput.value;
    const lat = document.getElementById('latitude').value;
    const lng = document.getElementById('longitude').value;

    if (!name || !phone || !address || !start || !end) {
      showToast('Please fill in all required fields.', 'error');
      return;
    }

    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner"></span> Processing…';

    try {
      const res = await fetch('/api/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_name: name,
          phone,
          led_wall_size: wallSize,
          start_date: start,
          end_date: end,
          event_address: address,
          latitude: lat ? parseFloat(lat) : null,
          longitude: lng ? parseFloat(lng) : null,
        }),
      });
      const data = await res.json();

      if (data.success) {
        window.location.href = `/success/${data.booking_id}`;
      } else {
        showToast(data.message || 'Booking failed. Please try again.', 'error');
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Confirm Booking';
      }
    } catch {
      showToast('Network error. Please try again.', 'error');
      submitBtn.disabled = false;
      submitBtn.innerHTML = 'Confirm Booking';
    }
  });
});

function showToast(msg, type = 'success') {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.className = `toast ${type} show`;
  setTimeout(() => { toast.className = 'toast'; }, 4000);
}

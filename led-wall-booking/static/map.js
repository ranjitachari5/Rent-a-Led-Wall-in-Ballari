// map.js — Leaflet map initialization for booking form

let map, marker;

function initMap() {
  // Default center: New York City
  const defaultLat = 40.7128;
  const defaultLng = -74.0060;

  map = L.map('map', {
    center: [defaultLat, defaultLng],
    zoom: 11,
    zoomControl: true,
  });

  // Dark tile layer using CartoDB dark tiles
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20,
  }).addTo(map);

  // Custom red marker icon
  const redIcon = L.divIcon({
    className: '',
    html: `<div style="
      width: 28px; height: 28px;
      background: #ff3d00;
      border: 3px solid #fff;
      border-radius: 50% 50% 50% 0;
      transform: rotate(-45deg);
      box-shadow: 0 0 10px rgba(255,61,0,0.6);
    "></div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 28],
  });

  // Click to place marker
  map.on('click', function (e) {
    const { lat, lng } = e.latlng;

    if (marker) {
      marker.setLatLng([lat, lng]);
    } else {
      marker = L.marker([lat, lng], { icon: redIcon }).addTo(map);
    }

    // Store in hidden fields
    document.getElementById('latitude').value = lat.toFixed(6);
    document.getElementById('longitude').value = lng.toFixed(6);

    // Update summary
    updateSummaryCoords(lat, lng);

    // Reverse geocode for address suggestion
    reverseGeocode(lat, lng);
  });
}

function reverseGeocode(lat, lng) {
  fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
    .then(r => r.json())
    .then(data => {
      if (data && data.display_name) {
        const addressField = document.getElementById('event_address');
        if (!addressField.value || addressField.value === addressField.dataset.lastGeo) {
          addressField.value = data.display_name;
          addressField.dataset.lastGeo = data.display_name;
          updateSummaryLocation(data.display_name);
        }
      }
    })
    .catch(() => {});
}

function updateSummaryCoords(lat, lng) {
  const el = document.getElementById('sum-coords');
  const val = document.getElementById('sum-coords-val');
  if (el && val) {
    el.style.display = 'flex';
    val.textContent = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
  }
}

function updateSummaryLocation(address) {
  const el = document.getElementById('sum-location');
  const val = document.getElementById('sum-location-val');
  if (el && val) {
    el.style.display = 'flex';
    val.textContent = address.length > 40 ? address.substring(0, 40) + '...' : address;
  }
}

// Init when DOM is ready
document.addEventListener('DOMContentLoaded', initMap);

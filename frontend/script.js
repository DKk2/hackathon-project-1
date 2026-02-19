const apiBase = "";

let buildings = [];
let currentLocation = "";

async function fetchBuildings() {
  const res = await fetch(`${apiBase}/buildings`);
  buildings = await res.json();
  populateSelectors();
}

function populateSelectors() {
  const names = buildings.map((b) => b.name);

  const startSelect = document.getElementById("startSelect");
  const endSelect = document.getElementById("endSelect");
  const qrSelect = document.getElementById("qrBuildingSelect");

  [startSelect, endSelect, qrSelect].forEach((select) => {
    select.innerHTML = names
      .map((name) => `<option value="${name}">${name}</option>`)
      .join("");
  });

  if (names.length > 0) {
    startSelect.value = names[0];
    endSelect.value = names[Math.min(1, names.length - 1)];
  }
}

async function navigate() {
  const start = document.getElementById("startSelect").value;
  const end = document.getElementById("endSelect").value;

  const res = await fetch(
    `${apiBase}/navigate?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`
  );
  const data = await res.json();

  const directionsText = document.getElementById("directionsText");
  const distanceText = document.getElementById("distanceText");

  if (!res.ok) {
    directionsText.textContent = data.error || "Unable to fetch route.";
    distanceText.textContent = "";
    return;
  }

  directionsText.textContent = data.directions;
  distanceText.textContent = `Total distance: ${data.total_distance} units`;
}

async function scanQr() {
  const qr_id = document.getElementById("qrBuildingSelect").value;
  const res = await fetch(`${apiBase}/scan_qr`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ qr_id }),
  });

  const data = await res.json();
  const status = document.getElementById("qrStatus");

  if (!res.ok) {
    status.textContent = data.error || "QR scan failed.";
    return;
  }

  currentLocation = data.current_location;
  document.getElementById("startSelect").value = currentLocation;
  status.textContent = `Current location set to: ${currentLocation}`;
}

function searchBuilding() {
  const search = document.getElementById("searchInput").value.trim().toLowerCase();
  const result = document.getElementById("searchResult");

  if (!search) {
    result.textContent = "Enter a building name to search.";
    return;
  }

  const match = buildings.find((b) => b.name.toLowerCase() === search);
  if (!match) {
    result.textContent = "Building not found in campus data.";
    return;
  }

  result.textContent = `Found ${match.name} at simulated coordinates (${match.x_coordinate}, ${match.y_coordinate}).`;
}

window.addEventListener("DOMContentLoaded", async () => {
  await fetchBuildings();
  document.getElementById("navigateBtn").addEventListener("click", navigate);
  document.getElementById("scanQrBtn").addEventListener("click", scanQr);
  document.getElementById("searchBtn").addEventListener("click", searchBuilding);
});

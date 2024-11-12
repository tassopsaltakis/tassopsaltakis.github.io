// hud.js
function updateHUD() {
  if (!airplane) return;

  // Update Airspeed (convert to km/h)
  const airspeedKmh = airspeed * 3.6;
  document.getElementById('airspeed').innerText = `Airspeed: ${Math.round(airspeedKmh)} km/h`;

  // Update Altitude
  const altitude = airplane.position.y;
  document.getElementById('altitude').innerText = `Altitude: ${Math.round(altitude)} m`;

  // Update Throttle
  const throttlePercentage = throttle * 100;
  document.getElementById('throttle').innerText = `Throttle: ${Math.round(throttlePercentage)}%`;
}

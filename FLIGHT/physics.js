// physics.js
let airspeed = 0;
const maxSpeed = 200; // Maximum speed in meters per second
const airplaneMass = 1000; // In kilograms
const dragCoefficient = 0.02;
const liftCoefficient = 1.0;
const wingArea = 16; // Square meters
const airDensity = 1.225; // kg/m^3 at sea level
const gravity = -9.81; // Gravity constant
let verticalSpeed = 0;

function updatePhysics(deltaTime) {
  if (!airplane) return;

  // Calculate thrust
  const thrust = throttle * 50000; // Adjust max thrust as needed

  // Calculate drag force
  const dragForce = 0.5 * dragCoefficient * airDensity * airspeed * airspeed * wingArea;

  // Calculate net force in the forward direction
  const netForce = thrust - dragForce;

  // Update airspeed
  const acceleration = netForce / airplaneMass;
  airspeed += acceleration * deltaTime;
  if (airspeed < 0) airspeed = 0;

  // Calculate lift force
  const angleOfAttack = airplane.rotation.x;
  const liftForce = 0.5 * liftCoefficient * airDensity * airspeed * airspeed * wingArea * Math.cos(angleOfAttack);

  // Update vertical speed
  const verticalAcceleration = (liftForce / airplaneMass) + gravity;
  verticalSpeed += verticalAcceleration * deltaTime;

  // Update airplane position
  const forward = new THREE.Vector3(0, 0, -1);
  forward.applyQuaternion(airplane.quaternion);
  airplane.position.add(forward.multiplyScalar(airspeed * deltaTime));

  airplane.position.y += verticalSpeed * deltaTime;

  // Simple Ground Collision
  if (airplane.position.y <= 0.5) {
    airplane.position.y = 0.5;
    verticalSpeed = 0;
  }

  // Rotate propeller
  const propeller = airplane.children.find(child => child.geometry.type === 'BoxGeometry' && child.material.color.getHex() === 0x000000);
  if (propeller) {
    propeller.rotation.x += 0.3 * throttle;
  }
}

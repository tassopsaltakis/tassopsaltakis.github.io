// controls.js
let keyboard = {};
let gamepad = null;
let throttle = 0.5; // Initial throttle at 50%

// Keyboard Input
window.addEventListener('keydown', (e) => {
  keyboard[e.code] = true;
});

window.addEventListener('keyup', (e) => {
  keyboard[e.code] = false;
});

// Gamepad Input
window.addEventListener('gamepadconnected', (e) => {
  console.log('Gamepad connected:', e.gamepad);
  gamepad = e.gamepad;
});

window.addEventListener('gamepaddisconnected', (e) => {
  console.log('Gamepad disconnected:', e.gamepad);
  gamepad = null;
});

function processKeyboardInput(deltaTime) {
  const rotationSpeed = 1; // Radians per second
  const throttleChange = 0.5; // Throttle change per second

  if (!airplane) return;

  // Yaw (Left/Right)
  if (keyboard['ArrowLeft'] || keyboard['KeyA']) {
    airplane.rotation.y += rotationSpeed * deltaTime;
  }
  if (keyboard['ArrowRight'] || keyboard['KeyD']) {
    airplane.rotation.y -= rotationSpeed * deltaTime;
  }

  // Pitch (Up/Down)
  if (keyboard['ArrowUp'] || keyboard['KeyW']) {
    airplane.rotation.x += rotationSpeed * deltaTime;
  }
  if (keyboard['ArrowDown'] || keyboard['KeyS']) {
    airplane.rotation.x -= rotationSpeed * deltaTime;
  }

  // Roll (Q/E)
  if (keyboard['KeyQ']) {
    airplane.rotation.z += rotationSpeed * deltaTime;
  }
  if (keyboard['KeyE']) {
    airplane.rotation.z -= rotationSpeed * deltaTime;
  }

  // Throttle Control (Shift/Ctrl)
  if (keyboard['ShiftLeft']) {
    throttle += throttleChange * deltaTime;
    if (throttle > 1) throttle = 1;
  }
  if (keyboard['ControlLeft']) {
    throttle -= throttleChange * deltaTime;
    if (throttle < 0) throttle = 0;
  }
}

function processGamepadInput(deltaTime) {
  if (!gamepad || !airplane) return;

  const rotationSpeed = 2; // Adjust sensitivity as needed
  const throttleChange = 0.5;

  // Update gamepad state
  gamepad = navigator.getGamepads()[gamepad.index];

  // Axes
  const yaw = gamepad.axes[0];    // Left stick X-axis
  const pitch = gamepad.axes[1];  // Left stick Y-axis
  const roll = gamepad.axes[2] || 0;   // Right stick X-axis (if available)
  const throttleUp = gamepad.buttons[7].value; // Right trigger
  const throttleDown = gamepad.buttons[6].value; // Left trigger

  // Apply rotations
  airplane.rotation.y -= yaw * rotationSpeed * deltaTime;
  airplane.rotation.x += pitch * rotationSpeed * deltaTime;
  airplane.rotation.z += roll * rotationSpeed * deltaTime;

  // Throttle control
  throttle += (throttleUp - throttleDown) * throttleChange * deltaTime;
  if (throttle > 1) throttle = 1;
  if (throttle < 0) throttle = 0;
}

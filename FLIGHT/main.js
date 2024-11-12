// main.js
let scene, camera, renderer;
let clock = new THREE.Clock();

// Audio (Web Audio API)
let audioContext, oscillator, gainNode;

function init() {
  // Scene
  scene = new THREE.Scene();

  // Camera
  camera = new THREE.PerspectiveCamera(
    75, window.innerWidth / window.innerHeight, 0.1, 5000
  );
  camera.position.set(0, 2, 5);

  // Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  // Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
  directionalLight.position.set(10, 10, 10);
  scene.add(directionalLight);

  // Add Skybox
  addSkybox();

  // Generate Terrain
  generateProceduralTerrain();

  // Create the Airplane Model
  createAirplane();

  // Setup Audio
  setupAudio();

  // Handle Window Resize
  window.addEventListener('resize', onWindowResize, false);

  // Start Animation Loop
  animate();
}

function addSkybox() {
  const skyGeo = new THREE.BoxGeometry(5000, 5000, 5000);
  const materialArray = [];

  const skyColor = new THREE.Color(0x87ceeb); // Light blue

  for (let i = 0; i < 6; i++) {
    materialArray.push(new THREE.MeshBasicMaterial({
      color: skyColor,
      side: THREE.BackSide
    }));
  }

  const skybox = new THREE.Mesh(skyGeo, materialArray);
  scene.add(skybox);
}

function generateProceduralTerrain() {
  const size = 5000;
  const divisions = 256;
  const geometry = new THREE.PlaneGeometry(size, size, divisions, divisions);
  const material = new THREE.MeshPhongMaterial({ color: 0x228B22, wireframe: false });
  const terrain = new THREE.Mesh(geometry, material);
  terrain.rotation.x = -Math.PI / 2;
  scene.add(terrain);

  // Height variation using Perlin noise
  const vertices = geometry.attributes.position.array;

  for (let i = 0; i <= divisions; i++) {
    for (let j = 0; j <= divisions; j++) {
      const index = (i * (divisions + 1) + j) * 3 + 2;
      const x = i / divisions;
      const y = j / divisions;
      const height = Perlin.noise(x * 10, y * 10) * 50; // Adjust scaling as needed
      vertices[index] = height;
    }
  }

  geometry.attributes.position.needsUpdate = true;
  geometry.computeVertexNormals();
}

function setupAudio() {
  audioContext = new (window.AudioContext || window.webkitAudioContext)();
  oscillator = audioContext.createOscillator();
  gainNode = audioContext.createGain();

  oscillator.type = 'sawtooth';
  oscillator.frequency.setValueAtTime(50, audioContext.currentTime); // Starting frequency
  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);
  gainNode.gain.setValueAtTime(0.1, audioContext.currentTime); // Starting volume
  oscillator.start();
}

function updateAudio() {
  if (oscillator) {
    const frequency = 50 + throttle * 200; // Adjust frequency based on throttle
    oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
  }
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();

  renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
  requestAnimationFrame(animate);

  const deltaTime = clock.getDelta();

  if (airplane) {
    // Update Controls
    processKeyboardInput(deltaTime);
    processGamepadInput(deltaTime);

    // Update Physics
    updatePhysics(deltaTime);

    // Update Camera
    updateCamera();

    // Update HUD
    updateHUD();

    // Update Audio
    updateAudio();
  }

  // Render Scene
  renderer.render(scene, camera);
}

function updateCamera() {
  // Camera follows the airplane from behind
  const relativeCameraOffset = new THREE.Vector3(0, 2, 10);
  const cameraOffset = relativeCameraOffset.applyMatrix4(airplane.matrixWorld);

  camera.position.lerp(cameraOffset, 0.1);
  camera.lookAt(airplane.position);
}

window.onload = init;

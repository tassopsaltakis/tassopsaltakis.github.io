// airplane.js

let airplane;

function createAirplane() {
  airplane = new THREE.Group();

  // Fuselage
  const fuselageGeometry = new THREE.CylinderGeometry(0.2, 0.2, 4, 16);
  const fuselageMaterial = new THREE.MeshPhongMaterial({ color: 0xff0000 });
  const fuselage = new THREE.Mesh(fuselageGeometry, fuselageMaterial);
  fuselage.rotation.z = Math.PI / 2; // Rotate to align with the X-axis
  airplane.add(fuselage);

  // Nose Cone
  const noseGeometry = new THREE.ConeGeometry(0.2, 0.5, 16);
  const noseMaterial = new THREE.MeshPhongMaterial({ color: 0xff0000 });
  const nose = new THREE.Mesh(noseGeometry, noseMaterial);
  nose.rotation.z = Math.PI / 2;
  nose.position.x = 2.25;
  airplane.add(nose);

  // Cockpit
  const cockpitGeometry = new THREE.SphereGeometry(0.15, 16, 8);
  const cockpitMaterial = new THREE.MeshPhongMaterial({ color: 0x0000ff });
  const cockpit = new THREE.Mesh(cockpitGeometry, cockpitMaterial);
  cockpit.position.x = 1.5;
  cockpit.position.y = 0.1;
  airplane.add(cockpit);

  // Tail
  const tailGeometry = new THREE.ConeGeometry(0.15, 0.5, 16);
  const tailMaterial = new THREE.MeshPhongMaterial({ color: 0xff0000 });
  const tail = new THREE.Mesh(tailGeometry, tailMaterial);
  tail.rotation.z = -Math.PI / 2;
  tail.position.x = -2.25;
  airplane.add(tail);

  // Wings
  const wingGeometry = new THREE.BoxGeometry(0.1, 1, 6);
  const wingMaterial = new THREE.MeshPhongMaterial({ color: 0xff0000 });
  const wing = new THREE.Mesh(wingGeometry, wingMaterial);
  wing.position.y = 0;
  airplane.add(wing);

  // Horizontal Stabilizer
  const hStabGeometry = new THREE.BoxGeometry(0.05, 0.5, 1.5);
  const hStabMaterial = new THREE.MeshPhongMaterial({ color: 0xff0000 });
  const hStab = new THREE.Mesh(hStabGeometry, hStabMaterial);
  hStab.position.set(-2.5, 0, 0);
  airplane.add(hStab);

  // Vertical Stabilizer
  const vStabGeometry = new THREE.BoxGeometry(0.05, 0.8, 0.5);
  const vStabMaterial = new THREE.MeshPhongMaterial({ color: 0xff0000 });
  const vStab = new THREE.Mesh(vStabGeometry, vStabMaterial);
  vStab.position.set(-2.5, 0.4, 0);
  vStab.rotation.z = Math.PI / 2;
  airplane.add(vStab);

  // Propeller
  const propellerGeometry = new THREE.BoxGeometry(0.1, 0.5, 0.05);
  const propellerMaterial = new THREE.MeshPhongMaterial({ color: 0x000000 });
  const propeller = new THREE.Mesh(propellerGeometry, propellerMaterial);
  propeller.position.x = 2.5;
  airplane.add(propeller);

  // Set initial position
  airplane.position.y = 1; // Start above the ground

  scene.add(airplane);
}

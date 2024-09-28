const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let particles = [];
let currentElementType = 'powder';
let drawing = false;
let brushSize = document.getElementById('brushSize').value;
let particleDensity = document.getElementById('particleDensity').value;

// Event listeners for brush size and particle density
document.getElementById('brushSize').addEventListener('input', (e) => {
    brushSize = e.target.value;
});

document.getElementById('particleDensity').addEventListener('input', (e) => {
    particleDensity = e.target.value;
});

// Add particles when mouse is clicked and held down
canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    createParticles(e);
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
});

canvas.addEventListener('mousemove', (e) => {
    if (drawing) {
        createParticles(e);
    }
});

// Create multiple particles based on density and brush size
function createParticles(e) {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    for (let i = 0; i < particleDensity; i++) {
        const randomOffsetX = (Math.random() - 0.5) * brushSize;
        const randomOffsetY = (Math.random() - 0.5) * brushSize;
        particles.push(new Particle(x + randomOffsetX, y + randomOffsetY, currentElementType, 5));
    }
}

function setElementType(type) {
    currentElementType = type;
}

function clearCanvas() {
    particles = [];
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// Main game loop to update and draw particles
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Remove particles marked for removal (e.g., fire particles that burn out)
    particles = particles.filter(particle => !particle.remove);

    // Update and draw each particle
    particles.forEach(particle => {
        particle.update();
        particle.draw(ctx);
    });

    requestAnimationFrame(gameLoop);
}

gameLoop();  // Start the loop

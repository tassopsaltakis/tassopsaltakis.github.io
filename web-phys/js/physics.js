class Particle {
    constructor(x, y, type, size) {
        this.x = x;
        this.y = y;
        this.type = type;
        this.color = elements[type].color;
        this.gravity = elements[type].gravity;
        this.size = size;
        this.velocityY = 0;
        this.settled = false;
        this.remove = false;
    }

    update() {
        if (!checkBelow(this) && this.y < canvas.height - this.size) {
            this.velocityY += this.gravity;  // Apply gravity force
            this.y += this.velocityY;  // Update position based on velocity
        } else {
            this.velocityY = 0;  // Reset velocity when hitting the bottom or another particle
            this.resolveCollision();
        }

        this.checkBounds();
    }

    resolveCollision() {
        const below = checkBelow(this);
        if (below) {
            const overlap = this.y + this.size - below.y;

            if (overlap > 0 && overlap < this.size) {
                // Correct the overlap by moving up and settle
                this.y -= overlap * 0.5;
                this.settled = true;
            } else {
                // If no room to move up, try moving sideways
                this.tryMoveSideways();
            }
        } else {
            this.settled = false;
        }
    }

    tryMoveSideways() {
        let moved = false;

        if (!checkLeft(this) && Math.random() > 0.5) {
            this.x -= this.size;  // Try moving left
            moved = true;
        } else if (!checkRight(this)) {
            this.x += this.size;  // Try moving right
            moved = true;
        }

        if (!moved) {
            this.settled = true;  // Settle if can't move sideways
        }
    }

    checkBounds() {
        if (this.x <= 0) this.x = 0;
        if (this.x >= canvas.width - this.size) this.x = canvas.width - this.size;
        if (this.y >= canvas.height - this.size) this.y = canvas.height - this.size;
    }

    draw(ctx) {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.size, this.size);  // Draw the particle
    }
}

// Check if there is a particle directly below this one
function checkBelow(particle) {
    return particles.find(p =>
        p.x < particle.x + particle.size && p.x + p.size > particle.x &&
        p.y === particle.y + particle.size
    );
}

// Check if there is a particle to the left
function checkLeft(particle) {
    return particles.some(p => p.x === particle.x - particle.size && p.y === particle.y);
}

// Check if there is a particle to the right
function checkRight(particle) {
    return particles.some(p => p.x === particle.x + particle.size && p.y === particle.y);
}

// Handle particle collisions
function handleCollisions() {
    particles.forEach((p1, index) => {
        for (let i = index + 1; i < particles.length; i++) {
            let p2 = particles[i];
            if (isColliding(p1, p2)) {
                resolveCollision(p1, p2);
            }
        }
    });
}

// Check if two particles are colliding
function isColliding(p1, p2) {
    return (
        p1.x < p2.x + p2.size &&
        p1.x + p1.size > p2.x &&
        p1.y < p2.y + p2.size &&
        p1.y + p1.size > p2.y
    );
}

// Resolve particle collisions
function resolveCollision(p1, p2) {
    if (p1.y < p2.y) {
        const overlap = p1.y + p1.size - p2.y;
        if (overlap > 0 && overlap < p1.size) {
            p1.y -= overlap * 0.5;  // Correct the overlap
            p1.velocityY = 0;  // Stop vertical movement
        }
    } else if (p1.y > p2.y) {
        const overlap = p2.y + p2.size - p1.y;
        if (overlap > 0 && overlap < p2.size) {
            p2.y -= overlap * 0.5;
            p2.velocityY = 0;
        }
    }
}

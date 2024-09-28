const elements = {
    powder: {
        color: '#c2b280',
        flammable: true,
        gravity: 2,
        update: function(particle) {
            applyGravity(particle);
            handleCompression(particle);  // Allow powder to compress and settle
        }
    },
    water: {
        color: '#3498db',
        gravity: 1.5,
        spreadSpeed: 0.8,
        update: function(particle) {
            applyGravity(particle);
            spreadLiquid(particle);  // Water flows sideways
        }
    },
    fire: {
        color: '#e74c3c',
        gravity: -1,  // Fire rises
        lifetime: 200,  // Fire dissipates over time
        spreadChance: 0.01,  // Slow fire spreading to flammable particles
        update: function(particle) {
            applyGravity(particle);
            spreadFire(particle);
            dissipateFire(particle);  // Fire burns out over time
        }
    }
};

// Fire-specific behavior
function spreadFire(particle) {
    if (Math.random() < particle.spreadChance) {
        const nearbyParticles = particles.filter(p =>
            Math.abs(p.x - particle.x) <= particle.size && Math.abs(p.y - particle.y) <= particle.size
        );
        nearbyParticles.forEach(p => {
            if (elements[p.type].flammable) {
                particles.push(new Particle(p.x, p.y, 'fire', p.size));
                p.remove = true;  // Burn the flammable particle
            }
        });
    }
}

function dissipateFire(particle) {
    particle.lifetime--;
    if (particle.lifetime <= 0) {
        particle.remove = true;  // Fire burns out
    }
}

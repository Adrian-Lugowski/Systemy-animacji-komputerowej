class Particle {
    constructor(x, y, vx, vy, hue, active) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.hue = hue;
        this.alpha = 1;
        this.decay = 0.015;
        this.active = active;
    }

    update(gravity, canvasHeight) {
        this.vx *= 0.98;
        this.vy *= 0.98;
        this.x += this.vx;
        this.y += this.vy;
        this.vy += gravity;
        this.alpha -= this.decay;
        if (this.alpha <= 0) {
            this.active = false;
        }
        if (this.y > canvasHeight) {
            this.vy *= -0.6;
            this.y = canvasHeight;
        }
    }

    draw(ctx) {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle = `hsla(${this.hue}, 100%, 50%, ${this.alpha})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

class Firework {
    constructor(startX, startY, targetX, targetY) {
        this.x = startX;
        this.y = startY;
        this.targetX = targetX;
        this.targetY = targetY;

        const speed = 8;
        const dx = targetX - startX;
        const dy = targetY - startY;
        const dist = Math.hypot(dx, dy) || 1;
        this.vx = (dx / dist) * speed;
        this.vy = (dy / dist) * speed;

        this.exploded = false;
        this.active = true;
        this.hue = Math.random() * 360;
    }

    draw(ctx) {
        ctx.save();
        ctx.fillStyle = `hsl(${this.hue}, 100%, 50%)`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    explode(particleCount) {
        const particles = [];
        for (let i = 0; i < particleCount; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 4 + 2;
            const vx = Math.cos(angle) * speed;
            const vy = Math.sin(angle) * speed;
            const hue = this.hue + (Math.random() * 40 - 20);
            particles.push(new Particle(this.x, this.y, vx, vy, hue, true));
        }
        return particles;
    }

    update(particleCount) {
        if (!this.active) return [];

        this.x += this.vx;
        this.y += this.vy;

        if (Math.hypot(this.targetX - this.x, this.targetY - this.y) < 5) {
            this.exploded = true;
            this.active = false;
            return this.explode(particleCount);
        }
        return [];
    }
}

class FireworkShow {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.rockets = [];
        
        this.gravityInput = document.getElementById('gravity');
        this.particleCountInput = document.getElementById('particleCount');
        
        this.gravity = parseFloat(this.gravityInput.value);
        this.particleCount = parseInt(this.particleCountInput.value);

        this.gravityInput.addEventListener('input', (e) => {
            this.gravity = parseFloat(e.target.value);
        });
        
        this.particleCountInput.addEventListener('input', (e) => {
            this.particleCount = parseInt(e.target.value);
        });

        this.canvas.addEventListener('click', (e) => this.onClick(e));

        setInterval(() => this.auto(), 1500);

        this.animate();
    }

    onClick(event) {
        const rect = this.canvas.getBoundingClientRect();
        const targetX = event.clientX - rect.left;
        const targetY = event.clientY - rect.top;
        const startX = this.canvas.width / 2;
        const startY = this.canvas.height;

        const firework = new Firework(startX, startY, targetX, targetY);
        this.rockets.push(firework);
    }

    auto() {
        const targetX = Math.random() * this.canvas.width;
        const targetY = Math.random() * (this.canvas.height / 2);
        const startX = this.canvas.width / 2;
        const startY = this.canvas.height;
        const firework = new Firework(startX, startY, targetX, targetY);
        this.rockets.push(firework);
    }

    update() {
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.globalCompositeOperation = 'lighter';

        for (let rocket of this.rockets) {
            rocket.draw(this.ctx);
            const newParticles = rocket.update(this.particleCount);
            if (newParticles.length > 0) {
                this.particles.push(...newParticles);
            }
        }

        for (let particle of this.particles) {
            particle.update(this.gravity, this.canvas.height);
            particle.draw(this.ctx);
        }

        this.ctx.globalCompositeOperation = 'source-over';

        this.rockets = this.rockets.filter(r => r.active);
        this.particles = this.particles.filter(p => p.active);
    }

    animate() {
        this.update();
        requestAnimationFrame(() => this.animate());
    }
}

window.onload = () => {
    new FireworkShow('firework');
};
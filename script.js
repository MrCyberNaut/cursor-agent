// AR Business Card - The Sawant Drop
// Main JavaScript functionality

class ARBusinessCard {
    constructor() {
        this.isPerformanceOptimized = false;
        this.contactInfo = {
            name: "Your Name",
            email: "you@example.com",
            phone: "+91XXXXXXXXXX",
            website: "https://yourwebsite.com",
            linkedin: "https://linkedin.com/in/yourprofile",
            github: "https://github.com/yourusername",
            twitter: "https://twitter.com/yourusername"
        };
        this.performance = {
            fps: 0,
            frameCount: 0,
            lastTime: performance.now()
        };
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.monitorPerformance();
        this.handleLoading();
        this.setupClickHandlers();
    }

    setupEventListeners() {
        // Wait for A-Frame to be ready
        document.addEventListener('DOMContentLoaded', () => {
            const scene = document.querySelector('a-scene');
            
            if (scene) {
                scene.addEventListener('loaded', () => {
                    this.onSceneLoaded();
                });

                // MindAR specific events
                scene.addEventListener('arReady', () => {
                    console.log('AR is ready');
                    this.hideLoading();
                    this.showInstructions();
                });

                scene.addEventListener('arError', (event) => {
                    console.error('AR Error:', event.detail);
                    this.showError('AR initialization failed. Please check camera permissions.');
                });

                // Target tracking events
                scene.addEventListener('targetFound', () => {
                    console.log('Business card detected!');
                    this.onTargetFound();
                });

                scene.addEventListener('targetLost', () => {
                    console.log('Business card lost');
                    this.onTargetLost();
                });
            }
        });
    }

    onSceneLoaded() {
        console.log('A-Frame scene loaded');
        // Add performance indicator
        this.addPerformanceIndicator();
        
        // Optimize for device performance
        this.optimizeForDevice();
    }

    onTargetFound() {
        // Trigger animations when card is found
        const caricature = document.querySelector('#caricature');
        const socialIcons = document.querySelector('#social-icons');
        const room = document.querySelector('#room');

        if (caricature) {
            caricature.setAttribute('visible', true);
            caricature.setAttribute('animation__appear', {
                property: 'scale',
                from: '0 0 0',
                to: '0.5 0.5 0.5',
                dur: 800,
                easing: 'easeOutBack'
            });
        }

        if (socialIcons) {
            socialIcons.setAttribute('visible', true);
            // Stagger animation for social icons
            const icons = socialIcons.querySelectorAll('.clickable');
            icons.forEach((icon, index) => {
                setTimeout(() => {
                    icon.setAttribute('animation__appear', {
                        property: 'scale',
                        from: '0 0 0',
                        to: '1 1 1',
                        dur: 500,
                        easing: 'easeOutBounce'
                    });
                }, index * 100);
            });
        }

        if (room && !this.isPerformanceOptimized) {
            room.setAttribute('visible', true);
            room.setAttribute('animation__appear', {
                property: 'scale',
                from: '0 0 0',
                to: '0.3 0.3 0.3',
                dur: 1000,
                easing: 'easeOutQuart'
            });
        }

        this.hideInstructions();
    }

    onTargetLost() {
        // Optional: Add fade out animations when target is lost
        console.log('Target lost - keeping AR content visible');
    }

    setupClickHandlers() {
        document.addEventListener('click', (event) => {
            // Get the intersected object from A-Frame raycaster
            const scene = document.querySelector('a-scene');
            const camera = scene.querySelector('a-camera');
            
            if (camera) {
                const raycaster = camera.components.raycaster;
                if (raycaster && raycaster.intersectedEl) {
                    const clickedElement = raycaster.intersectedEl;
                    const action = clickedElement.getAttribute('data-action');
                    
                    if (action) {
                        this.handleAction(action, clickedElement);
                    }
                }
            }
        });

        // Touch events for mobile
        document.addEventListener('touchend', (event) => {
            const scene = document.querySelector('a-scene');
            const camera = scene.querySelector('a-camera');
            
            if (camera) {
                const raycaster = camera.components.raycaster;
                if (raycaster && raycaster.intersectedEl) {
                    const clickedElement = raycaster.intersectedEl;
                    const action = clickedElement.getAttribute('data-action');
                    
                    if (action) {
                        this.handleAction(action, clickedElement);
                    }
                }
            }
        });
    }

    handleAction(action, element) {
        console.log(`Action triggered: ${action}`);
        
        // Add click animation
        element.setAttribute('animation__click', {
            property: 'scale',
            from: '1 1 1',
            to: '0.9 0.9 0.9',
            dur: 100,
            direction: 'alternate',
            loop: 1
        });

        switch (action) {
            case 'website':
                window.open(this.contactInfo.website, '_blank');
                break;
            case 'linkedin':
                window.open(this.contactInfo.linkedin, '_blank');
                break;
            case 'github':
                window.open(this.contactInfo.github, '_blank');
                break;
            case 'twitter':
                window.open(this.contactInfo.twitter, '_blank');
                break;
            case 'email':
                window.open(`mailto:${this.contactInfo.email}`, '_self');
                break;
            case 'add-contact':
                this.downloadVCard();
                break;
            default:
                console.log('Unknown action:', action);
        }
    }

    downloadVCard() {
        const vCardData = this.generateVCard();
        const blob = new Blob([vCardData], { type: 'text/vcard;charset=utf-8' });
        const url = window.URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `${this.contactInfo.name.replace(/\s+/g, '_')}_contact.vcf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        window.URL.revokeObjectURL(url);
        console.log('vCard downloaded');
    }

    generateVCard() {
        return `BEGIN:VCARD
VERSION:3.0
FN:${this.contactInfo.name}
EMAIL:${this.contactInfo.email}
TEL:${this.contactInfo.phone}
URL:${this.contactInfo.website}
NOTE:LinkedIn: ${this.contactInfo.linkedin}\\nGitHub: ${this.contactInfo.github}\\nTwitter: ${this.contactInfo.twitter}
END:VCARD`;
    }

    monitorPerformance() {
        const monitor = () => {
            const now = performance.now();
            const delta = now - this.performance.lastTime;
            
            this.performance.frameCount++;
            
            if (delta >= 1000) {
                this.performance.fps = Math.round((this.performance.frameCount * 1000) / delta);
                this.performance.frameCount = 0;
                this.performance.lastTime = now;
                
                this.updatePerformanceIndicator();
                
                // Auto-optimize if performance is poor
                if (this.performance.fps < 20 && !this.isPerformanceOptimized) {
                    this.optimizePerformance();
                }
            }
            
            requestAnimationFrame(monitor);
        };
        
        monitor();
    }

    optimizeForDevice() {
        // Basic device detection and optimization
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        const hasLowMemory = navigator.deviceMemory && navigator.deviceMemory < 4;
        
        if (isMobile || hasLowMemory) {
            this.optimizePerformance();
        }
    }

    optimizePerformance() {
        console.log('Optimizing for performance...');
        this.isPerformanceOptimized = true;
        
        // Hide the 3D room to improve performance
        const room = document.querySelector('#room');
        if (room) {
            room.setAttribute('visible', false);
        }
        
        // Reduce animation complexity
        const caricature = document.querySelector('#caricature');
        if (caricature) {
            caricature.removeAttribute('animation__float');
        }
        
        // Show performance message
        this.showPerformanceMessage();
    }

    addPerformanceIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'performance-indicator';
        indicator.id = 'fps-counter';
        indicator.innerHTML = 'FPS: --';
        document.body.appendChild(indicator);
    }

    updatePerformanceIndicator() {
        const indicator = document.getElementById('fps-counter');
        if (indicator) {
            const color = this.performance.fps >= 30 ? '#10b981' : 
                         this.performance.fps >= 20 ? '#f59e0b' : '#ef4444';
            indicator.innerHTML = `FPS: ${this.performance.fps}`;
            indicator.style.color = color;
        }
    }

    showPerformanceMessage() {
        const message = document.createElement('div');
        message.className = 'instructions';
        message.innerHTML = '⚡ Optimized for your device';
        message.style.backgroundColor = 'rgba(16, 185, 129, 0.8)';
        document.body.appendChild(message);
        
        setTimeout(() => {
            message.remove();
        }, 3000);
    }

    handleLoading() {
        // Hide loading after a timeout if AR doesn't initialize
        setTimeout(() => {
            this.hideLoading();
        }, 10000);
    }

    hideLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.add('hidden');
            setTimeout(() => {
                overlay.remove();
            }, 500);
        }
    }

    showInstructions() {
        const instructions = document.createElement('div');
        instructions.className = 'instructions';
        instructions.innerHTML = '📱 Point your camera at the business card';
        document.body.appendChild(instructions);
        
        // Hide instructions after 5 seconds
        setTimeout(() => {
            if (instructions.parentNode) {
                instructions.remove();
            }
        }, 5000);
    }

    hideInstructions() {
        const instructions = document.querySelector('.instructions');
        if (instructions) {
            instructions.remove();
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.display = 'block';
        errorDiv.innerHTML = `❌ ${message}`;
        document.body.appendChild(errorDiv);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
}

// Initialize the AR Business Card experience
const arBusinessCard = new ARBusinessCard();

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ARBusinessCard;
}
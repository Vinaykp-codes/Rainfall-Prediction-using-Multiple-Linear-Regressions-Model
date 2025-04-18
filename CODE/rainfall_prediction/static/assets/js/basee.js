document.addEventListener('mousemove', (e) => {
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;

    const content = document.querySelector('.perspective-content');
    const perspectiveContainer = document.querySelector('.perspective-container');

    content.style.transform = `rotateX(${10 + y * 5}deg) rotateY(${x * 5 - 2.5}deg)`;
    perspectiveContainer.style.transform = `translateZ(${y * 10}px)`;
});

function createRain() {
    const perspectiveContainer = document.querySelector('.perspective-container');
    const containerRect = perspectiveContainer.getBoundingClientRect();

    const numRaindrops = Math.floor(Math.random() * 50) + 30;

    for (let i = 0; i < numRaindrops; i++) {
        const raindrop = document.createElement('div');
        raindrop.classList.add('raindrop');
        raindrop.style.left = (Math.random() * containerRect.width) + 'px';
        raindrop.style.top = (Math.random() * containerRect.height / 2) + 'px';
        raindrop.style.animationDuration = (Math.random() * 1 + 0.5) + 's';

        raindrop.style.animationName = 'rainFall';
        raindrop.style.animationIterationCount = 'infinite';
        raindrop.style.animationDirection = 'normal';
        raindrop.style.animationDelay = (Math.random() * 2) + 's';
        raindrop.style.setProperty('--wind-drift', (Math.random() * 20 - 10) + 'px');

        perspectiveContainer.appendChild(raindrop);
    }
}

function initializeCloudsAndRain() {
    const perspectiveContainer = document.querySelector('.perspective-container');
    const perspectiveContent = document.querySelector('.perspective-content');

   
    const cloudShapes = [
        '<svg viewBox="0 0 180 120"><path d="M 60,50 C 40,30 30,70 50,80 C 70,90 90,70 100,80 C 110,90 130,70 120,50 C 140,30 160,70 140,90 C 120,110 90,100 80,80 C 70,100 40,90 50,70 C 30,50 40,30 60,50 Z" fill="skyblue" stroke="none" /></svg>'
    ];

    function createCloud() {
        const cloud = document.createElement('div');
        cloud.classList.add('cloud');
        cloud.innerHTML = cloudShapes[0]; // Always use the first cloud shape
        cloud.style.width = `${Math.random() * 100 + 100}px`;
        cloud.style.height = `${cloud.style.width * 0.6}px`;
        cloud.style.top = `${Math.random() * 100}vh`;
        cloud.style.left = `${Math.random() * 100}vw`;
        cloud.style.animationDuration = `${Math.random() * 10 + 10}s`;
        cloud.style.animationDelay = `${Math.random() * 5}s`;
        perspectiveContent.appendChild(cloud);

        cloud.addEventListener('animationiteration', () => {
            cloud.style.top = `${Math.random() * 100}vh`;
            cloud.style.left = '-200px';
        });
    }

    createRain();
    setInterval(createRain, 3000);

    // Create initial clouds
    for (let i = 0; i < 3; i++) {
        createCloud();
    }
}

initializeCloudsAndRain();

const style = document.createElement('style');
style.innerHTML = `
@keyframes rainFall {
    0% { transform: translateY(0) translateX(0); }
    100% { transform: translateY(100vh) translateX(var(--wind-drift)); }
}
`;
document.head.appendChild(style);
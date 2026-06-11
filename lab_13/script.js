import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const infoDiv = document.getElementById('info');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 2, 10);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);

renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.minDistance = 1;
controls.maxDistance = 50;


const ambientLight = new THREE.AmbientLight(0xffffff, 0.15);
scene.add(ambientLight);
const keyLight = new THREE.DirectionalLight(0xfff0dd, 2.0);
keyLight.position.set(5, 5, 5);
scene.add(keyLight);
const fillLight = new THREE.DirectionalLight(0xddeeff, 1.0);
fillLight.position.set(-5, 3, 5);
scene.add(fillLight);
const rimLight = new THREE.DirectionalLight(0x88ff88, 3.0);
rimLight.position.set(0, 5, -5);
scene.add(rimLight);


const clock = new THREE.Clock();
function animate() {
    requestAnimationFrame(animate);
    const delta = clock.getDelta(); 

    if (biomechModel) {
        biomechModel.rotation.y += 0.2 * delta;
    }

    controls.update(); 
    renderer.render(scene, camera);
}

let biomechModel = null;

async function loadModel() {
    const loader = new GLTFLoader();
    
    try {
        const gltf = await loader.loadAsync('biomech_13.glb');
        biomechModel = gltf.scene;
        scene.add(biomechModel);


        let meshCount = 0;
        biomechModel.traverse((node) => {
            if (node.isMesh) {
                meshCount++;
            }
        });

        infoDiv.innerHTML = `Model wczytany pomyślnie<br>Liczba mesh-y: <strong>${meshCount}</strong>`;
        infoDiv.style.color = "#a3e635";

        const boundingBox = new THREE.Box3().setFromObject(biomechModel);
        const center = boundingBox.getCenter(new THREE.Vector3());
        const size = boundingBox.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);
        camera.position.set(center.x, center.y + (size.y / 4), center.z + maxDim * 1.5);
        controls.target.copy(center);
        controls.update();

    } catch (error) {
        console.error("Błąd loadera GLTF: ", error);
        infoDiv.innerHTML = `Błąd ładowania modelu:<br><em>${error.message}</em>`;
        infoDiv.style.color = "#ff4a4a";
    }
}

loadModel();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

animate();
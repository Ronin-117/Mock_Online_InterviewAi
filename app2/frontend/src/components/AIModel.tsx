// src/components/AIModel.tsx
import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

interface AIModelProps {
  isVideoOff: boolean;
  modelScale: string;
}

const AIModel: React.FC<AIModelProps> = ({ isVideoOff, modelScale }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isVideoOff || !containerRef.current) {
      return;
    }

    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true }); // Enable transparency
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    // Load the GLB model
    const loader = new GLTFLoader();
    loader.load(
      '/models/nikhil.glb', // Replace with your model path
      (gltf) => {
        const model = gltf.scene;
        scene.add(model);

        // Center the model
        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        model.position.sub(center);

        // Calculate the bounding sphere radius
        const boundingSphere = box.getBoundingSphere(new THREE.Sphere());
        const radius = boundingSphere.radius;

        // Adjust camera position based on model size
        // Calculate the distance needed to fit the model in the view
        const fov = camera.fov * (Math.PI / 180); // Convert fov to radians
        const distance = radius / Math.tan(fov / 2);

        // Set camera position
        camera.position.z = distance * 0.3; // Adjust distance as needed
        camera.position.y = radius * 0.5; // Adjust the vertical position (higher)

        // Animation (if any)
        const animations = gltf.animations;
        if (animations && animations.length) {
          const mixer = new THREE.AnimationMixer(model);
          const action = mixer.clipAction(animations[0]); // Play the first animation
          action.play();

          // Animation loop
          const clock = new THREE.Clock();
          const animate = () => {
            requestAnimationFrame(animate);
            const delta = clock.getDelta();
            mixer.update(delta);
            renderer.render(scene, camera);
          };
          animate();
        } else {
          // No animation, just render
          const animate = () => {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
          };
          animate();
        }
      },
      undefined,
      (error) => {
        console.error('An error happened:', error);
      }
    );

    // Orbit Controls (optional)
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.25;
    controls.screenSpacePanning = false;
    controls.maxPolarAngle = Math.PI / 2;

    // Resize handling
    const handleResize = () => {
      const newWidth = container.clientWidth;
      const newHeight = container.clientHeight;
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      controls.dispose();
      renderer.dispose();
      container.removeChild(renderer.domElement);
    };
  }, [isVideoOff]);

  return (
    <div
      ref={containerRef}
      className="w-full h-full"
      style={{ transform: modelScale }}
    />
  );
};

export default AIModel;

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const ThreeScene = () => {
    const mountRef = useRef(null);

    useEffect(() => {
        // Scene, Camera, Renderer
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        if (mountRef.current) {
            mountRef.current.appendChild(renderer.domElement);
        }

        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5); // Soft white light
        scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
        directionalLight.position.set(1, 1, 1); // From top-right
        scene.add(directionalLight);

        // Load GLTF Model
        const loader = new GLTFLoader();
        loader.load(
          '/models/scene.gltf', // Correct path to the model within public
          (gltf) => {
            console.log("Model loaded successfully!", gltf); // Added log
            const model = gltf.scene;
            scene.add(model);

            // Adjust model scale and position (adjust these values as needed)
            model.scale.set(0.1, 0.1, 0.1); // Scale down the model
            model.position.set(0, -1, 0); // Adjust position

            // Camera and Scene must be 100% loaded so added rotation of 0
            model.rotation.y = 0.01;
            camera.position.set(0, 0, 5);
            // Animation Loop
            const animate = () => {
              requestAnimationFrame(animate);
              model.rotation.y += 0.01;  // Rotate the model

              renderer.render(scene, camera);
            };

            animate();
          },
          (xhr) => {
            console.log((xhr.loaded / xhr.total * 100) + '% loaded');
          },
          (error) => {
            console.error('An error happened', error);
          }
        );


        // Handle Window Resize
        const handleResize = () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        };
        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
            if (mountRef.current) {
                mountRef.current.removeChild(renderer.domElement); // Clean up
            }
            renderer.dispose();
        };

    }, []);

    return <div ref={mountRef} style={{ width: '100vw', height: '100vh' }} />;
};

export default ThreeScene;
// src/components/AIModel2.tsx
import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

interface AIModelProps {
  isVideoOff: boolean;
  modelScale: string;
}

const AIModel: React.FC<AIModelProps> = ({ isVideoOff, modelScale }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const modelRef = useRef<THREE.Object3D | null>(null);
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();
  const isHoveringRef = useRef<boolean>(false);
  const targetMeshRef = useRef<THREE.Mesh | null>(null);
  const mouthOpenIndexRef = useRef<number | null>(null);

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

    // Load background texture
        const textureLoader = new THREE.TextureLoader();
        textureLoader.load(
          '/background.jpg', // Path to your background image in the public folder
          (texture) => {
            scene.background = texture;
          },
          undefined,
          (error) => {
            console.error('An error happened while loading the background image:', error);
          }
        );

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    // Load the GLB model
    const loader = new GLTFLoader();
    loader.load(
      '/models/m1.glb', // Replace with your model path
      (gltf) => {
        const model = gltf.scene;
        modelRef.current = model;
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
        camera.position.z = distance * 0.15; // Adjust distance as needed
        camera.position.y = radius * 0.3; // Adjust the vertical position (higher)

        // Find the Cesar_D_LaTorre_Jacket group
        const jacket = model.getObjectByName("Cesar_D_LaTorre_Jacket");
        if (!jacket) {
          console.error("Group with name 'Cesar_D_LaTorre_Jacket' not found.");
          return;
        }

        // Find the Character.001 mesh within the jacket group
        const characterMesh = jacket.getObjectByName("Character.001") as THREE.Mesh;
        if (!characterMesh || !characterMesh.isMesh) {
          console.error("Mesh with name 'Character.001' not found within 'Cesar_D_LaTorre_Jacket'.");
          return;
        }
        targetMeshRef.current = characterMesh;

        // Get the index of the "Mouth_Open" shape key
        if (characterMesh.geometry.morphTargetDictionary) {
          mouthOpenIndexRef.current = characterMesh.geometry.morphTargetDictionary['Mouth_Open'];
        }

        if (mouthOpenIndexRef.current === undefined) {
          console.error("Shape key 'Mouth_Open' not found.");
          return;
        }

        // Animation loop (now just renders)
        const animate = () => {
          requestAnimationFrame(animate);
          renderer.render(scene, camera);
        };
        animate();
      },
      undefined,
      (error) => {
        console.error('An error happened:', error);
      }
    );

    // Resize handling
    const handleResize = () => {
      const newWidth = container.clientWidth;
      const newHeight = container.clientHeight;
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', handleResize);

    // Mouse hover event
    const onMouseMove = (event: MouseEvent) => {
      if (!modelRef.current || !targetMeshRef.current || mouthOpenIndexRef.current === null) return;
      mouse.x = (event.clientX / container.clientWidth) * 2 - 1;
      mouse.y = -(event.clientY / container.clientHeight) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      // Corrected line: Use modelRef.current instead of modelRef.current.children
      const intersects = raycaster.intersectObjects([modelRef.current], true);

      if (intersects.length > 0) {
        if (!isHoveringRef.current) {
          console.log("Mouse entered the model");
          isHoveringRef.current = true;
          targetMeshRef.current.morphTargetInfluences![mouthOpenIndexRef.current] = 1; // Activate shape key (set to 1)
        }
      } else {
        if (isHoveringRef.current) {
          console.log("Mouse left the model");
          isHoveringRef.current = false;
          targetMeshRef.current.morphTargetInfluences![mouthOpenIndexRef.current] = 0; // Deactivate shape key (set to 0)
        }
      }
    };

    container.addEventListener('mousemove', onMouseMove);
    container.addEventListener('mouseleave', () => {
      // Reset shape key when mouse leaves the container
      if (isHoveringRef.current && targetMeshRef.current && mouthOpenIndexRef.current !== null) {
        console.log("Mouse left the container");
        isHoveringRef.current = false;
        targetMeshRef.current.morphTargetInfluences![mouthOpenIndexRef.current] = 0; // Reset shape key to 0
      }
    });

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      container.removeEventListener('mousemove', onMouseMove);
      container.removeEventListener('mouseleave', () => {});
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

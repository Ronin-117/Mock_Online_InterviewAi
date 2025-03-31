import { useThree } from "@react-three/fiber";
//import { Avatar } from "./Avatar2";
//import { OrbitControls, Stage } from "@react-three/drei";
import { useGLTF } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useRef } from "react";
import * as THREE from "three";
import { useTexture, Environment } from "@react-three/drei";


export const Experience = () => {
  const texture = useTexture("textures/youtubeBackground.jpg");
  const viewport = useThree((state) => state.viewport);

  return (
    <>
      {/* <OrbitControls /> */}
      {/* <Avatar position={[0, -3, 5]} scale={2} /> */}
      <Environment preset="sunset" />
      <mesh>
        <planeGeometry args={[viewport.width, viewport.height]} />
        <meshBasicMaterial map={texture} />
      </mesh>
    </>
  );
};

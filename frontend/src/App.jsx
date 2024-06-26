import React from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Plane } from "@react-three/drei";
import { TextureLoader } from "three";

const Scene = () => {
  // Load the textures
  const diffuseTexture = new TextureLoader().load("/diffuse_image.png");
  //const normalTexture = new TextureLoader().load("/DefaultMaterial_Normal.png");
  const displacementTexture = new TextureLoader().load("/displacement_image.png");

  return (
    <group>
      {/* Plane with textures */}
      <Plane args={[8, 8, 2500, 2500]} rotation-x={-Math.PI / 2}>
        <meshStandardMaterial 
          map={diffuseTexture} 
          //normalMap={normalTexture} 
          displacementMap={displacementTexture}
          displacementScale={0.5} // adjust the scale as needed
          roughness={5} // Set the roughness here, value ranges from 0 to 1
          metalness={0}

          
        />
      </Plane>
    </group>
  );
};

export default function App() {
  return (
    <Canvas
      camera={{ position: [-5, 4, -5], rotation: [-Math.PI / 2, Math.PI / 2, 0] }}
    >
      <ambientLight intensity={0} color="white" />
      <directionalLight intensity={1} color="white" position={[-5, 4, -5]} />
      <directionalLight intensity={1} color="blue" position={[5, 4, -5]} />
      <directionalLight intensity={1} color="white" position={[-5, 4, 5]} />
      <directionalLight intensity={1} color="blue" position={[5, 4, 5]} />

      <directionalLight intensity={1} color="white" position={[-5, 4, 0]} />
      <directionalLight intensity={1} color="blue" position={[5, 4, 0]} />

      <Scene />
      <OrbitControls />
    </Canvas>
  );
}
